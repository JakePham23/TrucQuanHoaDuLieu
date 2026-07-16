# Đồ Án Trực Quan Hóa Dữ Liệu (Data Visualization) - NYC Airbnb Market Analysis

Báo cáo phân tích và trực quan hóa dữ liệu thị trường lưu trú Airbnb tại New York City (NYC). Dự án được triển khai trên 2 nền tảng song song: **Tableau** (bản thiết kế tĩnh/động) và **Web Dashboard** sử dụng D3.js, Leaflet và HTML/CSS.

---

## 👥 Thành Viên Nhóm & Phân Công Nhiệm Vụ

1. **Phạm Tấn Nghĩa (MSSV: 22120230)** - Phụ trách Dashboard Chung (Domain Task 1 & 2):
   - **Domain Task 1:** Market Supply & Pricing Distribution (Tổng quan thị trường và cơ cấu phòng).
   - **Domain Task 2:** Geospatial Analysis (Bản đồ phân vùng nhiệt Choropleth Map & Bảng xếp hạng Top 10 khu phố đắt đỏ nhất).
2. **Lê Trọng Nghĩa (MSSV: 22120226)** - Phụ trách Dashboard Nghĩa (`index_Nghia.html`):
   - Trực quan hóa Mật độ phân bổ, Treemap, Phân tích giá và sự tăng trưởng lượt đánh giá.
3. **Lý Trường Nam (MSSV: 22120218)** - Phụ trách Dashboard Nam (`index_Nam.html`):
   - Trực quan hóa Mật độ phòng (Density Grid), Treemap phân bổ và Ảnh hưởng của Tiện ích lên giá thuê (Amenity Uplift).
4. **Hà Gia Phúc (MSSV: 22120272)** - Phụ trách Dashboard Phúc (`index_Phuc.html`):
   - Phân tích tương quan định giá và hiệu suất kinh doanh phòng (Borough x Room Type).
5. **Nguyễn Minh Tâm (MSSV: 22120321)** - Phụ trách Dashboard Tâm (`index_Tam.html`):
   - Phân tích Giá cả, Nhu cầu (Demand), Cơ cấu Loại phòng (Room Type Structure) và Cường độ Cạnh tranh (Competitive Intensity).

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
