# Video AI Generator

Ứng dụng tạo video từ văn bản sử dụng công nghệ AI.

## Giới thiệu

Video AI Generator là ứng dụng Python cho phép tạo video từ mô tả văn bản. Ứng dụng hỗ trợ hai chế độ:

1. **Chế độ văn bản đơn giản:** Tạo video hiển thị văn bản ở trung tâm màn hình với nền đen.
2. **Chế độ AI:** Sử dụng mô hình Stable Diffusion để tạo hình ảnh từ mô tả văn bản, sau đó chuyển đổi thành video với hiệu ứng chuyển cảnh mượt mà.

Ứng dụng hoàn toàn hỗ trợ tiếng Việt và cung cấp giao diện dòng lệnh thân thiện với nhiều tùy chọn tùy chỉnh.

## Tính năng

### Chế độ văn bản đơn giản
- Tạo video hiển thị văn bản tiếng Việt ở trung tâm màn hình
- Tùy chỉnh thời lượng video, FPS, và độ phân giải
- Hỗ trợ font chữ Unicode

### Chế độ AI
- Sinh hình ảnh từ mô tả văn bản sử dụng Stable Diffusion
- Tự động tạo video từ các hình ảnh được sinh
- Thêm hiệu ứng chuyển cảnh mượt mà giữa các hình ảnh
- Tùy chỉnh số lượng hình ảnh, thời gian hiển thị, thời gian chuyển cảnh
- Hỗ trợ tùy chọn seed để tạo kết quả nhất quán

## Cài đặt

### Yêu cầu hệ thống
- Python 3.7 hoặc cao hơn
- Đối với chế độ AI: Khuyến nghị có GPU hỗ trợ CUDA

### Cài đặt thư viện

```bash
# Cài đặt các thư viện cơ bản (cho chế độ văn bản đơn giản)
pip install opencv-python numpy Pillow moviepy

# Cài đặt các thư viện AI (cho chế độ AI)
pip install torch diffusers transformers accelerate
```

Hoặc cài đặt tất cả thư viện bằng file requirements.txt:

```bash
pip install -r requirements.txt
```

## Sử dụng

### Sử dụng giao diện tương tác

```bash
python main.py
```

Ứng dụng sẽ hỏi bạn nhập văn bản và chọn chế độ tạo video.

### Sử dụng dòng lệnh với tham số

#### Chế độ văn bản đơn giản

```bash
python main.py --simple --text "Xin chào từ Video Generator!" --duration 10 --resolution 1920x1080
```

#### Chế độ AI

```bash
python main.py --ai --text "Bãi biển hoàng hôn đẹp ở Đà Nẵng" --frames 8 --frame-duration 3 --transition 1.5
```

### Sử dụng trực tiếp các module

#### Tạo video văn bản đơn giản

```bash
python app_simple.py --text "Xin chào thế giới!" --duration 5 --fps 30 --resolution 1280x720
```

#### Tạo video AI

```bash
python video_generator.py --text "Núi non hùng vĩ ở Việt Nam" --frames 6
```

## Tham số dòng lệnh

### Tham số chung
- `--text`: Văn bản/mô tả để tạo video
- `--output`: Đường dẫn file video đầu ra (mặc định: output.mp4)
- `--simple`: Sử dụng chế độ văn bản đơn giản
- `--ai`: Sử dụng chế độ AI

### Tham số cho chế độ văn bản đơn giản
- `--duration`: Thời lượng video (giây, mặc định: 5)
- `--fps`: Số khung hình mỗi giây (mặc định: 24)
- `--resolution`: Độ phân giải video, định dạng "chiều rộng x chiều cao" (mặc định: 1280x720)

### Tham số cho chế độ AI
- `--frames`: Số lượng khung hình sinh từ AI (mặc định: 5)
- `--frame-duration`: Thời lượng mỗi hình ảnh (giây, mặc định: 2.0)
- `--transition`: Thời gian chuyển cảnh (giây, mặc định: 1.0)
- `--seed`: Giá trị khởi tạo ngẫu nhiên (tùy chọn)
- `--device`: Thiết bị xử lý ('cpu' hoặc 'cuda')
- `--model`: ID mô hình Stable Diffusion (mặc định: stabilityai/stable-diffusion-2-1-base)

## Cấu trúc dự án

```
video-ai-generator/
├── main.py               # Script chính để chạy ứng dụng
├── app.py                # Module tạo video văn bản sử dụng MoviePy
├── app_simple.py         # Module tạo video văn bản đơn giản sử dụng OpenCV
├── video_generator.py    # Module sinh video từ mô tả văn bản sử dụng AI
├── requirements.txt      # Danh sách các thư viện cần thiết
└── README.md             # Tài liệu hướng dẫn
```

## Ví dụ đầu ra

Khi chạy chế độ văn bản đơn giản, ứng dụng sẽ tạo một video hiển thị văn bản được nhập vào ở giữa màn hình với nền đen.

Khi chạy chế độ AI, ứng dụng sẽ sinh các hình ảnh dựa trên mô tả văn bản, sau đó tạo video với hiệu ứng chuyển cảnh giữa các hình ảnh.

## Gỡ lỗi thường gặp

1. **Lỗi ImportError khi import thư viện AI**: Cần cài đặt đầy đủ các thư viện trong requirements.txt
2. **Lỗi CUDA out of memory**: Giảm độ phân giải hình ảnh hoặc sử dụng tham số `--device cpu`
3. **Không hiển thị được tiếng Việt**: Kiểm tra font chữ hỗ trợ Unicode đã được cài đặt

## Giấy phép

Dự án này được phân phối theo giấy phép MIT.
