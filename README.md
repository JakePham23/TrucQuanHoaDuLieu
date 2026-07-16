# Đồ Án Trực Quan Hóa Dữ Liệu (Data Visualization) - NYC Airbnb Market Analysis

Báo cáo phân tích và trực quan hóa dữ liệu thị trường lưu trú Airbnb tại New York City (NYC). Dự án được triển khai trên 2 nền tảng song song: **Tableau** (bản thiết kế tĩnh/động) và **Web Dashboard** sử dụng D3.js, Leaflet và HTML/CSS.

---

## 👥 Thành Viên Nhóm & Phân Công Nhiệm Vụ

1. **JakePham23 (MSSV: 22120230)** - Phụ trách Dashboard Chung (Domain Task 1 & 2):
   - **Domain Task 1:** Market Supply & Pricing Distribution (Tổng quan thị trường và cơ cấu phòng).
   - **Domain Task 2:** Geospatial Analysis (Bản đồ phân vùng nhiệt Choropleth Map & Bảng xếp hạng Top 10 khu phố đắt đỏ nhất).
2. **Phạm Tấn Nghĩa** - Phụ trách Dashboard Nghĩa (`index_Nghia.html`):
   - Trực quan hóa Mật độ phòng (Density Grid), Treemap phân bổ và Ảnh hưởng của Tiện ích lên giá thuê (Amenity Uplift).
3. **Hoàng Minh Phúc** - Phụ trách Dashboard Phúc (`index_Phuc.html`):
   - Phân tích tương quan định giá và hiệu suất kinh doanh phòng (Borough x Room Type).

---

## 🚀 Hướng Dẫn Chạy Dashboard (Local Execution)

Dự án sử dụng Python làm Web Server cục bộ phục vụ các file HTML tĩnh chứa biểu đồ tương tác D3.js.

### Bước 1: Cài đặt thư viện cần thiết
Mở Terminal tại thư mục gốc của dự án và chạy lệnh sau để cài đặt các thư viện tiền xử lý dữ liệu:
```bash
pip install -r requirements.txt
```

### Bước 2: Khởi động Local Server
Chạy file script Server Python:
```bash
python dashboard/app.py
```
*Hệ thống sẽ chạy một HTTP Server tại cổng `8080`.*

### Bước 3: Xem Dashboard tương tác
Mở trình duyệt bất kỳ (Chrome, Brave, Safari...) và truy cập địa chỉ:
👉 **[http://localhost:8080](http://localhost:8080)**

---

## 🔗 Chuyển Đổi Qua Lại Giữa Các Dashboard
Ở thanh đầu trang của mỗi trang web, nhóm đã tích hợp sẵn thanh điều hướng:
* Click nút **Domain Task 1 & 2 (22120230)** để xem Dashboard chính.
* Click nút **Dashboard Nghĩa** để xem phân tích Tiện ích & Mật độ phòng.
* Click nút **Dashboard Phúc** để xem phân tích tương quan định giá.

---
