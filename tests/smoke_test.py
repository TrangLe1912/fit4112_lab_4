"""Fast, deterministic checks. Run: python tests/smoke_test.py"""
from pathlib import Path
import sys
import tempfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.lab4 import (
    generate_demo, prepare_hourly, make_model_frame, time_split,
    baseline_predict, fit_rf, model_predict, error_metrics, FULL_FEATURES
)

def run():
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / "demo.csv"
        generate_demo(path, seed=4112)
        a = pd.read_csv(path)
        assert len(a) > 700
        hourly = prepare_hourly(a)
        assert (~hourly["observed_target"]).sum() > 0
        # Không được dùng dữ liệu tương lai để lấp một khoảng trống trong quá khứ
        missing_idx = np.flatnonzero(~hourly["observed_target"].to_numpy())
        assert len(missing_idx) > 0
        j = int(missing_idx[0])
        assert hourly.loc[j, "pm25"] == hourly.loc[j-1, "pm25"]
        frame = make_model_frame(hourly)
        assert not frame["y"].isna().any()
        assert set(FULL_FEATURES).issubset(frame.columns)
        assert "pm25" not in frame.columns
        # Không có nhãn từ mốc giờ bị thiếu
        missing_t = set(hourly.loc[~hourly["observed_target"], "datetime"])
        assert not any(t in missing_t for t in frame["datetime"])
        # t-1 khớp số đo ffill ở một giờ trước, không phải nhãn hiện tại
        lookup = hourly.set_index("datetime")["pm25"]
        sample = frame.iloc[20]
        assert sample["lag_1"] == lookup.loc[sample["datetime"] - pd.Timedelta(hours=1)]
        train, test = time_split(frame)
        assert train["datetime"].max() < test["datetime"].min()
        base = baseline_predict(test)
        assert np.isfinite(base).all()
        mod = fit_rf(train)
        pred = model_predict(mod, test)
        values = error_metrics(test["y"], pred)
        assert all(np.isfinite(v) and v >= 0 for v in values.values())
        # Schema checks & rejection of leaking feature
        try:
            fit_rf(train, ["y"])
            raise AssertionError("Feature leakage guard failed")
        except ValueError:
            pass
    print("PASS: causal ffill, invalid labels excluded, lag alignment, time split, baseline, ML model.")

if __name__ == "__main__":
    run()
