# FIT4112 – Phiếu thực hành Lab 04: Dự báo PM2.5 theo giờ

**Hình thức:** cá nhân, một buổi dự kiến 200 phút.  
**Bài nộp:** 3 notebook chạy thành công + báo cáo **tối đa 2 trang**.  
**Nguồn:** dữ liệu PM2.5 giả lập (được tạo tự động), có thể chuyển sang dữ liệu thật nếu đủ năng lực.  
**Lộ trình:** `FOUNDATION` hoặc `APPLIED`; sinh viên **tự chọn**, cùng điểm tối đa 100.

## Mục tiêu
- Xác định được mỗi bản ghi là một thời điểm, nhận diện missing value và timestamp trống.
- Tạo lag 1, 3, 24 giờ, giải thích biến mục tiêu dự báo **PM2.5(t)** chỉ dùng thông tin có trước t.
- Chia tập theo thời gian, xây dựng persistence baseline và một mô hình RandomForest.
- Phân tích MAE/RMSE, biểu đồ thực tế – dự báo; nêu giới hạn của dự báo một bước.

## Thực hành và thang điểm

### A – Dữ liệu và EDA (20 điểm)
Chạy `01_prepare_and_eda.ipynb`. Ghi số bản ghi, số thời điểm thiếu/giá trị âm, quan sát chu kỳ ngày và trả lời:
1. Số đo PM2.5 âm có hợp lệ không?
2. Vì sao điền thiếu bằng **forward-fill (chỉ dữ liệu trước đó)**, không nội suy dùng dữ liệu sau thời điểm t?
3. Có được tính giá trị ffill thành nhãn thật khi chấm mô hình không?

### B – Chuyển chuỗi thành bài toán dự báo (20 điểm)
Chạy `02_time_split_and_baseline.ipynb`. Giải thích ý nghĩa một hàng của bảng mô hình và `lag_1`, `lag_3`, `lag_24`. Chỉ ra khoảng train/test, mô tả lý do chia theo thời gian và chống leakage.

### C – Baseline và mô hình hồi quy (25 điểm)
Tính MAE, RMSE của persistence baseline và RandomForest trên **cùng test**:
- **Foundation:** chạy cấu hình `TRACK="FOUNDATION"` và giải thích dữ liệu đầu vào, hai thước đo.
- **Applied:** đặt `TRACK="APPLIED"`, thử hai bộ đặc trưng *lag-only* và *lag + giờ trong ngày*, chọn theo **validation thuộc train**, sau đó đánh giá test. Có bảng validation và lập luận lựa chọn.

**Công bằng:** cùng chuẩn là sử dụng mô hình hợp lệ và giải thích so sánh có căn cứ; Foundation không cần thử nhiều cấu hình để đạt điểm tối đa. Nếu RandomForest kém baseline, giải thích thay vì chỉnh số liệu.

### D – Đọc biểu đồ và phân tích sai số (20 điểm)
Chọn hai khoảng thời gian/điểm dự báo đáng chú ý trên test. Nêu khi nào mô hình sai lớn, vì sao có thể sai và đề xuất một cải tiến khả thi **không dựa vào chỉnh hyperparameter liên tục trên test**.

### E – Kết luận và báo cáo (15 điểm)
Viết báo cáo tối đa 2 trang với số liệu, biểu đồ, hai kết luận chính và ít nhất **hai giới hạn**: dữ liệu giả lập, dự báo rolling một giờ, missing sensors, phân phối thay đổi, v.v.

## Rubric

| Tiêu chí | Điểm |
|---|---:|
| A. Đọc/làm sạch/khảo sát dữ liệu có giải thích | 20 |
| B. Lag đúng thời gian; chia train/test hợp lệ | 20 |
| C. Baseline, mô hình, MAE/RMSE và so sánh | 25 |
| D. Diễn giải kết quả và phân tích sai số | 20 |
| E. Báo cáo có căn cứ, chỉ ra giới hạn | 15 |
| **Tổng** | **100** |

## Nộp bài
- `01_prepare_and_eda.ipynb`, `02_time_split_and_baseline.ipynb`, `03_regression_forecast.ipynb` có output, câu trả lời ngắn.
- Báo cáo `LAB04_REPORT.md` hoặc PDF theo mẫu `docs/REPORT_TEMPLATE.md`.
- Không nộp `.venv`, `data/processed`, ZIP dữ liệu lớn hoặc cache.
- **Không bắt buộc** notebook 04 ARIMA, dashboard, Papermill hoặc tự triển khai RandomForest.

## Vài điểm dễ nhầm
- *Rolling one-step ahead* tại giờ t có thể quan sát số đo đến t−1. Khác **dự báo từ cùng một mốc ban đầu cho 24 giờ sau**.
- Lấy `PM2.5(t)` để dự báo lại `PM2.5(t)` là leakage.
- Dữ liệu giả lập không chứng minh bất kỳ điều gì về ô nhiễm thực tế.
- RMSE thường nhạy hơn MAE với lỗi dự báo lớn; cả hai càng thấp càng tốt.
