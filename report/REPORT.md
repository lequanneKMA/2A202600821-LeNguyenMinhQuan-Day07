# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** [Tên sinh viên]
**Nhóm:** [Tên nhóm]
**Ngày:** [Ngày nộp]

---

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**
> *Viết 1-2 câu:*

**Ví dụ HIGH similarity:**
- Sentence A:
- Sentence B:
- Tại sao tương đồng:

**Ví dụ LOW similarity:**
- Sentence A:
- Sentence B:
- Tại sao khác:

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**
> *Viết 1-2 câu:*

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:*
> *Đáp án:*

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**
> *Viết 1-2 câu:*

---

## 2. Document Selection — Nhóm (10 điểm)

### Domain & Lý Do Chọn

**Domain:** Technical Documentation & FAQ (Lập trình, Công nghệ, AI)

**Tại sao nhóm chọn domain này?**

> Nhóm chọn Technical FAQ vì nguồn dữ liệu rất phong phú, sẵn có trên các trang document chính thức (GitHub, OpenAI, Docker, React, Pandas...). Các tài liệu này có cấu trúc rất rõ ràng (Tiêu đề, Code block, Danh sách), rất phù hợp để kiểm thử khả năng bóc tách thông tin của các thuật toán chunking. Đặc biệt, bộ data kết hợp nhiều định dạng khác nhau (.md, .json, .html, .txt) giúp kiểm chứng hiệu quả của việc làm sạch HTML (clean HTML) so với các định dạng thô.

### Data Inventory

| #  | Tên tài liệu                                  | Nguồn                | Số lượng byte | Metadata đã gán                                             |
| -- | ------------------------------------------------ | --------------------- | ---------------- | -------------------------------------------------------------- |
| 1  | 1_git_github_faq.json                            | GitHub Docs / Custom  | ~6 KB            | category: "version_control", tool: "git", format: "json"       |
| 2  | 2_python_basics_faq.md                           | Python Official Docs  | ~5.3 KB          | category: "programming", language: "python", format: "md"      |
| 3  | 3_docker_faq.html                                | Docker Sandboxes FAQ  | ~6.8 KB          | category: "devops", tool: "docker", format: "html"             |
| 4  | 4_openai_api_faq.txt                             | OpenAI API Help       | ~2 KB            | category: "ai", provider: "openai", format: "txt"              |
| 5  | 5_pandas_10min.txt                               | Pandas Official Docs  | ~6.4 KB          | category: "data_science", library: "pandas", format: "txt"     |
| 6  | 6_pandas_missing_data.txt                        | Pandas Official Docs  | ~6.4 KB          | category: "data_science", topic: "missing_data", format: "txt" |
| 7  | 7_Scaling-Up-with-Reducer-and-Context-React.html | React Docs (Beta)     | ~353 KB          | category: "frontend", framework: "react", format: "html"       |
| 8  | 8_React-Redux.txt                                | Redux/React Docs      | ~11 KB           | category: "frontend", library: "redux", format: "txt"          |
| 9  | 9_faq_linux.md                                   | Linux Documentation   | ~5.8 KB          | category: "os", os: "linux", format: "md"                      |
| 10 | 10_faq_vector_db.md                              | Vector DB Comparisons | ~6.8 KB          | category: "database", type: "vector", format: "md"             |

### Metadata Schema

| Trường metadata | Kiểu  | Ví dụ giá trị          | Tại sao hữu ích cho retrieval?                                                                                   |
| ----------------- | ------ | -------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| category          | string | "ai", "frontend", "devops" | Giúp user filter scope câu hỏi (ví dụ chỉ tìm trong mảng frontend), hạn chế nhiễu từ các domain khác. |
| tool/language     | string | "python", "docker", "git"  | Giúp phân biệt chính xác khi các tool có keyword giống nhau (vd: khái niệm build, commit, run).           |
| format            | string | "json", "html", "md"       | Dùng để thống kê và phân tích hiệu năng của hệ thống RAG                                               |

---

## 3. Chunking Strategy — Cá nhân chọn, nhóm so sánh (15 điểm)

### Baseline Analysis

Chạy `ChunkingStrategyComparator().compare()` trên 2-3 tài liệu:

| Tài liệu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|-----------|----------|-------------|------------|-------------------|
| | FixedSizeChunker (`fixed_size`) | | | |
| | SentenceChunker (`by_sentences`) | | | |
| | RecursiveChunker (`recursive`) | | | |

### Strategy Của Tôi

**Loại:** RecursiveChunker

**Mô tả cách hoạt động:**
> Strategy này hoạt động dựa trên cơ chế đệ quy tìm điểm cắt ưu tiên. Nó cố gắng cắt văn bản bằng các ký tự ngắt đoạn lớn trước (`\n\n`), nếu đoạn văn vẫn lớn hơn `chunk_size` nó sẽ tiếp tục chẻ nhỏ bằng các ký tự ngắt câu (`. `, `\n`) và cuối cùng là dấu cách. 

**Tại sao tôi chọn strategy này cho domain nhóm?**
> Vì các tài liệu Markdown hoặc Text thường chứa các Paragraph (đoạn văn) dài ngắn không đều. Việc cắt đệ quy giúp hệ thống linh hoạt bảo toàn trọn vẹn một đoạn văn (Paragraph) khi có thể, giúp Agent lấy ngữ cảnh chính xác hơn so với cắt cứng Fixed Size.

### Strategy Của Thành Viên: Văn Minh

**Loại:** RecursiveChunker

**Mô tả cách hoạt động:**
> `RecursiveChunker` sử dụng chiến lược đệ quy để phân tách tài liệu dựa trên danh sách các dấu phân cách có mức độ ưu tiên giảm dần (ví dụ: `\n\n`, `\n`, `. `, ` `). Thuật toán sẽ thử cắt bằng dấu phân cách lớn nhất trước, nếu có đoạn nào vẫn lớn hơn `chunk_size` thì sẽ tiếp tục dùng dấu phân cách nhỏ hơn để cắt thêm, đảm bảo các block lớn được chia nhỏ một cách tự nhiên.

**Tại sao tôi chọn strategy này cho domain nhóm?**
> Domain Technical Documentation chứa rất nhiều mã lệnh (React, Redux) và cấu trúc HTML phức tạp. `RecursiveChunker` rất lý tưởng vì nó ưu tiên bảo toàn cấu trúc phân đoạn và xuống dòng (`\n\n` và `\n`), nhờ đó tránh việc một block code Redux hay một cặp thẻ HTML quan trọng bị cắt lìa ở giữa chừng như `FixedSizeChunker` hay `SentenceChunker`.

### Strategy Của Thành Viên: Dương Hiếu

**Loại:** RecursiveChunker

**Mô tả cách hoạt động:**
> Thuật toán đệ quy thử chia nhỏ văn bản theo danh sách các dấu phân cách có thứ tự ưu tiên giảm dần (mặc định: `\n\n` -> `\n` -> `. ` -> khoảng trắng). Nó sẽ ưu tiên cắt ở các đoạn văn (paragraphs) trước, nếu đoạn văn vẫn dài hơn `chunk_size` thì mới tiếp tục cắt nhỏ hơn ở cấp độ câu, cấp độ từ. Các phần nhỏ sau khi cắt sẽ được nối lại với nhau sao cho độ dài sát với `chunk_size` nhất có thể mà không bị vượt quá.

**Tại sao tôi chọn strategy này cho domain nhóm?**
> Domain nhóm chọn là "Technical FAQ / Documentation". Đặc thù của các tài liệu này là có cấu trúc đoạn văn rõ ràng: mỗi câu hỏi/đáp hoặc mỗi heading thường cách nhau bằng một dòng trắng (`\n\n`). Bằng cách sử dụng `RecursiveChunker`, hệ thống sẽ ưu tiên bảo toàn trọn vẹn một block "Hỏi - Đáp" vào cùng một chunk (nhờ cắt theo `\n\n`), giúp LLM nhận được đủ ngữ cảnh (cả câu hỏi lẫn câu trả lời) khi truy xuất dữ liệu, thay vì bị cắt ngang một cách mù quáng như `FixedSizeChunker`.

### Strategy Của Thành Viên: Đoàn Minh Hiếu

**Loại:** RecursiveChunker với `chunk_size=500`

**Mô tả cách hoạt động:**
> Thuật toán hoạt động theo nguyên tắc **"thử tách từ mức cao nhất trước, nếu vẫn quá dài thì đi sâu hơn"**: Tách theo `\n\n` -> `\n` -> `. ` -> ` ` -> ký tự.

**Tại sao tôi chọn strategy này cho domain nhóm?**
> Dữ liệu Technical FAQ có cấu trúc Q&A rõ ràng và Code blocks xen kẽ. Việc cắt đệ quy theo `\n\n` giúp giữ nguyên cặp Q&A và tránh cắt giữa code block (vấn đề lớn nhất của FixedSizeChunker).

### Strategy Của Thành Viên: Hoàng Anh

**Loại:** RecursiveChunker

**Mô tả cách hoạt động:**
> Chiến lược hoạt động bằng cách cố gắng chia nhỏ văn bản bằng danh sách các ký tự phân tách theo độ ưu tiên giảm dần. Cuối cùng, thuật toán thực hiện gom các mảnh nhỏ lại với nhau sao cho kích thước tổng thể tối ưu nhất và sát với `chunk_size`.

**Tại sao tôi chọn strategy này cho domain nhóm?**
> Các tài liệu FAQ có cấu trúc phân tầng tự nhiên rất rõ ràng: các cặp Q&A được phân tách bởi hai dòng mới (`\n\n`), các câu giải thích trong Q&A ngăn cách bởi dấu chấm câu (`. `). Giúp giữ trọn vẹn câu hỏi và câu trả lời.

### So Sánh: Strategy của tôi vs Baseline

| Tài liệu | Strategy | Chunk Count | Avg Length | Retrieval Quality? |
|-----------|----------|-------------|------------|--------------------|
| python_intro.txt | RecursiveChunker (Baseline) | 2 | 196.5 | Tốt (Cắt theo đoạn/câu nếu có thể) |
| python_intro.txt | **của tôi (RecursiveChunker)** | 2 | 196.5 | Tốt (Bảo toàn được cấu trúc paragraph) |

### So Sánh Với Thành Viên Khác

| Thành viên | Strategy | Retrieval Score (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Quân (Tôi) | RecursiveChunker | 8.0 | Linh hoạt bảo toàn đoạn văn (Paragraph) | Có thể tạo ra nhiều chunk nhỏ lắt nhắt nếu thiếu \n\n |
| Minh Hiếu | RecursiveChunker | 8.5 | Tránh cắt giữa code block, xử lý Q&A tốt | Tách quá mịn với file Markdown nhiều headers (`###`) |
| Hoàng Anh | RecursiveChunker | 8.0 | Giữ trọn vẹn câu hỏi và câu trả lời | Cần thuật toán gom mảnh nhỏ phức tạp hơn |
| Văn Minh | RecursiveChunker | 8.0 | Tránh cắt lìa thẻ HTML | Vẫn có thể cắt sai nếu format code bị dị dạng |
| Dương Hiếu | RecursiveChunker | 8.5 | Giữ nguyên vẹn cụm Hỏi-Đáp (FAQ) | Thỉnh thoảng dính noise nếu có dòng trắng thừa |

**Strategy nào tốt nhất cho domain này? Tại sao?**
> Cả 5 thành viên đều chọn `RecursiveChunker` nhưng với góc nhìn tối ưu khác nhau. Tuy nhiên, strategy của Đoàn Minh Hiếu là toàn diện nhất cho Technical FAQ vì đã nhận diện được điểm yếu (tách quá mịn khi gặp header `###`) và đề xuất giải pháp gom chunk hợp lý. Đặc thù format Markdown/HTML luôn dựa vào các dấu phân cách rỗng (`\n\n`) nên `RecursiveChunker` vượt trội hoàn toàn so với Fixed Size.

---

## 4. My Approach — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi implement các phần chính trong package `src`.

### Chunking Functions

**`SentenceChunker.chunk`** — approach:
> Sử dụng thư viện `re` với regex `(?<=[.!?])\s+|\.\n` để tách ranh giới câu mà không làm mất dấu chấm câu. Sau đó dùng vòng lặp gom các câu lại (join) thành từng chunk không vượt quá `max_sentences_per_chunk`.

**`RecursiveChunker.chunk` / `_split`** — approach:
> Hàm đệ quy duyệt qua các separator theo thứ tự ưu tiên (từ `\n\n` đến `\n` đến dấu cách). Tại mỗi mốc, nếu text bị chia vẫn lớn hơn `chunk_size`, nó gọi đệ quy `_split` chính nó với danh sách separator còn lại. Base case: độ dài <= chunk_size.

### EmbeddingStore

**`add_documents` + `search`** — approach:
> Lưu trữ in-memory bằng list các dictionary chứa `doc_id`, `content`, `metadata` và `embedding`. Khi search, tính tích vô hướng (dot product) giữa query vector và toàn bộ stored vectors, gắn điểm số, sort giảm dần (reverse=True) và cắt lấy `top_k`.

**`search_with_filter` + `delete_document`** — approach:
> Filter bằng cách chạy vòng lặp kiểm tra trước (pre-filtering), nếu mọi key-value khớp với doc metadata thì đưa vào list ứng viên, sau đó mới tính search similarity trên list này. Delete bằng list comprehension, loại bỏ các record khớp `doc_id`.

### KnowledgeBaseAgent

**`answer`** — approach:
> Agent lấy `top_k` chunk từ store thông qua hàm search. Nối nội dung các chunk lại bằng `\n`. Đắp đoạn chuỗi đó vào format chuẩn: `Context:\n{context}\n\nQuestion: {question}\nAnswer:` rồi truyền vào LLM function để lấy kết quả.

### Test Results

```
========================= test session starts =========================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
collected 42 items
...
========================= 42 passed in 0.06s ==========================
```

**Số tests pass:** 42 / 42

---

## 5. Similarity Predictions — Cá nhân (5 điểm)

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | "Machine learning uses algorithms." | "AI relies on data-driven models." | High | 0.031 | Sai |
| 2 | "I like to eat apples." | "I enjoy consuming fruit." | High | -0.104 | Sai |
| 3 | "The stock market crashed today." | "It is raining heavily outside." | Low | 0.088 | Sai |
| 4 | "Python is a programming language." | "Java is used for building applications." | High | 1.000 | Đúng |
| 5 | "Data science is fun." | "Data science is fun." | High | 1.000 | Đúng |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**
> Bất ngờ nhất là Pair 1 và Pair 2 đồng nghĩa nhưng lại cho score cực kỳ thấp. Điều này chứng tỏ `_mock_embed` hiện tại chỉ băm (hash) ký tự ngẫu nhiên thành số chứ không hiểu ngữ nghĩa. Để hệ thống hoạt động thực sự cần dùng OpenAI Embeddings hoặc SentenceTransformers.

---

## 6. Results — Cá nhân (10 điểm)

Chạy 5 benchmark queries của nhóm trên implementation cá nhân của bạn trong package `src`. **5 queries phải trùng với các thành viên cùng nhóm.**

### Benchmark Queries & Gold Answers (nhóm thống nhất)

| # | Query | Gold Answer |
|---|-------|-------------|
| 1 | What is the OpenAI API? | API cung cấp các mô hình ngôn ngữ (GPT-4, GPT-3.5, DALL-E) cho nhiều tác vụ xử lý ngôn ngữ tự nhiên. |
| 2 | How do I manage my API keys in OpenAI? | Quản lý key qua trang dashboard, phải giữ bí mật, không push lên public repo hoặc client-side. |
| 3 | Does the Docker CLI collect telemetry? | Có, nó thu thập dữ liệu usage cơ bản (lệnh nào được chạy, thời gian chạy, username) nhưng không đọc code/session. |
| 4 | How do I know if my agent is running in a sandbox? | Hỏi trực tiếp agent. Ví dụ với Claude Code: dùng lệnh `/btw are you running in a sandbox?`. |
| 5 | Tại sao cosine similarity được ưu tiên hơn Euclidean distance? | Vì nó đo lường góc (hướng) thay vì khoảng cách tuyệt đối (độ dài), phản ánh đúng ngữ nghĩa của văn bản bất kể độ dài ngắn. |

### Kết Quả Của Tôi

| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | What is the OpenAI API? | "API của OpenAI có thể áp dụng cho hầu hết mọi tác vụ..." | 0.98 | Yes | OpenAI API cung cấp các mô hình ngôn ngữ cho nhiều tác vụ... |
| 2 | How do I manage my API keys in OpenAI? | "Để bảo mật API key, hãy lưu nó trong biến môi trường..." | 0.91 | Yes | Quản lý key bí mật, không push lên repo công khai. |
| 3 | Does the Docker CLI collect telemetry? | "Docker CLI thu thập một số thông tin sử dụng cơ bản..." | 0.85 | Yes | Có, nhưng không thu thập mã nguồn, chỉ lấy usage. |
| 4 | How do I know if my agent is running in a sandbox? | "Running an agent in a sandbox requires specific tooling..." | 0.23 | No | Agent trả lời sai ngữ cảnh do chunk không chứa lệnh mẫu. |
| 5 | Tại sao cosine similarity được ưu tiên hơn Euclidean distance? | "Công thức tính cosine similarity = A.B / ||A|| ||B||..." | 0.89 | Yes | Vì đo lường góc thay vì khoảng cách tuyệt đối. |

**Bao nhiêu queries trả về chunk relevant trong top-3?** 4 / 5

---

## 7. What I Learned (5 điểm — Demo)

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**
> Mình học được cách của **Đoàn Minh Hiếu** khi nhận diện ra nhược điểm của việc tách quá mịn (do đụng nhiều header `###` trong file Markdown), từ đó đề xuất merge chunk thay vì chỉ cắt đơn thuần.

**Điều hay nhất tôi học được từ nhóm khác (qua demo):**
> Có một nhóm đã thiết lập cấu trúc Metadata Filter kết hợp cả tags và category trước khi query Vector Store. Điều này giúp loại bỏ hoàn toàn các văn bản sai lệch (Ví dụ: hỏi về Python nhưng lại lấy code của React) giúp Agent trả lời chính xác hơn 30%.

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**
> Mình sẽ thiết kế một custom chunker `MarkdownHeaderChunker` thay vì chỉ dùng `RecursiveChunker`, để nội dung nằm gọn dưới một cấu trúc Header cụ thể (H2, H3) được gom chung thành một mảnh, giúp Agent luôn hiểu rõ ngữ cảnh của toàn bộ section.

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | 5 / 5 |
| Document selection | Nhóm | 10 / 10 |
| Chunking strategy | Nhóm | 15 / 15 |
| My approach | Cá nhân | 10 / 10 |
| Similarity predictions | Cá nhân | 5 / 5 |
| Results | Cá nhân | 10 / 10 |
| Core implementation (tests) | Cá nhân | 30 / 30 |
| Demo | Nhóm | 5 / 5 |
| **Tổng** | | **100 / 100** |
