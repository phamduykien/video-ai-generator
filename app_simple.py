import os
import argparse
import numpy as np
import cv2
from PIL import ImageFont, ImageDraw, Image

def create_text_video(text, output_path="output.mp4", duration=5, fps=24, resolution=(1280, 720)):
    """
    Tạo video từ văn bản sử dụng OpenCV
    """
    try:
        print(f"Đang tạo video với văn bản '{text}'...")

        # Thiết lập thông số video
        width, height = resolution
        total_frames = duration * fps
        
        # Tạo đối tượng VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec cho định dạng MP4
        video = cv2.VideoWriter(output_path, fourcc, fps, resolution)
        
        # Đường dẫn font mặc định (Arial cho Windows hoặc DejaVuSans cho Linux)
        font_size = 70
        try:
            # Sử dụng PIL để hỗ trợ tiếng Việt tốt hơn
            font_path = "C:/Windows/Fonts/Arial.ttf"  # Đường dẫn font trên Windows
            if not os.path.exists(font_path):
                font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Đường dẫn trên Linux
        except:
            print("Không tìm thấy font, sử dụng font mặc định")
            font_path = None  # Sẽ dùng font mặc định
            
        # Tạo các khung hình cho video
        for _ in range(total_frames):
            # Tạo một khung hình đen
            frame = np.zeros((height, width, 3), np.uint8)
            
            # Sử dụng PIL để vẽ văn bản tiếng Việt
            pil_img = Image.fromarray(frame)
            draw = ImageDraw.Draw(pil_img)
            
            try:
                # Thử sử dụng font đã chỉ định
                font = ImageFont.truetype(font_path, font_size)
            except:
                # Nếu không có font, sử dụng font mặc định
                font = ImageFont.load_default()
                
            # Tính toán vị trí để đặt text ở giữa
            text_size = draw.textbbox((0, 0), text, font=font)
            text_width = text_size[2] - text_size[0]
            text_height = text_size[3] - text_size[1]
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2
            
            # Vẽ văn bản lên hình ảnh với màu trắng (255,255,255)
            draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))
            
            # Chuyển đổi lại sang định dạng OpenCV
            frame = np.array(pil_img)
            
            # Thêm khung hình vào video
            video.write(frame)
            
        # Giải phóng tài nguyên
        video.release()
        
        print(f"Video đã được tạo và lưu tại '{output_path}'")
        return True
        
    except Exception as e:
        print(f"Lỗi khi tạo video: {e}")
        return False

if __name__ == "__main__":
    # Xử lý tham số dòng lệnh
    parser = argparse.ArgumentParser(description="Tạo video từ văn bản.")
    parser.add_argument("--text", required=True, help="Văn bản muốn thêm vào video.")
    parser.add_argument("--output", default="output.mp4", help="Đường dẫn tệp video đầu ra (mặc định: output.mp4).")
    parser.add_argument("--duration", type=int, default=5, help="Thời lượng video (giây, mặc định: 5).")
    parser.add_argument("--fps", type=int, default=24, help="Số khung hình mỗi giây (mặc định: 24).")
    parser.add_argument("--resolution", default="1280x720", help="Độ phân giải video: chiều rộng x chiều cao (mặc định: 1280x720).")
    
    args = parser.parse_args()
    
    # Parse độ phân giải từ chuỗi "widthxheight"
    try:
        resolution = tuple(map(int, args.resolution.split('x')))
    except:
        print("Lỗi định dạng độ phân giải. Sử dụng mặc định 1280x720.")
        resolution = (1280, 720)
    
    # Tạo video
    create_text_video(args.text, args.output, args.duration, args.fps, resolution)
