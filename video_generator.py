import os
import torch
import numpy as np
import argparse
from PIL import Image
from diffusers import StableDiffusionPipeline
from transformers import pipeline
from pathlib import Path

class VideoGenerator:
    """
    Lớp tạo video từ mô tả văn bản sử dụng AI
    """
    def __init__(self, model_id="stabilityai/stable-diffusion-2-1-base", device=None):
        """
        Khởi tạo VideoGenerator
        
        model_id: ID của mô hình Stable Diffusion để sinh hình ảnh
        device: Thiết bị chạy mô hình ('cpu' hoặc 'cuda')
        """
        self.temp_dir = Path("temp_frames")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Xác định thiết bị phù hợp
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        print(f"Đang sử dụng thiết bị: {self.device}")
        
        # Tải mô hình Stable Diffusion để tạo hình ảnh từ văn bản
        print("Đang tải mô hình Stable Diffusion...")
        self.image_generator = StableDiffusionPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )
        self.image_generator = self.image_generator.to(self.device)
        print("Đã tải xong mô hình Stable Diffusion")

    def _generate_images_from_text(self, text, num_frames=5, resolution=(512, 512), seed=None):
        """
        Sinh các hình ảnh từ mô tả văn bản
        
        text: Mô tả văn bản
        num_frames: Số lượng khung hình (hình ảnh) cần sinh
        resolution: Độ phân giải hình ảnh (width, height)
        seed: Giá trị khởi tạo ngẫu nhiên (để sinh kết quả nhất quán)
        """
        print(f"Đang sinh {num_frames} hình ảnh từ văn bản: '{text}'")
        
        images = []
        # Tạo giá trị seed ngẫu nhiên nếu không được cung cấp
        if seed is None:
            seed = np.random.randint(1, 1000000)

        # Sinh hình ảnh với seed khác nhau để có sự khác biệt
        for i in range(num_frames):
            frame_seed = seed + i
            generator = torch.Generator(device=self.device).manual_seed(frame_seed)
            
            # Sinh hình ảnh từ văn bản
            with torch.autocast(self.device):
                image = self.image_generator(
                    text, 
                    generator=generator,
                    height=resolution[1],
                    width=resolution[0]
                ).images[0]
                
            # Lưu hình ảnh tạm thời
            frame_path = self.temp_dir / f"frame_{i:03d}.png"
            image.save(frame_path)
            images.append(str(frame_path))
            
            print(f"Đã sinh hình {i+1}/{num_frames}")
            
        return images

    def _create_video_from_images(self, image_paths, output_path, duration_per_image=2.0, 
                                transition_duration=1.0, fps=24, add_text=True):
        """
        Tạo video từ danh sách đường dẫn hình ảnh
        
        image_paths: Danh sách đường dẫn đến các hình ảnh
        output_path: Đường dẫn file video đầu ra
        duration_per_image: Thời gian hiển thị mỗi hình ảnh (giây)
        transition_duration: Thời gian chuyển cảnh (giây)
        fps: Số khung hình mỗi giây
        add_text: Thêm văn bản gốc vào video hay không
        """
        print(f"Đang tạo video từ {len(image_paths)} hình ảnh...")
        
        import cv2
        
        # Đọc hình ảnh đầu tiên để lấy kích thước
        img = cv2.imread(image_paths[0])
        height, width = img.shape[:2]
        
        # Tạo VideoWriter để ghi video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Định dạng MPEG-4
        video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Biến đổi hình ảnh và thêm vào video với hiệu ứng chuyển cảnh
        for i in range(len(image_paths)):
            # Đọc hình ảnh hiện tại
            img_current = cv2.imread(image_paths[i])
            
            # Thời gian hiển thị hình ảnh (số frame)
            display_frames = int(duration_per_image * fps)
            
            # Nếu có chuyển cảnh và không phải hình cuối cùng
            if transition_duration > 0 and i < len(image_paths) - 1:
                # Đọc hình ảnh tiếp theo cho hiệu ứng chuyển cảnh
                img_next = cv2.imread(image_paths[i + 1])
                
                # Số frame cho hiệu ứng chuyển cảnh
                transition_frames = int(transition_duration * fps)
                
                # Thêm frame hiển thị thông thường (không có hiệu ứng)
                normal_frames = display_frames - transition_frames
                for _ in range(normal_frames):
                    video.write(img_current)
                
                # Thêm frame chuyển cảnh
                for j in range(transition_frames):
                    # Tính alpha cho hiệu ứng (từ 0 đến 1)
                    alpha = j / transition_frames
                    
                    # Tạo hiệu ứng chuyển cảnh
                    blended = cv2.addWeighted(img_current, 1 - alpha, img_next, alpha, 0)
                    
                    # Thêm vào video
                    video.write(blended)
            else:
                # Không có hiệu ứng chuyển cảnh
                for _ in range(display_frames):
                    video.write(img_current)
                    
        # Đóng VideoWriter
        video.release()
        
        # Xóa files tạm
        for img_path in image_paths:
            try:
                os.remove(img_path)
            except:
                pass
                
        print(f"Video đã được lưu tại '{output_path}'")
        
    def generate_video(self, text_description, output_path="output_ai.mp4", num_frames=5, 
                       frame_duration=2.0, transition_duration=1.0, resolution=(512, 512), seed=None):
        """
        Tạo video từ mô tả văn bản
        
        text_description: Mô tả văn bản đầu vào
        output_path: Đường dẫn file video đầu ra
        num_frames: Số lượng khung hình (hình ảnh) cần sinh
        frame_duration: Thời gian hiển thị mỗi hình ảnh (giây)
        transition_duration: Thời gian chuyển cảnh (giây)
        resolution: Độ phân giải hình ảnh (width, height)
        seed: Giá trị khởi tạo ngẫu nhiên (để sinh kết quả nhất quán)
        """
        try:
            # Sinh hình ảnh từ văn bản
            image_paths = self._generate_images_from_text(
                text_description,
                num_frames=num_frames,
                resolution=resolution,
                seed=seed
            )
            
            # Tạo video từ các hình ảnh
            self._create_video_from_images(
                image_paths,
                output_path,
                duration_per_image=frame_duration,
                transition_duration=transition_duration
            )
            
            return True
        except Exception as e:
            print(f"Lỗi khi tạo video: {e}")
            return False

if __name__ == "__main__":
    # Xử lý tham số dòng lệnh
    parser = argparse.ArgumentParser(description="Tạo video từ mô tả văn bản sử dụng AI.")
    parser.add_argument("--text", required=True, help="Mô tả văn bản để sinh video.")
    parser.add_argument("--output", default="output_ai.mp4", help="Đường dẫn tệp video đầu ra.")
    parser.add_argument("--frames", type=int, default=5, help="Số lượng khung hình sinh từ AI.")
    parser.add_argument("--duration", type=float, default=2.0, help="Thời lượng mỗi hình ảnh (giây).")
    parser.add_argument("--transition", type=float, default=1.0, help="Thời gian chuyển cảnh (giây).")
    parser.add_argument("--resolution", default="512x512", help="Độ phân giải hình ảnh: chiều rộng x chiều cao.")
    parser.add_argument("--seed", type=int, help="Giá trị khởi tạo ngẫu nhiên (không bắt buộc).")
    parser.add_argument("--device", choices=["cpu", "cuda"], help="Thiết bị xử lý ('cpu' hoặc 'cuda').")
    
    args = parser.parse_args()
    
    # Parse độ phân giải từ chuỗi "widthxheight"
    try:
        resolution = tuple(map(int, args.resolution.split('x')))
    except:
        print("Lỗi định dạng độ phân giải. Sử dụng mặc định 512x512.")
        resolution = (512, 512)
    
    # Khởi tạo VideoGenerator và tạo video
    generator = VideoGenerator(device=args.device)
    generator.generate_video(
        args.text, 
        output_path=args.output, 
        num_frames=args.frames,
        frame_duration=args.duration,
        transition_duration=args.transition,
        resolution=resolution,
        seed=args.seed
    )
