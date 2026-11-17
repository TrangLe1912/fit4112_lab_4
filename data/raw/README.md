# Dữ liệu Lab 4

**Mặc định:** data/raw/demo_pm25_hourly.csv được tạo tự động bằng scripts/generate_demo_data.py hoặc khi chạy Notebook 01. Đây là dữ liệu **giả lập**, trạm DEMO_STATION, 35 ngày theo giờ, cố ý có vài giờ không có bản ghi, giá trị thiếu và số âm.

**Mở rộng với dữ liệu thực:** tải bộ [Beijing Multi-Site Air Quality](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data) từ UCI và đặt file ZIP tên PRSA2017_Data_20130301-20170228.zip trong thư mục này. Notebook 01: DATA_SOURCE = "uci_zip", STATION = "Aotizhongxin". Code đọc một trạm từ ZIP, giữ tối đa 60 ngày cuối để phù hợp buổi thực hành.

Hãy chạy lại 01 → 02 → 03 sau khi đổi nguồn. Không commit ZIP lớn lên GitHub. Tránh khẳng định thông tin môi trường thực tế từ dữ liệu giả lập.
