---
category: "programming"
difficulty: "beginner"
tags: ["python", "basics", "faq", "syntax", "functions"]
---

# Python Basics FAQ

Tài liệu này tổng hợp các câu hỏi và giải đáp chi tiết về các khái niệm cơ bản nhất trong Python. Rất hữu ích cho những người mới bắt đầu làm quen với ngôn ngữ lập trình này.

---

## 1. Các Câu Hỏi Về Kiểu Dữ Liệu (Data Types)

### Q: Python có những kiểu dữ liệu cơ bản nào?
**A:** Python có các nhóm kiểu dữ liệu chính sau:
- **Kiểu số (Numeric Types):** 
  - `int`: Số nguyên (ví dụ: `10`, `-3`).
  - `float`: Số thực (ví dụ: `3.14`, `-0.001`).
  - `complex`: Số phức (ví dụ: `3 + 4j`).
- **Kiểu văn bản (Text Type):** `str` (chuỗi ký tự, ví dụ: `"Hello World"`).
- **Kiểu logic (Boolean Type):** `bool` (`True` hoặc `False`).
- **Kiểu tập hợp dữ liệu (Sequence Types):**
  - `list`: Danh sách có thể thay đổi (Mutable) (ví dụ: `[1, 2, "a"]`).
  - `tuple`: Danh sách không thể thay đổi (Immutable) sau khi khởi tạo (ví dụ: `(1, 2, "a")`).
- **Kiểu ánh xạ (Mapping Type):** `dict` (Từ điển, lưu trữ dưới dạng key-value, ví dụ: `{"name": "Alice", "age": 25}`).

### Q: Sự khác biệt giữa `list` và `tuple` là gì?
**A:** 
Sự khác biệt lớn nhất nằm ở tính **Mutability** (khả năng thay đổi nội dung):
- **List:** Có thể thêm, sửa, xóa phần tử sau khi đã tạo ra (`mutable`). Ký hiệu bằng ngoặc vuông `[]`.
- **Tuple:** **Không thể** thay đổi nội dung sau khi khởi tạo (`immutable`). Tốc độ duyệt qua tuple nhanh hơn list. Ký hiệu bằng ngoặc tròn `()`.

### Q: Làm thế nào để kiểm tra kiểu dữ liệu của một biến?
**A:** Bạn sử dụng hàm `type()`.
```python
x = 10
print(type(x))  # <class 'int'>
```

---

## 2. Các Câu Hỏi Về Vòng Lặp (Loops)

### Q: Khi nào nên sử dụng vòng lặp `for`, khi nào nên sử dụng `while`?
**A:**
- **Vòng lặp `for`:** Thường được sử dụng khi bạn **đã biết trước số lần lặp** hoặc cần duyệt qua các phần tử của một tập hợp (list, tuple, dictionary, string).
  ```python
  for item in [1, 2, 3]:
      print(item)
  ```
- **Vòng lặp `while`:** Thường được sử dụng khi bạn **chưa biết trước số vòng lặp**, mà điều kiện dừng lại phụ thuộc vào một trạng thái nào đó. Vòng lặp sẽ tiếp tục chạy chừng nào điều kiện còn trả về `True`.
  ```python
  count = 0
  while count < 3:
      print(count)
      count += 1
  ```

### Q: Công dụng của `break` và `continue` trong vòng lặp?
**A:**
- **`break`:** Dừng vòng lặp **ngay lập tức** và thoát ra khỏi thân vòng lặp, bất kể điều kiện lặp có còn đúng hay không.
- **`continue`:** Bỏ qua các đoạn code phía dưới trong chu trình lặp hiện tại và lập tức **chuyển sang lần lặp tiếp theo**.

---

## 3. Các Câu Hỏi Về Hàm (Functions)

### Q: Cách định nghĩa và gọi hàm trong Python?
**A:** Bạn sử dụng từ khóa `def` để định nghĩa một hàm.
```python
# Định nghĩa hàm
def greet(name):
    return f"Hello, {name}!"

# Gọi hàm
message = greet("Alice")
print(message)  # In ra: Hello, Alice!
```

### Q: Sự khác biệt giữa tham số mặc định (Default arguments) và `*args`, `**kwargs`?
**A:**
- **Tham số mặc định:** Bạn gán sẵn giá trị cho tham số. Nếu người gọi không truyền vào, biến sẽ lấy giá trị mặc định.
  ```python
  def say_hello(name="Guest"): ...
  ```
- **`*args`:** Cho phép hàm nhận một số lượng tham số vô hạn dưới dạng vị trí (Positional arguments). Trong hàm, `args` là một tuple.
- **`**kwargs`:** Cho phép hàm nhận tham số vô hạn dưới dạng từ khóa (Keyword arguments). Trong hàm, `kwargs` là một dictionary.

---

## 4. Các Lỗi Cú Pháp Cơ Bản (Syntax & Common Errors)

### Q: Tại sao Python báo lỗi `IndentationError`?
**A:** Không giống như C++ hay Java dùng cặp ngoặc nhọn `{}` để nhóm các khối lệnh, Python sử dụng **khoảng trắng (indentation)**. Lỗi này xuất hiện khi bạn thụt lề thụt lùi không đồng nhất (ví dụ: dòng thì dùng 4 dấu cách, dòng thì dùng tab, hoặc không thụt lề cho lệnh bên trong `if`/`for`/`def`).
**Cách sửa:** Đảm bảo sử dụng đồng nhất 4 dấu cách (Space) cho mỗi cấp thụt lề.

### Q: Lỗi `SyntaxError: invalid syntax` thường xuất phát từ đâu?
**A:** Lỗi này xảy ra khi trình biên dịch không thể hiểu dòng code. Các nguyên nhân phổ biến nhất:
- Quên dấu hai chấm `:` ở cuối dòng định nghĩa `if`, `for`, `while`, `def`.
- Quên đóng ngoặc đơn `)`, ngoặc vuông `]` hoặc ngoặc nhọn `}`.
- Viết sai tên từ khóa (ví dụ: viết `Tru` thay vì `True`).

### Q: Làm sao để xử lý ngoại lệ (Exception) để chương trình không bị crash đột ngột?
**A:** Sử dụng khối lệnh `try...except`.
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Lỗi: Không thể chia cho 0!")
```
