# PHẦN BÀI LÀM: PHÂN TÍCH API UPDATE THÔNG TIN SẢN PHẨM

## Phần 1: Phân tích & Đề xuất đa giải pháp

### 1. Phân tích yêu cầu Input / Output

- **Input:**
  - Path parameter: `product_id` (ID của sản phẩm cần sửa, chèn thẳng trên URL).
  - Request body: Một cục JSON chứa thông tin mới: `code` (chuỗi), `name` (chuỗi), `price` (số lớn hơn 0), `stock` (số lớn hơn hoặc bằng 0).
- **Output thành công:** Trả về mã 200 kèm cục dữ liệu JSON của sản phẩm sau khi đã cập nhật thành công.
- **Output thất bại:**
  - Lỗi `404 Not Found` kèm detail `{"detail": "Product not found"}` nếu truyền cái ID không có trong hệ thống.
  - Lỗi `400 Bad Request` kèm detail `{"detail": "Product code already exists"}` nếu mã `code` định sửa lại bị trùng với một sản phẩm khác.
  - Lỗi 422 (Unprocessable Entity) do FastAPI tự bắt nếu tên để rỗng, giá <= 0 hoặc tồn kho < 0.

### 2. Đề xuất tối thiểu 2 giải pháp

- **Giải pháp 1: Duyệt list (Dùng vòng lặp for trên mảng)**
  Dữ liệu gốc `products` đề cho là một cái list. Khi có request update, mình xài vòng lặp `for` quét từ đầu đến cuối list. Quét trúng cái `product_id` thì bợ ra xử lý. Lúc check trùng mã `code`, mình lại lôi mảng ra check xem có cái nào khác ID hiện tại mà cầm cái mã y chang không. Tóm lại là dựa dẫm hoàn toàn vào việc duyệt mảng tuần tự.
- **Giải pháp 2: Dùng dict (Biến list thành dạng Key-Value)**
  Đổi cấu trúc `products` thành một dictionary to đùng, dùng luôn `id` làm key. Ví dụ: `{1: {"code": "SP001", ...}, 2: {"code": "SP002", ...}}`. Khỏi cần lặp gì cho cực, muốn update ID nào chỉ cần bốc `products.get(product_id)` là túm được ngay mục tiêu.

---

## Phần 2: So sánh & Lựa chọn giải pháp

### 1. Lập bảng so sánh các giải pháp

| Tiêu chí             | Giải pháp 1: Duyệt list                                       | Giải pháp 2: Dùng dict                                 |
| :------------------- | :------------------------------------------------------------ | :----------------------------------------------------- |
| **Tốc độ tìm kiếm**  | Chậm hơn, phải lục tìm từng món (Độ phức tạp O(n)).           | Cực nhanh, trỏ phát ăn ngay (Độ phức tạp O(1)).        |
| **Bộ nhớ**           | Tốn ít tài nguyên hơn một chút.                               | Tốn RAM hơn xíu để lưu cái bảng băm (hash table).      |
| **Dễ hiểu**          | Quá quen thuộc với sinh viên, nhắm mắt cũng viết được.        | Hơi lấn cấn lúc đầu nếu chưa quen xài dict lồng nhau.  |
| **Dễ bảo trì**       | Nếu logic phình to, code sẽ lồng nhiều vòng lặp nhìn khá rối. | Gọn gàng hơn, code dễ nhìn, dễ chia tách hàm.          |
| **Bối cảnh phù hợp** | Chữa cháy nhanh, data cứng (mock data) ít ỏi như đề bài.      | Hệ thống lớn hơn, cần lấy thông tin sản phẩm liên tục. |

### 2. Kết luận lựa chọn

Tui chốt **Giải pháp 1: Duyệt list**.
Lý do: Bám sát đúng cái dữ liệu ban đầu đề bài vứt cho (`products = [...]`). Đề cho sao mình xài vậy cho khỏe, đỡ mất công viết thêm hàm chuyển đổi data từ list sang dict. Với lại, đây chỉ là mock data trên memory, chừng vài ba cái item thì duyệt list chạy vẫn dư sức mượt. Lên dự án thực tế xài Database thật thì lúc đó Database tự lo phần tối ưu tốc độ tìm kiếm rồi.
