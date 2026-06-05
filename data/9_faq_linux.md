# FAQ về Dòng lệnh Linux (Linux Command Line)

### Q1: Làm thế nào để thay đổi quyền truy cập của một tệp tin bằng lệnh chmod?
Trong hệ điều hành Linux, quyền truy cập tệp tin được biểu diễn bởi ba nhóm người dùng: Owner (chủ sở hữu), Group (nhóm người dùng), và Others (người dùng khác). Mỗi nhóm có ba loại quyền cơ bản: Read (đọc - ký hiệu r, giá trị 4), Write (ghi - ký hiệu w, giá trị 2), và Execute (thực thi - ký hiệu x, giá trị 1).
Khi sử dụng lệnh `chmod` với hệ số bát phân (octal mode):
- Lệnh `chmod 755 filename` sẽ gán quyền đầy đủ (rwx = 7) cho Owner, quyền đọc và thực thi (r-x = 5) cho Group và Others. Đây là quyền phổ biến cho các thư mục công cộng hoặc tệp tin script.
- Lệnh `chmod 644 filename` sẽ gán quyền đọc ghi (rw- = 6) cho Owner, quyền chỉ đọc (r-- = 4) cho Group và Others. Quyền này thường dùng cho các tệp tin cấu hình hoặc mã nguồn thông thường.
- Lệnh `chmod +x filename` là cách gán nhanh quyền thực thi cho cả ba nhóm người dùng mà không cần tính toán giá trị số.

### Q2: Làm sao để tìm kiếm một chuỗi văn bản cụ thể bên trong các tệp tin bằng lệnh grep?
Lệnh `grep` (Global Regular Expression Print) là công cụ cực kỳ mạnh mẽ để tìm kiếm văn bản trong Linux.
- Cú pháp cơ bản: `grep "chuỗi_tìm_kiếm" filename` sẽ in ra tất cả các dòng chứa chuỗi đó trong tệp tin cụ thể.
- Để tìm kiếm không phân biệt chữ hoa chữ thường, sử dụng cờ `-i`: `grep -i "python" main.py`.
- Để tìm kiếm đệ quy trong tất cả các tệp tin thuộc thư mục hiện tại và các thư mục con, sử dụng cờ `-r` hoặc `-R`: `grep -r "TODO" ./src`.
- Nếu bạn chỉ muốn hiển thị tên của các tệp tin chứa chuỗi tìm kiếm thay vì in ra toàn bộ nội dung dòng, hãy thêm cờ `-l`: `grep -rl "database_url" .`.
- Để đếm số dòng khớp với kết quả tìm kiếm, sử dụng cờ `-c`: `grep -c "Error" server.log`.

### Q3: Sự khác biệt giữa lệnh top và htop khi theo dõi tiến trình hệ thống là gì?
Cả hai lệnh `top` và `htop` đều dùng để giám sát tài nguyên hệ thống (CPU, RAM, Swap) và quản lý các tiến trình (processes) đang chạy trong thời gian thực. Tuy nhiên chúng có một số điểm khác biệt lớn:
- Lệnh `top` là công cụ mặc định có sẵn trên hầu hết các bản phân phối Linux. Giao diện của `top` khá đơn giản, đơn sắc và khó tương tác trực tiếp bằng chuột hay phím tắt điều hướng.
- Lệnh `htop` là phiên bản nâng cấp đồ họa chạy trong terminal (CLI). Nó cung cấp biểu đồ thanh trực quan nhiều màu sắc hiển thị tải CPU trên từng luồng/nhân, mức sử dụng bộ nhớ RAM và Swap. `htop` hỗ trợ cuộn dọc/ngang mượt mà, cho phép tìm kiếm tiến trình nhanh bằng phím `/`, sắp xếp tiến trình theo các cột tài nguyên chỉ bằng vài phím tắt, và gửi tín hiệu tắt tiến trình (`kill signal`) trực tiếp từ giao diện mà không cần gõ lệnh thủ công.

### Q4: Làm thế nào để tìm kiếm tệp tin dựa trên tên, kích thước hoặc thời gian sửa đổi bằng lệnh find?
Lệnh `find` được sử dụng để quét qua cây thư mục và lọc ra các tệp tin thỏa mãn những tiêu chí phức tạp:
- Tìm kiếm theo tên tệp tin (hỗ trợ wildcard): `find . -name "*.log"` sẽ quét toàn bộ thư mục hiện tại và tìm các tệp tin có đuôi là `.log`.
- Tìm kiếm không phân biệt chữ hoa chữ thường trong tên: `find /var/log -iname "*nginx*"`.
- Tìm kiếm theo loại tệp tin (chỉ tìm file hoặc chỉ tìm thư mục): Sử dụng cờ `-type`. Ví dụ `find . -type d -name "config"` để tìm thư mục tên config.
- Tìm kiếm theo kích thước tệp tin: Sử dụng cờ `-size`. Ví dụ `find . -type f -size +100M` để tìm các tệp tin lớn hơn 100 Megabytes.
- Tìm kiếm theo thời gian sửa đổi: Sử dụng cờ `-mtime` (tính theo ngày) hoặc `-mmin` (tính theo phút). Ví dụ `find . -mtime -7` để tìm các file đã bị thay đổi trong vòng 7 ngày qua.

### Q5: Làm thế nào để điều hướng dòng vào/ra chuẩn (I/O Redirection) trong terminal Linux?
Trong Linux, mỗi chương trình khi chạy đều mở ba luồng dữ liệu chuẩn: dòng vào chuẩn (stdin - đầu vào phím, giá trị 0), dòng ra chuẩn (stdout - hiển thị màn hình, giá trị 1), và dòng báo lỗi chuẩn (stderr - hiển thị lỗi màn hình, giá trị 2).
Bạn có thể chuyển hướng các luồng này bằng các ký tự đặc biệt:
- Ký tự `>`: Chuyển hướng stdout của một lệnh và ghi đè vào file. Ví dụ: `echo "Hello" > file.txt`.
- Ký tự `>>`: Chuyển hướng stdout và ghi nối tiếp vào cuối file mà không xóa nội dung cũ. Ví dụ: `date >> log.txt`.
- Ký tự `<`: Nhận đầu vào stdin từ nội dung một tệp tin thay vì bàn phím. Ví dụ: `mysql -u root db_name < backup.sql`.
- Chuyển hướng lỗi stderr: Sử dụng ký hiệu `2>`. Ví dụ `python script.py 2> error.log` sẽ ghi tất cả các lỗi runtime vào file error.log và không hiển thị trên màn hình.
- Ký hiệu toán tử Pipe `|`: Lấy đầu ra stdout của chương trình phía trước làm đầu vào stdin cho chương trình phía sau. Ví dụ: `cat server.log | grep "Critical"`.
