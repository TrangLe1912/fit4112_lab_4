# Hai lộ trình trong FIT4112 Lab 4

Một bài Lab, một rubric 100 điểm. Sinh viên được chọn lộ trình dựa trên năng lực; không giới hạn theo lớp.

## Foundation – gợi ý HTTT
1. Chạy Notebook 01; đọc dữ liệu theo giờ, xử lý thiếu và giải thích forward-fill.
2. Chạy Notebook 02; hiểu lag features, chia train/test theo thời gian và persistence baseline.
3. Notebook 03: chọn `TRACK = "FOUNDATION"`, giữ cấu hình mặc định của RandomForest.
4. Tập trung đọc bảng MAE/RMSE, biểu đồ; nêu 2 điểm sai số cao và giới hạn. Không phải tìm siêu tham số tối ưu.

## Applied – gợi ý PTPM
1. Hai notebook đầu dùng giống Foundation.
2. Notebook 03: chọn `TRACK = "APPLIED"`. Code mẫu chạy hai cấu hình `lag_only` và `lag_plus_hour`, tự giải thích thêm việc thêm hour sin/cos có lợi hay không.
3. Chọn theo **MAE validation** trên đoạn cuối train, tuyệt đối không dò thông số trên test.
4. Fit lại trên toàn train bằng cấu hình chọn, chấm test một lần. Nếu test kém baseline, phản biện nguyên nhân, không chọn lại theo test.

## Công bằng
- **Foundation và Applied cùng có thể nhận 100/100.**
- Foundation được chấm mức độ hiểu đúng quy trình và diễn giải trung thực.
- Applied được chấm trên lựa chọn/giải thích cấu hình và cách tránh leakage; không cộng điểm chỉ vì có nhiều mô hình.
- Không bắt buộc Applied cho sinh viên PTPM hoặc Foundation cho HTTT.
- ARIMA Notebook 04 tự chọn, không là điều kiện điểm tối đa.

## Phân biệt bài toán
- **One-hour rolling:** với mỗi thời điểm t trên test, cập nhật số đo gần nhất t−1 (dữ liệu thực sự đến từng giờ).
- **24-hour fixed-origin:** đưa ra 24 dự báo từ cùng thời điểm ban đầu, không sử dụng quan sát mới. Không lấy MAE của hai setting này để so như thể là cùng điều kiện.
