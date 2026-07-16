# Đồ Án Trực Quan Hóa Dữ Liệu (Data Visualization) - NYC Airbnb Market Analysis

Báo cáo phân tích và trực quan hóa dữ liệu thị trường lưu trú Airbnb tại New York City (NYC). Dự án được triển khai trên 2 nền tảng song song: **Tableau** (bản thiết kế tĩnh/động) và **Web Dashboard** sử dụng D3.js, Leaflet và HTML/CSS.

---

## 👥 Thành Viên Nhóm & Phân Công Nhiệm Vụ

1. **JakePham23 (MSSV: 22120230)** - Phụ trách Dashboard Chung (Domain Task 1 & 2):
   - **Domain Task 1:** Market Supply & Pricing Distribution (Tổng quan thị trường và cơ cấu phòng).
   - **Domain Task 2:** Geospatial Analysis (Bản đồ phân vùng nhiệt Choropleth Map & Bảng xếp hạng Top 10 khu phố đắt đỏ nhất).
2. **Phạm Tấn Nghĩa** - Phụ trách Dashboard Nam (`index_Nam.html`):
   - Trực quan hóa Mật độ phòng (Density Grid), Treemap phân bổ và Ảnh hưởng của Tiện ích lên giá thuê (Amenity Uplift).
3. **Hoàng Minh Phúc** - Phụ trách Dashboard Phúc (`index_Phuc.html`):
   - Phân tích tương quan định giá và hiệu suất kinh doanh phòng (Borough x Room Type).
4. **Lê Trọng Nghĩa** - Phụ trách Dashboard Lê Nghĩa (index_Nghia.html):
   - Phân tích mật độ phân bổ thị phần.
   - Mức giá trung bình theo vùng 
   - Phân tích tốc độ tăng trưởng reivew theo thời gian
   - Sự tương quan giữa giá thuê và điểm số đánh giá 

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
* Click nút **Dashboard Nam** để xem phân tích Tiện ích & Mật độ phòng.
* Click nút **Dashboard Phúc** để xem phân tích tương quan định giá.

---

## 🛠️ Các Công Cụ Tiền Xử Lý Dữ Liệu (Data Tooling)

Trong thư mục `tool/` chứa các script Python giúp tiền xử lý và trích xuất dữ liệu từ tập dữ liệu thô ban đầu:
* `prepare_dashboard_data.py`: Trích xuất file `listings_dash.csv` cho Dashboard của Phúc.
* `prepare_data_Nam.py`: Tính toán Amenity Uplift, cụm mật độ bản đồ và chèn trực tiếp JSON vào `index_Nam.html`.
* `data_profiling.py`: Chạy phân tích chất lượng dữ liệu thô (Data Profiling).

---

## 📅 Lộ Trình Triển Khai Trọng Tâm (6 Tuần)
- **(Profiling):** Khởi tạo Repo. Thống nhất làm sạch Master Data (Xóa Null, xóa Price <=0, chuẩn hóa ngày tháng `YYYY-MM-DD`). 
- **(Abstraction):** Bám sát dữ liệu sạch, mỗi người định nghĩa Data Type (Categorical, Quantitative...) cho các cột mình dùng.
- **(Task Abstraction):** Mỗi người chốt 2 câu `Action` + `Target` tương ứng với 2 domain task của mình.
- **(Idiom):** Phác thảo biểu đồ. Trưởng nhóm quy định bảng màu chung.
- **(Code & Merge):** Mỗi người tự code file biểu đồ riêng. Cuối tuần đẩy tất cả vào chung 1 file Dashboard.
- **(Evaluation):** Rà soát tốc độ Load, độ thân thiện UI. Tự ráp Word báo cáo & Nộp bài. 
