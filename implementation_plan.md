# Kế Hoạch Thực Hiện Đồ Án Data Visualization (6 Tuần - 5 Người)

**Dựa trên Môn học CSC10108 và nội dung các Slide (Chapter 1 - 6)**

Kế hoạch này được thiết kế để ép tiến độ (6 tuần so với 10 tuần gốc của môn học), phân công song song (parallel) cho 5 thành viên (M1 đến M5). Từng giai đoạn bám sát chặt chẽ các yêu cầu chấm điểm (Data Profiling, Task Abstraction, Idiom Design, Implementation, Evaluation).

## Vai trò đề xuất (Role Assignment)
*   **M1 (Data Lead & Tech Eval):** Phụ trách thu thập, làm sạch dữ liệu, tối ưu hóa hiệu năng kĩ thuật lúc chạy.
*   **M2 (Analyst & Dev - Nhóm 1 & 3):** Phụ trách phân tích Tổng quan thị trường & Xu hướng thời gian.
*   **M3 (Analyst & Dev - Nhóm 2):** Phụ trách phân tích Không gian (Geospatial / Bản đồ).
*   **M4 (Analyst & Dev - Nhóm 4):** Phụ trách phân tích Chất lượng & Phản hồi (Reviews/Correlation).
*   **M5 (UI/UX Lead & Perceptual Eval):** Phụ trách thiết kế khung Dashboard, tính nhất quán (Color, Layout) và đánh giá trải nghiệm.

---

## Chi Tiết Kế Hoạch 6 Tuần

### Tuần 1: Khởi động, Khám phá Dữ liệu & Data Profiling (Dựa theo Chapter 2)
**Mục tiêu:** Nắm bắt dữ liệu thô, phát hiện lỗi, hiểu cấu trúc dữ liệu.
*   **M1:** Tìm dataset (Ví dụ: Inside Airbnb NYC). Thiết lập repo chung (GitHub) và môi trường làm việc. Chạy các tool tự động để xuất báo cáo Data Profiling cơ bản (Null, Duplicate, Outlier).
*   **M2, M3, M4:** Nghiên cứu Chapter 2. Thực hiện *Structure & Content Discovery* trên các file dữ liệu (listings, calendar, reviews). Mỗi người rà soát 1/3 số cột (attributes) quan trọng để báo cáo độ hoàn thiện (Completeness), tính duy nhất (Uniqueness) và ngoại lệ.
*   **M5:** Nghiên cứu bài toán kinh doanh (Domain), tham khảo các mẫu Dashboard tốt, lập dàn ý (Wireframe) sơ bộ để chia zone biểu đồ.

### Tuần 2: Xử lý Dữ liệu & Data Abstraction (Dựa theo Chapter 3)
**Mục tiêu:** Dữ liệu sạch 100% – Định nghĩa rõ ràng Data Type & Dataset Type.
*   **M1:** Chịu trách nhiệm chính code/tool làm sạch dữ liệu (Xử lý Missing data bằng Deletion/Imputation theo Chapter 2). Output ra tập dữ liệu cuối cùng (sạch).
*   **M2, M3, M4:** Dựa trên Chapter 3, định nghĩa *Data Abstraction* cho phần việc của mình:
    *   Xác định Attribute Types (Categorical, Ordinal, Quantitative).
    *   Xác định Direction (Sequential, Diverging).
    *   Định nghĩa Semantics (Key/Value, ý nghĩa thực tế).
*   **M5:** Hỗ trợ M1 trong việc chuẩn hóa các dữ liệu danh mục (Tên khu vực, nhãn). Bắt đầu chọn bộ màu (Color Palette) dự kiến cho Dashboard dựa trên đặc tính Data (Chapter 6).

### Tuần 3: Domain-task & Task Abstraction (Dựa theo Chapter 4)
**Mục tiêu:** Chuyển câu hỏi kinh doanh thành các "Action + Target". (Trọng số 20% điểm đồ án).
*   **Toàn Team:** Họp chốt 4 Cụm Domain-task sử dụng phương pháp *3-Tier Logic Chain* hoặc *User Story Formula*.
*   **M2 (Nhóm 1 & 3):** Viết Task Abstraction cho Tổng quan & Thời gian (VD: `Action: Consume -> Discover; Target: Trends`).
*   **M3 (Nhóm 2):** Viết Task Abstraction cho Không gian (VD: `Action: Search -> Locate; Target: Spatial Distribution`).
*   **M4 (Nhóm 4):** Viết Task Abstraction cho Phản hồi & Chất lượng (VD: `Action: Query -> Compare; Target: Correlation`).
*   **M1, M5:** Review chéo (Cross-review) các định nghĩa Task Abstraction của M2, M3, M4 để đảm bảo logic và khả năng thực thi thực tế trên Dashboard.

### Tuần 4: Idiom Design & Visual Encoding (Dựa theo Chapter 5 & 6)
**Mục tiêu:** Bản vẽ chi tiết các biểu đồ sử dụng đúng Marks, Channels & Color. (Trọng số 20% điểm đồ án).
*   **M2, M3, M4:** Lựa chọn và thiết kế Idiom (Biểu đồ) cho nhiệm vụ của mình. 
    *   Áp dụng *Chapter 5*: Chốt Mark (Point, Line, Area) và Channel (Position, Size, Shape).
    *   Tuân thủ *Chapter 1*: Tối đa hóa *Data-Ink Ratio*, loại bỏ "Chart Junk" & tránh hiệu ứng "Deception" (ví dụ: cấm dùng 3D tùy tiện).
*   **M5:** Rà soát và áp dụng quy tắc *Chapter 6 (Color)*: Sử dụng Categorical Colormaps cho tên quận/quốc gia; Continuous/Diverging cho hiển thị giá/mật độ. Đảm bảo toàn bộ màu sắc là Colorblind-Safe.
*   **M1:** Chuẩn bị các script / view dữ liệu rút gọn (aggregated data) riêng biệt cho từng Idiom để tối ưu tốc độ.

### Tuần 5: Implementation (Dashboard Coding/Building)
**Mục tiêu:** Ráp nối thành Dashboard tương tác hoàn chỉnh. (Trọng số 20% điểm đồ án).
*   **M5 (UI/UX Lead):** Thiết lập hệ thống Layout chung trên công cụ (Tableau / PowerBI / D3.js / Web-based tuỳ nhóm chọn). Thiết lập hệ thống Filter / Slicing toàn cục.
*   **M2:** Code / Kéo ráp các biểu đồ thuộc Tab Tổng quan và Chuỗi thời gian. Ghép nối với Filter chung.
*   **M3:** Code / Kéo ráp bản đồ Geospatial Analysis. Đảm bảo tính năng Zooming và Tooltips trên bản đồ hoạt động trơn tru.
*   **M4:** Code / Kéo ráp các biểu đồ phân tích Tương quan (Scatter plot) và Sentiment dựa trên review.
*   **M1:** Hỗ trợ debug kỹ thuật liên kết dữ liệu, xử lý các lỗi filter không đồng bộ hoặc lỗi trễ dữ liệu (Data latency).

### Tuần 6: Đánh giá (Evaluation) & Hoàn thiện Báo cáo
**Mục tiêu:** Test hệ thống, viết báo cáo giải trình theo chuẩn và làm video trình bày.
*   **M1:** Thực hiện *Technical Evaluation* (10% điểm) – Benchmark thời gian load dữ liệu, kiểm chứng tính đúng đắn khi filter kết hợp (Cross-filtering correctness).
*   **M5:** Thực hiện *Perceptual Evaluation* (10% điểm) – User testing nội bộ, đảm bảo tính dễ hiểu, tính thẩm mỹ.
*   **M2, M3, M4:** Viết file Báo Cáo chi tiết word/pdf cho các mục: Data Profiling, Task Abstraction và Idiom Design của phần mình phụ trách.
*   **Toàn Team:** Góp ý, chỉnh sửa lỗi giao diện cuối cùng và quay Video Demo hệ thống để nộp bài trên Moodle theo yêu cầu.

---

## Các Điểm Cần Chú Ý Trong Khi Làm:
1.  **Dữ liệu thô luôn ẩn chứa sai sót (GIGO):** Đừng bỏ qua khâu Data Profiling ở Tuần 1.
2.  **Sự đa dạng & Tương tác:** Cố gắng đạt ít nhất 4 Idioms khác biệt và phải link Filter (lọc) tương tác chéo giữa các biểu đồ.
3.  **Bám sát lý thuyết:** Báo cáo phải dùng ĐÚNG TỪ KHÓA trong Slide (Ví dụ: Encode, Marks, Channels, Sequential Colormap, Action: Discover, Target: Outliers, v.v.) chứng tỏ có học lý thuyết.
