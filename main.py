import argparse
import os
from pathlib import Path

# Import module video generator AI
try:
    from video_generator import VideoGenerator
except ImportError:
    print("Lỗi: Không thể tải thư viện video_generator. Vui lòng kiểm tra cài đặt.")
    exit(1)

def print_banner():
    """In banner cho ứng dụng"""
    banner = """
    ╔═══════════════════════════════════════════════════╗
    ║                                                   ║
    ║     VIDEO AI GENERATOR - Sinh video từ văn bản    ║
    ║                                                   ║
    ╚═══════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Hàm chính của ứng dụng"""
    print_banner()
    
    # Tạo parser cho tham số dòng lệnh
    parser = argparse.ArgumentParser(description="Ứng dụng sinh video AI từ mô tả văn bản.")
    
    # Các tham số chung
    parser.add_argument("--text", help="Mô tả văn bản để tạo video.")
    parser.add_argument("--output", default="output.mp4", help="Đường dẫn file video đầu ra.")
    parser.add_argument("--resolution", default="512x512", help="Độ phân giải video (chiều rộng x chiều cao).")
    
    # Các tham số cho AI video generator
    parser.add_argument("--frames", type=int, default=5, help="Số lượng khung hình sinh từ AI.")
    parser.add_argument("--frame-duration", type=float, default=2.0, help="Thời lượng mỗi hình ảnh (giây).")
    parser.add_argument("--transition", type=float, default=1.0, help="Thời gian chuyển cảnh (giây).")
    parser.add_argument("--seed", type=int, help="Giá trị khởi tạo ngẫu nhiên (tùy chọn).")
    parser.add_argument("--device", choices=["cpu", "cuda"], help="Thiết bị xử lý ('cpu' hoặc 'cuda').")
    parser.add_argument("--model", default="stabilityai/stable-diffusion-2-1-base", 
                       help="ID mô hình Stable Diffusion (mặc định: stabilityai/stable-diffusion-2-1-base).")
    
    args = parser.parse_args()
    
    # Nếu không có văn bản đầu vào, hỏi người dùng
    if not args.text:
        args.text = input("Nhập mô tả văn bản để tạo video: ")
    
    # Thông báo về chế độ video AI
    print("\nỨng dụng Video AI Generator sử dụng Stable Diffusion để sinh video từ mô tả văn bản")
    
    # Đảm bảo đường dẫn đầu ra hợp lệ
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Parse độ phân giải từ chuỗi "widthxheight"
    try:
        resolution = tuple(map(int, args.resolution.split('x')))
    except:
        print("Lỗi định dạng độ phân giải. Sử dụng mặc định 512x512.")
        resolution = (512, 512)
    
    print(f"\nBắt đầu tạo video AI từ mô tả: '{args.text}'")
    print(f"- Số khung hình: {args.frames}")
    print(f"- Thời gian mỗi khung hình: {args.frame_duration} giây")
    print(f"- Thời gian chuyển cảnh: {args.transition} giây")
    print(f"- Độ phân giải: {resolution[0]}x{resolution[1]}")
    print(f"- File đầu ra: {args.output}")
    
    # Khởi tạo và chạy VideoGenerator
    generator = VideoGenerator(model_id=args.model, device=args.device)
    success = generator.generate_video(
        args.text, 
        output_path=args.output, 
        num_frames=args.frames,
        frame_duration=args.frame_duration,
        transition_duration=args.transition,
        resolution=resolution,
        seed=args.seed
    )
    
    if success:
        print(f"\n✅ Đã tạo xong video AI! File đã được lưu tại: {args.output}")
    else:
        print(f"\n❌ Không thể tạo video AI. Vui lòng kiểm tra log lỗi.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nĐã hủy quá trình tạo video.")
    except Exception as e:
        print(f"\n❌ Đã xảy ra lỗi: {e}")
