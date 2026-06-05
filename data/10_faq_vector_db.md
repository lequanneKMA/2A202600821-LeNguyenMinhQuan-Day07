# FAQ về Cơ sở dữ liệu Vector (Vector Database)

### Q1: Khái niệm Embedding là gì và tại sao nó quan trọng trong AI?
Embedding (phép nhúng) là quá trình chuyển đổi các đối tượng dữ liệu không cấu trúc như từ ngữ, câu văn, hình ảnh, hoặc âm thanh thành các vector số thực có số chiều cố định (ví dụ: 384, 768, hoặc 1536 chiều).
- Mục đích chính của embedding là chụp lại ngữ nghĩa và mối quan hệ ngữ cảnh của dữ liệu. Các đối tượng có ý nghĩa tương tự nhau sẽ được biểu diễn bởi các vector nằm gần nhau trong không gian nhiều chiều này.
- Ví dụ, vector biểu diễn của từ "vua" và "hoàng hậu" sẽ có khoảng cách rất gần nhau, trong khi khoảng cách giữa "vua" và "quả chuối" sẽ rất xa.
- Đây là nền tảng giúp máy tính có thể so sánh sự tương đồng ngữ nghĩa một cách toán học mà không cần dựa trên việc so khớp từ khóa (keyword matching) thô sơ.

### Q2: Sự khác biệt cơ bản giữa ChromaDB, Pinecone và Milvus là gì?
Các cơ sở dữ liệu vector khác nhau được thiết kế cho các nhu cầu sử dụng và quy mô hệ thống khác nhau:
- **ChromaDB**: Là cơ sở dữ liệu vector mã nguồn mở gọn nhẹ, cực kỳ dễ cài đặt và sử dụng. Nó hỗ trợ lưu trữ hoàn toàn trong bộ nhớ (in-memory) hoặc lưu trữ file cục bộ dưới máy khách. ChromaDB là lựa chọn hoàn hảo cho các dự án phát triển phần mềm thử nghiệm (prototypes), ứng dụng chạy offline, hoặc lưu trữ tập dữ liệu vừa và nhỏ mà không cần hạ tầng máy chủ phức tạp.
- **Pinecone**: Là cơ sở dữ liệu vector dạng dịch vụ đám mây (fully managed SaaS). Pinecone không yêu cầu người dùng phải tự vận hành máy chủ, có khả năng tự động mở rộng (auto-scale) rất tốt và hỗ trợ truy vấn độ trễ thấp ở quy mô lớn. Nhược điểm duy nhất là nó có tính phí dựa trên lượng tài nguyên sử dụng và bắt buộc phải kết nối Internet.
- **Milvus**: Là một hệ thống cơ sở dữ liệu vector phân tán mã nguồn mở, được tối ưu hóa cho hàng tỷ vector ở quy mô doanh nghiệp lớn. Milvus có kiến trúc microservices phức tạp, cho phép mở rộng độc lập các phần đọc/ghi và tài nguyên tính toán. Tuy nhiên, Milvus đòi hỏi cấu hình triển khai hạ tầng rất lớn (thường dùng Kubernetes).

### Q3: Các độ đo tương đồng phổ biến (Similarity Metrics) hoạt động thế nào trong không gian vector?
Khi truy vấn tìm kiếm các vector tương đồng nhất, hệ thống sử dụng các thuật toán đo khoảng cách hình học:
- **Cosine Similarity (Độ tương đồng Cosine)**: Đo góc giữa hai vector mà không quan tâm đến độ dài vật lý của chúng. Công thức là `dot(A, B) / (||A|| * ||B||)`. Giá trị nằm trong khoảng [-1, 1], trong đó 1 nghĩa là hoàn toàn cùng hướng. Độ đo này thường được ưu tiên nhất cho xử lý ngôn ngữ tự nhiên vì độ dài văn bản không làm ảnh hưởng đến độ chính xác ngữ nghĩa.
- **L2 Distance / Euclidean Distance (Khoảng cách L2)**: Đo khoảng cách đường thẳng ngắn nhất nối liền hai đầu mút vector. Công thức là căn bậc hai của tổng bình phương hiệu các chiều. Giá trị bằng 0 nghĩa là hai vector trùng khít hoàn toàn. Càng lớn thì độ tương đồng càng thấp. Độ đo này nhạy cảm với độ dài văn bản.
- **Dot Product / Inner Product (Tích vô hướng)**: Nhân từng thành phần tương ứng của hai vector rồi cộng lại. Nếu các vector đã được chuẩn hóa độ dài về 1 (normalized to unit length), phép tính tích vô hướng sẽ cho kết quả giống hệt như Cosine Similarity nhưng tốc độ tính toán nhanh hơn rất nhiều do không phải chia cho độ dài vector.

### Q4: Phương pháp tạo chỉ mục HNSW và IVF-FLAT giúp tăng tốc truy vấn vector ra sao?
Nếu so khớp một truy vấn với tất cả vector trong cơ sở dữ liệu lớn (quét tuyến tính O(N)), tốc độ tìm kiếm sẽ cực kỳ chậm. Các giải thuật lập chỉ mục ANN (Approximate Nearest Neighbor) ra đời để giải quyết bài toán này:
- **HNSW (Hierarchical Navigable Small World)**: Xây dựng một đồ thị phân cấp nhiều tầng dựa trên lý thuyết thế giới nhỏ. Tầng trên cùng thưa thớt giúp di chuyển nhanh qua các khu vực lớn, tầng dưới cùng chi tiết hơn để tinh chỉnh kết quả gần nhất. HNSW cho tốc độ truy vấn cực nhanh và độ chính xác rất cao, tuy nhiên nó tiêu tốn rất nhiều bộ nhớ RAM để lưu trữ cấu trúc đồ thị.
- **IVF-FLAT (Inverted File Flat)**: Sử dụng thuật toán phân cụm K-Means để gom các vector trong không gian thành K cụm (centroids). Khi có câu hỏi, hệ thống chỉ so sánh khoảng cách với các centroids để chọn ra vài cụm gần nhất, sau đó tìm kiếm chi tiết bên trong các cụm đó. IVF-FLAT tiết kiệm bộ nhớ RAM hơn nhiều so với HNSW nhưng độ chính xác và tốc độ tìm kiếm có thể thấp hơn một chút nếu số lượng cụm phân chia không tối ưu.

### Q5: Tại sao việc kết hợp Metadata Filtering (Lọc siêu dữ liệu) lại quan trọng trong tìm kiếm vector?
Tìm kiếm vector thuần túy đôi khi trả về các kết quả có độ tương đồng toán học cao nhưng không đáp ứng đúng yêu cầu nghiệp vụ thực tế của ứng dụng.
- Ví dụ, khi bạn hỏi "Làm cách nào để kết nối cơ sở dữ liệu?" trong hệ thống tài liệu hỗ trợ của công ty, thuật toán vector có thể trả về tài liệu hướng dẫn cho cả ngôn ngữ Python, Java và C++. Nếu người dùng đang làm việc với dự án Python, các kết quả Java/C++ là vô giá trị.
- Bằng cách gán metadata như `{"language": "python"}` cho các chunk dữ liệu, bạn có thể thực hiện bộ lọc cứng (hard filter) trước hoặc trong quá trình tìm kiếm vector (hybrid search).
- Việc lọc này loại bỏ hoàn toàn các ứng viên không phù hợp về mặt cấu trúc ngữ cảnh nghiệp vụ, giúp cải thiện đáng kể độ chính xác của câu trả lời từ mô hình RAG và tránh làm tràn cửa sổ ngữ cảnh của LLM bằng thông tin rác.
