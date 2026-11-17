# FIT4112 – Lab 4: Dự báo PM2.5 bằng dữ liệu chuỗi thời gian

**Học phần:** Khai phá dữ liệu (Data Mining) · **Đối tượng:** HTTT và PTPM  
**Bài toán:** Dự báo nồng độ PM2.5 tại giờ t từ dữ liệu đã biết đến hết giờ t−1 (one-step-ahead, rolling observation).  
**Nguồn phát triển:** [air_quality_timeseries](https://github.com/TrangLe1912/air_quality_timeseries) – phiên bản **Student Friendly**.

Lab 4 chuyển từ khai phá luật kết hợp/phân cụm (Lab 1–3) sang **dự báo có yếu tố thời gian**. Sinh viên không cần học ARIMA trước và không cần chạy Papermill.

## Mục tiêu sau lab
1. Hiểu quan sát theo thời gian; làm sạch chuỗi của **một trạm** và xử lý khoảng trống bằng giá trị đã quan sát trước đó (không nhìn tương lai).
2. Chuyển chuỗi thành bảng hồi quy với lag 1, 3, 24 giờ; giải thích tại sao không dùng giá trị PM2.5 của chính giờ cần dự báo.
3. Chia tập train/test **theo thời gian** và so sánh mô hình với baseline persistence.
4. Đánh giá bằng MAE/RMSE, trực quan hóa và giải thích trường hợp mô hình không hơn baseline.
5. Nêu được giới hạn: dữ liệu giả lập, quan sát rolling one-step khác dự báo đồng thời nhiều giờ vào tương lai, sai số khi thiếu cảm biến.

## Cấu trúc
~~~text
fit4112_lab_4/
├── README.md
├── requirements.txt
├── src/
│   └── lab4.py                         # hàm dùng chung, tập trung logic kiểm soát leakage
├── scripts/
│   └── generate_demo_data.py           # tự sinh dữ liệu PM2.5 giả lập
├── data/raw/README.md                  # cách dùng dữ liệu thật tùy chọn
├── notebooks/
│   ├── 01_prepare_and_eda.ipynb        # dữ liệu, missing, biểu đồ
│   ├── 02_time_split_and_baseline.ipynb# lag features, split, persistence
│   ├── 03_regression_forecast.ipynb    # RandomForest, so sánh, đánh giá
│   └── 04_arima_optional.ipynb         # ARIMA chỉ dành cho mở rộng
├── docs/
│   ├── LAB04_STUDENT.md
│   ├── TRACKS.md
│   ├── REPORT_TEMPLATE.md
│   └── INSTRUCTOR_GUIDE.md
├── tests/
│   ├── smoke_test.py
│   └── run_notebooks.py
└── .github/workflows/validate.yml
~~~

## Chạy nhanh
Yêu cầu Python 3.11 hoặc 3.12. Tại thư mục repository:
~~~bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
~~~

Chạy **01 → 02 → 03** trong VS Code/JupyterLab. Notebook 01 **tự tạo dữ liệu giả lập** tại data/raw/demo_pm25_hourly.csv khi chưa có file. Không cần tải dữ liệu để bắt đầu; hai notebook sau đọc kết quả của notebook trước.

Nếu muốn tạo dữ liệu trước:
~~~bash
python scripts/generate_demo_data.py
~~~

Kiểm tra dành cho giảng viên:
~~~bash
python tests/smoke_test.py
python tests/run_notebooks.py
~~~

## Hai lộ trình cùng chuẩn chấm

| | **FOUNDATION – gợi ý HTTT** | **APPLIED – gợi ý PTPM** |
|---|---|---|
| Hướng dẫn | Code mẫu, chạy và giải thích từng bước | Tự đối chiếu hai cấu hình đặc trưng trên validation |
| Mô hình | RandomForest cố định + baseline | Chọn lag-only hoặc lag+calendar bằng validation |
| Đánh giá | Giải thích MAE/RMSE, biểu đồ, giới hạn | Cùng đầu ra, có thêm lập luận chọn cấu hình |
| Điểm tối đa | **100/100** | **100/100** |

Trong Notebook 03 đổi TRACK = "FOUNDATION" hoặc TRACK = "APPLIED". **Sinh viên tự chọn lộ trình, không bị khóa theo lớp**, không cộng điểm vì chọn Applied. Xem [docs/TRACKS.md](docs/TRACKS.md).

## Bài nộp
- Ba notebook bắt buộc đã chạy (có kết quả và trả lời câu hỏi).
- Báo cáo ngắn theo [docs/REPORT_TEMPLATE.md](docs/REPORT_TEMPLATE.md), tối đa 2 trang.
- Ghi MAE/RMSE của **baseline và mô hình trên cùng tập test**; nêu ít nhất một giới hạn.
- Không nộp file dữ liệu thật nhiều GB, data/processed, .venv hoặc cache.

Chi tiết và rubric 100 điểm: [docs/LAB04_STUDENT.md](docs/LAB04_STUDENT.md).

## Đổi sang dữ liệu thật (tự chọn)
Đọc [data/raw/README.md](data/raw/README.md). Đặt ZIP gốc của Beijing Multi-Site Air Quality vào data/raw/, sau đó trong Notebook 01 đặt DATA_SOURCE = "uci_zip", STATION = "Aotizhongxin" (hoặc trạm có trong ZIP). Khi chuyển nguồn, **chạy lại cả 3 notebook** để kết quả không lẫn bộ dữ liệu.

## Lưu ý phương pháp
- Đây là dự báo **1 giờ trước, rolling**: tại mỗi giờ t, có thể sử dụng số đo đến t−1. Không được hiểu kết quả này là dự báo cố định 24 giờ khi chưa có bất kỳ số đo mới nào.
- Điểm đo thiếu được điền **forward-fill** chỉ nhằm tạo lag từ thông tin quá khứ; **không đánh giá mô hình trên nhãn đã điền thiếu**.
- Chia test theo thời gian, không dùng random split. Applied chọn cấu hình trên **validation thuộc train**, không nhìn test để chọn.
- Dữ liệu demo là **dữ liệu giả lập**, không đưa ra nhận định thật về Bắc Kinh.
- Notebook ARIMA là **tự chọn**; bài toán forecast 24 giờ cố định của ARIMA **không so sánh trực tiếp** với one-step rolling trên test của Notebook 03.

**Không bắt buộc:** Papermill, dashboard Streamlit, nhiều trạm, ADF/KPSS, grid-search ARIMA hay xây dựng mô hình deep learning.
