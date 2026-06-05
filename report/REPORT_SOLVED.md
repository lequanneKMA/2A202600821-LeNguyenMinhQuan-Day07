# Phần Trả Lời Cá Nhân (Tham khảo)

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**
> Hai đoạn văn bản có vector trỏ về cùng một hướng trong không gian đa chiều, nghĩa là chúng mang ý nghĩa hoặc chủ đề tương đồng nhau, bất kể việc sử dụng từ vựng khác nhau hay độ dài ngắn khác biệt.

**Ví dụ HIGH similarity:**
- Sentence A: "Con mèo màu vàng đang nằm ngủ trên thảm."
- Sentence B: "Một chú mèo mướp đang say giấc trên tấm thảm."
- Tại sao tương đồng: Dùng từ ngữ khác nhau (mèo vàng/mèo mướp, nằm ngủ/say giấc) nhưng cùng mô tả một bối cảnh.

**Ví dụ LOW similarity:**
- Sentence A: "Con mèo màu vàng đang nằm ngủ trên thảm."
- Sentence B: "Ngân hàng trung ương vừa tăng lãi suất cơ bản."
- Tại sao khác: Nội dung hoàn toàn không liên quan, một câu về đời sống vật nuôi, một câu về tài chính kinh tế.

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**
> Vì Euclidean đo khoảng cách tuyệt đối nên bị ảnh hưởng lớn bởi độ lớn (magnitude) như độ dài văn bản. Trong khi đó, Cosine chỉ đo góc (angle), giúp nhận diện sự tương đồng ngữ nghĩa dù văn bản dài ngắn khác nhau.

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:* num_chunks = ceil((10000 - 50) / (500 - 50)) = ceil(9950 / 450) = 22.11
> *Đáp án:* 23 chunks.

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**
> *Trả lời:* Nếu overlap = 100 -> ceil((10000 - 100) / (500 - 100)) = ceil(9900 / 400) = 24.75 -> 25 chunks (số chunk tăng lên). 
> *Tại sao:* Overlap lớn giúp giữ trọn vẹn ngữ cảnh (context) ở ranh giới cắt, tránh việc một câu hay một ý quan trọng bị chém đứt đôi khiến mô hình LLM không hiểu được trọn vẹn ý nghĩa.

---

## 3. Chunking Strategy — Cá nhân chọn (15 điểm)

### Baseline Analysis
*(Dựa trên file `python_intro.txt` và hàm Comparator của hệ thống)*

| Tài liệu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|-----------|----------|-------------|------------|-------------------|
| python_intro.txt | FixedSizeChunker (`fixed_size`) | 2 | 200.0 | Thấp (Có thể cắt ngang giữa từ) |
| python_intro.txt | SentenceChunker (`by_sentences`) | 2 | 148.5 | Cao (Nguyên vẹn câu) |
| python_intro.txt | RecursiveChunker (`recursive`) | 2 | 196.5 | Tốt (Cắt theo đoạn/câu nếu có thể) |

### Strategy Của Tôi
**Loại:** RecursiveChunker

**Mô tả cách hoạt động:**
> Strategy này hoạt động dựa trên cơ chế đệ quy tìm điểm cắt ưu tiên. Nó cố gắng cắt văn bản bằng các ký tự ngắt đoạn lớn trước (`\n\n`), nếu đoạn văn vẫn lớn hơn `chunk_size` nó sẽ tiếp tục chẻ nhỏ bằng các ký tự ngắt câu (`. `, `\n`) và cuối cùng là dấu cách. 

**Tại sao tôi chọn strategy này cho domain nhóm?**
> Vì các tài liệu Markdown hoặc Text thường chứa các Paragraph (đoạn văn) dài ngắn không đều. Việc cắt đệ quy giúp hệ thống linh hoạt bảo toàn trọn vẹn một đoạn văn (Paragraph) khi có thể, giúp Agent lấy ngữ cảnh chính xác hơn so với cắt cứng Fixed Size.

---

## 4. My Approach — Cá nhân (10 điểm)

### Chunking Functions

**`SentenceChunker.chunk`** — approach:
> Sử dụng thư viện `re` với regex `(?<=[.!?])\s+|\.\n` để tách ranh giới câu mà không làm mất các dấu chấm/hỏi/than ở cuối. Sau đó dùng vòng lặp gom các câu lại (join) thành từng chunk không vượt quá `max_sentences_per_chunk`.

**`RecursiveChunker.chunk` / `_split`** — approach:
> Hàm đệ quy duyệt qua các separator theo thứ tự ưu tiên (từ `\n\n` đến `\n` đến dấu cách). Tại mỗi mốc, nếu text bị chia vẫn lớn hơn `chunk_size`, nó gọi đệ quy `_split` chính nó với danh sách separator còn lại. Base case: độ dài <= chunk_size, hoặc khi hết separator thì fallback về `FixedSizeChunker` để tránh crash.

### EmbeddingStore

**`add_documents` + `search`** — approach:
> Lưu trữ in-memory bằng list các dictionary chứa `doc_id`, `content`, `metadata` và `embedding`. Khi search, tính tích vô hướng (dot product) giữa query vector và toàn bộ stored vectors, gắn điểm số, sort giảm dần (reverse=True) và cắt lấy `top_k`.

**`search_with_filter` + `delete_document`** — approach:
> Filter bằng cách chạy vòng lặp kiểm tra trước (pre-filtering), nếu mọi key-value trong metadata_filter khớp với doc metadata thì đưa vào list ứng viên, sau đó search trên list này. Delete bằng list comprehension, loại bỏ các record có `doc_id` khớp với ID truyền vào.

### KnowledgeBaseAgent

**`answer`** — approach:
> Agent lấy `top_k` chunk từ store thông qua hàm search. Nối nội dung các chunk lại bằng `\n`. Đắp đoạn chuỗi đó vào format chuẩn: `Context:\n{context}\n\nQuestion: {question}\nAnswer:` rồi truyền vào LLM function để lấy kết quả.

### Test Results

```
===================================================================== test session starts =====================================================================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0 -- /usr/bin/python3
... (42 passed in 0.12s) ...
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED [100%]
===================================================================== 42 passed in 0.12s ======================================================================
```
**Số tests pass:** 42 / 42

---

## 5. Similarity Predictions — Cá nhân (5 điểm)

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score (Mock) | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | "Machine learning is powerful." | "AI is very capable." | High | 0.031 | Sai |
| 2 | "Tôi thích ăn táo." | "Tôi thích ăn trái cây." | High | -0.104 | Sai |
| 3 | "Trời đang mưa to." | "Ngân hàng giảm lãi suất." | Low | 0.088 | Sai |
| 4 | "Màu đỏ là màu ấm." | "Màu đỏ là màu ấm." | High | 1.000 | Đúng |
| 5 | "AI model" | "LLM system" | High | -0.012 | Sai |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**
> Bất ngờ nhất là các câu đồng nghĩa hoàn toàn (Pair 1, 2) nhưng điểm Similarity lại xấp xỉ 0 (thấp hơn cả 2 câu không liên quan ở Pair 3). 
> **Bài học rút ra:** Hệ thống Mock Embedding hiện tại chỉ là "phân băm" (hash) ký tự ngẫu nhiên thành số chứ **không hề có năng lực hiểu ngôn ngữ** (Semantics). Để biểu diễn được ngữ nghĩa thực sự và tính toán độ tương đồng một cách chính xác, bắt buộc phải sử dụng các mô hình học sâu thật sự như OpenAI Text Embedding hay SentenceTransformers.
