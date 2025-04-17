"""
Tệp demo minh họa cách sử dụng Video AI Generator trong mã Python
"""
import os
import argparse
from pathlib import Path

# Import các module từ dự án
try:
    from app_simple import create_text_video
    from video_generator import VideoGenerator
except ImportError:
    print("Lỗi: Không thể import các module cần thiết!")
    print("Vui lòng đảm bảo đã cài đặt các thư viện với lệnh: pip install -r requirements.txt")
    exit(1)

def demo_simple_video():
    """Demo chế độ video văn bản đơn giản"""
    print("\n===== DEMO CHẾ ĐỘ VIDEO VĂN BẢN ĐƠN GIẢN =====")
    
    # Tạo thư mục output nếu chưa tồn tại
    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "demo_simple.mp4"
    
    # Tạo video văn bản đơn giản
    print("Đang tạo video văn bản đơn giản...")
    
    text = "Xin chào từ Video Generator!"
    duration = 5  # giây
    fps = 24
    resolution = (1280, 720)
    
    print(f"- Văn bản: {text}")
    print(f"- Thời lượng: {duration} giây")
    print(f"- FPS: {fps}")
    print(f"- Độ phân giải: {resolution[0]}x{resolution[1]}")
    
    result = create_text_video(
        text, 
        str(output_file), 
        duration, 
        fps, 
        resolution
    )
    
    if result:
        print(f"\n✅ Video đã được tạo thành công: {output_file}")
    else:
        print("\n❌ Không thể tạo video!")
        
    return str(output_file) if result else None

def demo_ai_video(device=None):
    """Demo chế độ video AI"""
    try:
        print("\n===== DEMO CHẾ ĐỘ VIDEO AI =====")
        
        # Tạo thư mục output nếu chưa tồn tại
        output_dir = Path("demo_output")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "demo_ai.mp4"
        
        # Tạo video AI
        print("Đang tạo video AI từ mô tả...")
        
        text = "Hoàng hôn trên bãi biển với ánh nắng màu cam phản chiếu trên mặt biển"
        num_frames = 3  # Sử dụng số nhỏ để demo nhanh hơn
        frame_duration = 2.0
        transition = 1.0
        resolution = (512, 512)
        
        print(f"- Mô tả: {text}")
        print(f"- Số khung hình: {num_frames}")
        print(f"- Thời gian mỗi khung hình: {frame_duration} giây")
        print(f"- Thời gian chuyển cảnh: {transition} giây")
        print(f"- Độ phân giải: {resolution[0]}x{resolution[1]}")
        print(f"- Thiết bị: {device if device else 'Tự động chọn'}")
        
        # Khởi tạo generator
        generator = VideoGenerator(device=device)
        
        # Tạo video
        result = generator.generate_video(
            text, 
            output_path=str(output_file), 
            num_frames=num_frames,
            frame_duration=frame_duration,
            transition_duration=transition,
            resolution=resolution
        )
        
        if result:
            print(f"\n✅ Video AI đã được tạo thành công: {output_file}")
        else:
            print("\n❌ Không thể tạo video AI!")
            
        return str(output_file) if result else None
        
    except Exception as e:
        print(f"\n❌ Lỗi khi tạo video AI: {e}")
        print("Chế độ AI có thể yêu cầu cài đặt thêm thư viện: pip install diffusers transformers accelerate torch")
        return None

def run_demo():
    """Chạy demo"""
    parser = argparse.ArgumentParser(description="Demo video generator")
    parser.add_argument("--mode", choices=["simple", "ai", "all"], default="all", 
                       help="Chọn chế độ demo (simple: văn bản đơn giản, ai: trí tuệ nhân tạo, all: cả hai)")
    parser.add_argument("--device", choices=["cpu", "cuda"], help="Thiết bị xử lý cho chế độ AI ('cpu' hoặc 'cuda')")
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("DEMO VIDEO AI GENERATOR")
    print("=" * 50)
    
    simple_output = None
    ai_output = None
    
    if args.mode in ["simple", "all"]:
        simple_output = demo_simple_video()
    
    if args.mode in ["ai", "all"]:
        ai_output = demo_ai_video(args.device)
    
    # Tổng kết
    print("\n" + "=" * 50)
    print("KẾT QUẢ DEMO")
    print("=" * 50)
    
    if simple_output:
        print(f"- Video văn bản đơn giản: {simple_output}")
        
    if ai_output:
        print(f"- Video AI: {ai_output}")
        
    if not simple_output and not ai_output:
        print("❌ Không có video nào được tạo thành công!")
    else:
        print("\n✅ Demo hoàn tất!")
        print("Các file video được lưu trong thư mục 'demo_output'")

if __name__ == "__main__":
    run_demo()
