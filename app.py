import os
import argparse # Thêm thư viện argparse
# from PIL import Image # Không cần PIL nữa

# Hàm tạo video chỉ từ văn bản
def generate_video(text, output_path="output.mp4", duration=5, bg_color=(0,0,0), text_color='white', font_size=70, font='Arial', video_size=(1280, 720)):
    """
    Hàm tạo video chỉ từ văn bản với nền màu.
    """
    try:
        print(f"Đang tạo video với văn bản '{text}'...")

        # Tạo nền màu
        background_clip = mpe.ColorClip(size=video_size, color=bg_color, ismask=False, duration=duration)

        # Tạo TextClip từ văn bản
        # Cần chọn font hỗ trợ tiếng Việt, ví dụ 'Arial' nếu có hoặc cần cài đặt font phù hợp
        txt_clip = mpe.TextClip(text, fontsize=font_size, color=text_color, font=font, size=(video_size[0]*0.9, None)) # Chiều rộng text bằng 90% chiều rộng video
        txt_clip = txt_clip.set_position('center').set_duration(duration)

        # Kết hợp nền và văn bản
        video = mpe.CompositeVideoClip([background_clip, txt_clip])

        # Ghi video ra tệp
        video.write_videofile(output_path, fps=24) # fps = frames per second

        print(f"Video đã được lưu tại '{output_path}'")

    except Exception as e:
        print(f"Lỗi khi tạo video: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tạo video từ văn bản.")
    # Bỏ argument --image, chỉ cần --text
    parser.add_argument("--text", required=True, help="Văn bản muốn thêm vào video.")
    parser.add_argument("--output", default="output.mp4", help="Đường dẫn tệp video đầu ra (mặc định: output.mp4).")
    parser.add_argument("--duration", type=int, default=5, help="Thời lượng video (giây, mặc định: 5).")
    # Thêm tùy chọn cho màu nền, màu chữ, kích thước chữ, font, kích thước video nếu muốn tùy chỉnh thêm
    # parser.add_argument("--bgcolor", default="0,0,0", help="Màu nền RGB (vd: 0,0,0 cho đen).")
    # parser.add_argument("--textcolor", default="white", help="Màu chữ.")
    # parser.add_argument("--fontsize", type=int, default=70, help="Kích thước chữ.")
    # parser.add_argument("--font", default="Arial", help="Tên font hoặc đường dẫn tệp font.")
    # parser.add_argument("--size", default="1280x720", help="Kích thước video (vd: 1920x1080).")


    args = parser.parse_args()

    # Gọi hàm tạo video chỉ với văn bản và các tùy chọn khác
    # (Cần xử lý thêm nếu muốn dùng các tùy chọn màu sắc, font, size từ args)
    generate_video(args.text, args.output, duration=args.duration)
