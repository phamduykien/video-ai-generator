# Hướng dẫn nhanh - Video AI Generator

## Giới thiệu

Video AI Generator là ứng dụng Python cho phép tạo video từ mô tả văn bản với hai chế độ:
1. **Chế độ đơn giản**: Hiển thị văn bản trên nền đen
2. **Chế độ AI**: Sinh hình ảnh từ mô tả văn bản và tạo video có hiệu ứng chuyển cảnh

## Cài đặt

1. Cài đặt các thư viện cần thiết:
   ```
   pip install -r requirements.txt
   ```

2. (Tùy chọn) Nếu chỉ muốn chế độ văn bản đơn giản:
   ```
   pip install opencv-python numpy Pillow moviepy
   ```

## Cách sử dụng nhanh

### 1. Sử dụng giao diện đồ họa (GUI)

Chạy lệnh:
```
python gui.py
```

### 2. Sử dụng giao diện dòng lệnh tương tác

Chạy lệnh:
```
python main.py
```

### 3. Sử dụng dòng lệnh trực tiếp

**Chế độ văn bản đơn giản**:
```
python main.py --simple --text "Xin chào từ Video Generator!" --duration 10
```

**Chế độ AI**:
```
python main.py --ai --text "Bãi biển đẹp ở Đà Nẵng" --frames 5
```

## Các tệp trong dự án

- `main.py`: Giao diện dòng lệnh chính
- `gui.py`: Giao diện đồ họa người dùng 
- `video_generator.py`: Module tạo video sử dụng AI
- `app_simple.py`: Module tạo video văn bản đơn giản
- `app.py`: Module tạo video văn bản phiên bản MoviePy
- `requirements.txt`: Danh sách các thư viện cần thiết
- `README.md`: Tài liệu chi tiết

## Yêu cầu hệ thống

- Python 3.7 trở lên
- Đối với chế độ AI: khuyến nghị GPU hỗ trợ CUDA

## Gỡ lỗi thường gặp

1. Nếu gặp lỗi khi sử dụng chế độ AI, hãy thử chỉ định sử dụng CPU:
   ```
   python main.py --ai --text "Mô tả" --device cpu
   ```

2. Nếu gặp lỗi "Không tải được mô hình Stable Diffusion", hãy kiểm tra kết nối internet và cài đặt thư viện:
   ```
   pip install diffusers transformers accelerate torch
   ```

3. Để xem tất cả các tùy chọn có sẵn:
   ```
   python main.py --help
   ```

## Ví dụ câu mô tả hay

1. "Hoàng hôn trên bãi biển Đà Nẵng với ánh nắng màu cam phản chiếu trên mặt biển"
2. "Núi non hùng vĩ ở Sapa trong ánh bình minh, có sương mù bao phủ thung lũng"
3. "Phố cổ Hội An về đêm với ánh sáng đèn lồng đủ màu sắc phản chiếu xuống sông"
4. "Ruộng bậc thang ở Mù Cang Chải mùa lúa chín vàng rực rỡ"
5. "Chợ nổi miền Tây Nam Bộ với nhiều ghe thuyền đầy hoa quả và hàng hóa"
