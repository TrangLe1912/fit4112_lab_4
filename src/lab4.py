"""Helpers for FIT4112 Lab 4: strictly causal, rolling one-hour PM2.5 forecasting.

Teaching rules:
- raw PM2.5 at hour t is the label; only earlier PM2.5 appears in features.
- forward fill uses history only; missing hourly labels are never scored.
- test is chronologically later than train; model selection uses train/validation.
"""
from __future__ import annotations

import csv
import math
import random
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


LAG_FEATURES = ["lag_1", "lag_3", "lag_24"]
FULL_FEATURES = LAG_FEATURES + ["hour_sin", "hour_cos"]


def project_root() -> Path:
    cwd = Path.cwd().resolve()
    for folder in (cwd, *cwd.parents):
        if (folder / "src" / "lab4.py").exists():
            return folder
    raise FileNotFoundError("Hãy chạy Jupyter từ trong repository fit4112_lab_4.")


def generate_demo(path: Path, n_hours: int = 24 * 35, seed: int = 4112) -> Path:
    """Tạo dữ liệu GIẢ LẬP; có dòng mất, thiếu số đo và giá trị âm để luyện làm sạch."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    begin = pd.Timestamp("2025-01-01 00:00:00")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["datetime", "station", "PM2.5"])
        for i in range(n_hours):
            if i > 0 and i % 137 == 0:
                continue  # mất trọn một mốc giờ
            hour = i % 24
            daily = 17 * math.sin(2 * math.pi * (hour - 7) / 24)
            weekly = 12 * math.sin(2 * math.pi * i / (24 * 7))
            event = 32 if 240 <= i < 272 else 0
            value = max(2, 65 + daily + weekly + event + 0.012 * i + rng.gauss(0, 8))
            if i > 0 and i % 97 == 0:
                value = ""  # cảm biến thiếu
            if i > 0 and i % 181 == 0:
                value = -9  # lỗi cảm biến; không hiểu là giá trị hợp lệ
            writer.writerow([(begin + pd.Timedelta(hours=i)).isoformat(sep=" "), "DEMO_STATION", value if value == "" else round(value, 2)])
    return path


def load_raw(root: Path, source: str = "demo", station: str = "Aotizhongxin", last_hours: int = 24 * 60) -> pd.DataFrame:
    """Demo tự sinh. UCI ZIP đọc đúng một trạm; giới hạn 60 ngày cuối để máy SV chạy nhẹ."""
    root = Path(root)
    if source == "demo":
        path = root / "data/raw/demo_pm25_hourly.csv"
        if not path.exists():
            generate_demo(path)
        raw = pd.read_csv(path)
    elif source == "uci_zip":
        path = root / "data/raw/PRSA2017_Data_20130301-20170228.zip"
        if not path.exists():
            raise FileNotFoundError(f"Chưa có ZIP UCI: {path}")
        with zipfile.ZipFile(path) as zf:
            matches = [name for name in zf.namelist() if name.lower().endswith(".csv") and station.lower() in Path(name).name.lower()]
            if not matches:
                raise ValueError(f"Không tìm thấy trạm {station!r} trong ZIP UCI.")
            with zf.open(matches[0]) as f:
                raw = pd.read_csv(f)
        if "datetime" not in raw:
            raw["datetime"] = pd.to_datetime(raw[["year", "month", "day", "hour"]], errors="coerce")
        if "station" in raw:
            raw = raw.loc[raw["station"].astype(str).str.lower() == station.lower()].copy()
        raw = raw.sort_values("datetime").tail(last_hours).copy()
    else:
        raise ValueError("source chỉ nhận 'demo' hoặc 'uci_zip'.")
    required = {"datetime", "PM2.5"}
    if not required.issubset(raw):
        raise ValueError(f"Thiếu các cột {sorted(required - set(raw))}")
    return raw[["datetime", "PM2.5"]].copy()


def prepare_hourly(raw: pd.DataFrame) -> pd.DataFrame:
    """Chuẩn hóa giờ, invalid<0 -> NaN, lấp chỗ trống theo quá khứ (ffill).

    observed_target=True chỉ khi số đo gốc tồn tại và hợp lệ;
    giá trị điền thiếu không bao giờ được coi là ground truth.
    """
    x = raw[["datetime", "PM2.5"]].copy()
    x["datetime"] = pd.to_datetime(x["datetime"], errors="coerce")
    x["PM2.5"] = pd.to_numeric(x["PM2.5"], errors="coerce")
    x.loc[x["PM2.5"] < 0, "PM2.5"] = np.nan
    x = x.dropna(subset=["datetime"]).sort_values("datetime")
    if x.empty:
        raise ValueError("Không có timestamp hợp lệ.")
    measured = x.groupby("datetime")["PM2.5"].mean().resample("h").mean()
    observed = measured.notna()
    filled = measured.ffill()  # tuyệt đối không bfill/interpolate cả hai phía
    result = pd.DataFrame({
        "datetime": filled.index,
        "pm25": filled.to_numpy(),
        "observed_target": observed.to_numpy(),
    })
    result = result.dropna(subset=["pm25"]).reset_index(drop=True)
    if len(result) < 96:
        raise ValueError("Cần >=96 giờ dữ liệu để tạo lag và chia train/test.")
    return result


def make_model_frame(hourly: pd.DataFrame) -> pd.DataFrame:
    """Bảng mỗi hàng là dự báo PM2.5(t) từ PM2.5(t-1,t-3,t-24) + giờ biết trước."""
    x = hourly[["datetime", "pm25", "observed_target"]].copy()
    x = x.sort_values("datetime").reset_index(drop=True)
    step = x["datetime"].diff().dropna()
    if not step.eq(pd.Timedelta(hours=1)).all():
        raise ValueError("Chuỗi cần đều theo giờ. Hãy chạy prepare_hourly.")
    for lag in (1, 3, 24):
        x[f"lag_{lag}"] = x["pm25"].shift(lag)
    hour = x["datetime"].dt.hour
    x["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    x["hour_cos"] = np.cos(2 * np.pi * hour / 24)
    x["y"] = x["pm25"]
    # Chỉ giữ nhãn đo THẬT; lag có thể đã ffill từ quá khứ.
    x = x.dropna(subset=LAG_FEATURES)
    x = x.loc[x["observed_target"]].copy()
    return x.drop(columns=["pm25", "observed_target"]).reset_index(drop=True)


def time_split(frame: pd.DataFrame, test_fraction: float = 0.2):
    """Chia đúng thứ tự thời gian; không shuffle."""
    if not 0 < test_fraction < 0.5:
        raise ValueError("test_fraction phải nằm trong khoảng (0,0.5).")
    if len(frame) < 60:
        raise ValueError("Không đủ quan sát hợp lệ để chia.")
    k = int(len(frame) * (1 - test_fraction))
    train, test = frame.iloc[:k].copy(), frame.iloc[k:].copy()
    if train["datetime"].max() >= test["datetime"].min():
        raise AssertionError("Time leakage trong chia tập!")
    return train, test


def error_metrics(actual, predicted) -> dict:
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    if actual.shape != predicted.shape or actual.size == 0:
        raise ValueError("Kích thước actual/predicted không hợp lệ.")
    if not (np.isfinite(actual).all() and np.isfinite(predicted).all()):
        raise ValueError("Không được chấm điểm trên dữ liệu NaN/vô hạn.")
    return {
        "MAE": float(mean_absolute_error(actual, predicted)),
        "RMSE": float(np.sqrt(mean_squared_error(actual, predicted))),
    }


def baseline_predict(frame: pd.DataFrame) -> np.ndarray:
    """Persistence: PM2.5(t) = PM2.5 đã biết gần nhất tại t−1."""
    return frame["lag_1"].to_numpy(dtype=float)


def fit_rf(train: pd.DataFrame, features=FULL_FEATURES, max_depth: int = 7):
    """Chỉ cho phép các đặc trưng biết trước thời điểm cần dự báo."""
    cols = list(features)
    if not cols or not set(cols).issubset(set(FULL_FEATURES)):
        raise ValueError("Features chỉ được là lag_1,lag_3,lag_24,hour_sin,hour_cos.")
    model = RandomForestRegressor(
        n_estimators=80, max_depth=max_depth, min_samples_leaf=3,
        random_state=42, n_jobs=2
    )
    model.fit(train[cols], train["y"])
    return model


def model_predict(model, frame: pd.DataFrame, features=FULL_FEATURES):
    return model.predict(frame[list(features)])
