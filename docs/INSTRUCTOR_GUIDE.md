# FIT4112 Lab 04 – Hướng dẫn giảng viên

## Phạm vi và mục tiêu sư phạm
Lab 4 chuyển từ khai phá mẫu và phân cụm sang dự báo PM2.5(t) bằng các lag t−1,t−3,t−24 trên chuỗi một trạm. Khối lượng dự kiến **200 phút** (có thể điều chỉnh theo thực tế).

| Giai đoạn | Dự kiến | Trọng tâm |
|---|---:|---|
| Khởi động, phân biệt dự báo/đọc xu hướng | 20 phút | t, lag, one-step rolling |
| Notebook 01 | 45 phút | cảm biến thiếu, irregular timestamp, EDA |
| Notebook 02 | 45 phút | lag, chronological split, persistence |
| Notebook 03 | 65 phút | RandomForest, MAE/RMSE, validation |
| Tổng kết, viết báo cáo | 25 phút | so sánh và giới hạn |

## Phân hóa
Foundation (gợi ý HTTT) đọc/rà soát code mẫu, không viết model từ đầu. Applied (gợi ý PTPM) xem xét hai bộ đặc trưng trên validation thuộc train. Cả hai chung rubric 100 điểm. Học sinh được tự chọn lộ trình, không chấm thưởng Applied.

## Chuẩn bị trước buổi
~~~bash
python -m pip install -r requirements.txt
python tests/smoke_test.py
python tests/run_notebooks.py
~~~
Notebook 01 tạo dữ liệu giả lập có một số missing/negative, không cần ZIP ngoài. Notebook 04 (ARIMA) chỉ dành cho mở rộng; không đòi chạy khi đánh giá bắt buộc.

## Chống leakage
- Nhãn `PM2.5(t)` không được xuất hiện trong feature `t`. Chỉ lag quá khứ, các đặc trưng thời gian biết trước.
- Không điền thiếu bằng bfill/nội suy hai chiều trước khi tạo lag.
- Bảng hourly vẫn có giá trị ffill để tạo đầu vào, nhưng `observed_target=False` được loại khỏi bảng tính MAE/RMSE.
- Chia theo thời gian, không random split. Khi chọn cấu hình Applied: validation phải ở trong train.
- Đánh giá ngoài đời thật còn cần kiểm tra độ trễ công bố của cảm biến, độ ổn định của chuỗi và khả năng thay đổi phân phối.

## Đánh giá
Rubric xem `LAB04_STUDENT.md`. Không trừ điểm nếu RandomForest kém persistence mà giải thích đúng. **Không đánh đồng kết quả one-step rolling với 24h fixed origin.** Không đánh đồng dữ liệu demo với Beijing thực.

## Kiểm tra thủ công nhanh
1. Chạy lần lượt 01 → 02 → 03 với mặc định Foundation.
2. Chạy lại 03 với `TRACK="APPLIED"`, xác nhận có bảng validation, không dùng test để chọn.
3. Xác nhận có `data/processed/forecast_predictions.csv` và `forecast_metrics.json`.
4. Khi dùng UCI ZIP (tự chọn), kiểm tra trạm trong file; chạy lại 01 → 02 → 03.
5. Sinh viên cần nêu **nguồn dữ liệu thực/giả lập** trên báo cáo.

## Khả năng phát triển
Sau buổi học có thể đề xuất thử lag dài hơn, mô hình mùa vụ, phân tích drift hoặc so sánh ARIMA one-step rolling trên cùng tập, nhưng các mục này không thuộc chuẩn bắt buộc Lab 04.
