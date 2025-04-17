import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import threading
import os
import sys
from pathlib import Path

# Kiểm tra xem file video_generator.py có tồn tại không
video_generator_path = os.path.join(os.getcwd(), "video_generator.py")
GENERATOR_FILE_EXISTS = os.path.exists(video_generator_path)

# Kiểm tra thư viện AI cần thiết
AI_LIBRARIES_IMPORTED = False
if GENERATOR_FILE_EXISTS:
    try:
        # Thử import các thư viện cần thiết cho AI
        import torch
        import diffusers
        from video_generator import VideoGenerator
        AI_LIBRARIES_IMPORTED = True
    except ImportError as e:
        print(f"Cảnh báo: Không thể import thư viện AI: {e}")

class VideoGeneratorGUI:
    """Giao diện đồ họa cho Video AI Generator"""
    
    def __init__(self, root):
        """Khởi tạo giao diện"""
        self.root = root
        self.root.title("Video AI Generator")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Đặt style cho giao diện
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        
        # Biến để lưu trạng thái
        self.output_file = tk.StringVar(value=os.path.join(os.getcwd(), "output.mp4"))
        
        # Tạo các thành phần giao diện
        self._create_widgets()
        self._update_options()
        
    def _create_widgets(self):
        """Tạo các thành phần giao diện"""
        # Tiêu đề
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)
        
        ttk.Label(
            header_frame, 
            text="Video AI Generator - Tạo video từ mô tả văn bản", 
            style='Header.TLabel'
        ).pack()
        
        # Khung nhập mô tả
        input_frame = ttk.LabelFrame(self.root, text="Mô tả văn bản", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.text_input = scrolledtext.ScrolledText(
            input_frame, 
            height=5, 
            wrap=tk.WORD, 
            font=('Arial', 11)
        )
        self.text_input.pack(fill=tk.BOTH, expand=True)
        
        # Khung mô tả chế độ
        mode_frame = ttk.LabelFrame(self.root, text="Chế độ tạo video", padding="10")
        mode_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(
            mode_frame, 
            text="Chế độ AI - Sinh video từ mô tả văn bản sử dụng Stable Diffusion", 
            font=('Arial', 10, 'bold')
        ).pack(anchor=tk.W)
        
        # Hiển thị thông báo lỗi nếu không tìm thấy thư viện AI
        if not GENERATOR_FILE_EXISTS:
            ttk.Label(
                mode_frame,
                text="Lỗi: Không tìm thấy file video_generator.py",
                foreground="red"
            ).pack(anchor=tk.W, pady=5)
        elif not AI_LIBRARIES_IMPORTED:
            ttk.Label(
                mode_frame,
                text="Cảnh báo: Thiếu thư viện AI cần thiết. Vui lòng cài đặt với 'pip install -r requirements.txt'",
                foreground="orange"
            ).pack(anchor=tk.W, pady=5)
        
        # Khung tùy chọn
        self.options_frame = ttk.LabelFrame(self.root, text="Tùy chọn", padding="10")
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)
        self._update_options()
        
        # Khung tùy chọn đầu ra
        output_frame = ttk.LabelFrame(self.root, text="Đầu ra", padding="10")
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        output_file_frame = ttk.Frame(output_frame)
        output_file_frame.pack(fill=tk.X)
        
        ttk.Label(output_file_frame, text="File đầu ra:").pack(side=tk.LEFT)
        ttk.Entry(output_file_frame, textvariable=self.output_file, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_file_frame, text="Chọn file...", command=self._select_output_file).pack(side=tk.LEFT)
        
        # Khung trạng thái và log
        log_frame = ttk.LabelFrame(self.root, text="Trạng thái", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=6, 
            wrap=tk.WORD, 
            font=('Courier', 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        # Khung nút
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)
        
        # Tạo style cho nút tạo video nổi bật hơn
        self.style.configure('Generate.TButton', font=('Arial', 12, 'bold'))
        
        # Nút thoát bên trái
        ttk.Button(
            button_frame, 
            text="Thoát", 
            command=self.root.destroy
        ).pack(side=tk.LEFT, padx=10)
        
        # Nút tạo video nổi bật ở giữa
        self.create_button = ttk.Button(
            button_frame, 
            text="TẠO VIDEO",
            style='Generate.TButton',
            command=self._generate_video
        )
        self.create_button.pack(expand=True, pady=10)
        
    def _update_options(self):
        """Hiển thị các tùy chọn cho tạo video AI"""
        # Xóa các tùy chọn hiện tại
        for widget in self.options_frame.winfo_children():
            widget.destroy()
            
        # Tùy chọn cho chế độ AI
        ttk.Label(self.options_frame, text="Số khung hình:").grid(row=0, column=0, sticky=tk.W)
        self.frames_entry = ttk.Spinbox(self.options_frame, from_=1, to=20, width=5)
        self.frames_entry.set(5)
        self.frames_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(self.options_frame, text="Thời gian mỗi khung hình (giây):").grid(row=1, column=0, sticky=tk.W)
        self.frame_duration_entry = ttk.Spinbox(self.options_frame, from_=0.5, to=10, increment=0.5, width=5)
        self.frame_duration_entry.set(2.0)
        self.frame_duration_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(self.options_frame, text="Thời gian chuyển cảnh (giây):").grid(row=2, column=0, sticky=tk.W)
        self.transition_entry = ttk.Spinbox(self.options_frame, from_=0.0, to=5.0, increment=0.1, width=5)
        self.transition_entry.set(1.0)
        self.transition_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(self.options_frame, text="Thiết bị xử lý:").grid(row=3, column=0, sticky=tk.W)
        self.device_var = tk.StringVar(value="cuda" if torch.cuda.is_available() else "cpu")
        device_frame = ttk.Frame(self.options_frame)
        device_frame.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Radiobutton(device_frame, text="CPU", variable=self.device_var, value="cpu").pack(side=tk.LEFT)
        ttk.Radiobutton(device_frame, text="GPU (CUDA)", variable=self.device_var, value="cuda").pack(side=tk.LEFT)
        
        ttk.Label(self.options_frame, text="Độ phân giải:").grid(row=4, column=0, sticky=tk.W)
        resolution_frame = ttk.Frame(self.options_frame)
        resolution_frame.grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)
        
        self.width_entry = ttk.Spinbox(resolution_frame, from_=320, to=1024, width=5)
        self.width_entry.set(512)
        self.width_entry.pack(side=tk.LEFT)
        
        ttk.Label(resolution_frame, text="x").pack(side=tk.LEFT)
        
        self.height_entry = ttk.Spinbox(resolution_frame, from_=240, to=1024, width=5)
        self.height_entry.set(512)
        self.height_entry.pack(side=tk.LEFT)
            
    def _select_output_file(self):
        """Mở hộp thoại chọn file đầu ra"""
        filename = filedialog.asksaveasfilename(
            title="Chọn file đầu ra",
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")],
            initialfile="output.mp4"
        )
        if filename:
            self.output_file.set(filename)
            
    def _log(self, message):
        """Thêm thông báo vào vùng log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
        
    def _generate_video(self):
        """Tạo video theo cấu hình đã chọn"""
        # Kiểm tra đầu vào
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            self._log("Lỗi: Vui lòng nhập mô tả văn bản!")
            return
            
        # Vô hiệu hóa nút tạo video
        self.create_button.config(state="disabled")
                        
        # Bắt đầu tiến trình tạo video
        threading.Thread(target=self._generate_video_thread, daemon=True).start()
    
    def _generate_video_thread(self):
        """Tiến trình tạo video"""
        try:
            text = self.text_input.get("1.0", tk.END).strip()
            output_path = self.output_file.get()
            
            # Đảm bảo thư mục đầu ra tồn tại
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                
            self._log(f"Bắt đầu tạo video từ mô tả: '{text}'")
            self._log(f"File đầu ra: {output_path}")
            
            # Kiểm tra xem file VideoGenerator tồn tại không
            if not GENERATOR_FILE_EXISTS:
                self._log("Lỗi: Không tìm thấy file video_generator.py!")
                return
            
            # Thử import các thư viện AI cần thiết
            try:
                import torch
                import diffusers
                from video_generator import VideoGenerator
            except ImportError as e:
                self._log(f"Lỗi: Thiếu thư viện AI cần thiết: {e}")
                self._log("Vui lòng cài đặt thư viện cần thiết bằng lệnh sau:")
                self._log("pip install diffusers transformers accelerate torch")
                self._log("\nHoặc cài đặt tất cả thư viện:")
                self._log("pip install -r requirements.txt")
                return
                
            # Lấy các tham số
            frames = int(self.frames_entry.get())
            frame_duration = float(self.frame_duration_entry.get())
            transition = float(self.transition_entry.get())
            device = self.device_var.get()
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            resolution = (width, height)
            
            self._log(f"Sử dụng chế độ AI:")
            self._log(f"- Số khung hình: {frames}")
            self._log(f"- Thời gian mỗi khung hình: {frame_duration} giây")
            self._log(f"- Thời gian chuyển cảnh: {transition} giây")
            self._log(f"- Độ phân giải: {width}x{height}")
            self._log(f"- Thiết bị xử lý: {device}")
            
            try:
                # Khởi tạo generator
                self._log("Đang tải mô hình AI...")
                generator = VideoGenerator(device=device)
                
                # Tạo video
                generator.generate_video(
                    text, 
                    output_path=output_path, 
                    num_frames=frames,
                    frame_duration=frame_duration,
                    transition_duration=transition,
                    resolution=resolution
                )
                
                self._log(f"Video đã được tạo thành công và lưu tại: {output_path}")
            except Exception as e:
                self._log(f"Lỗi khi tạo video AI: {e}")
                import traceback
                self._log(traceback.format_exc())
            
        except Exception as e:
            self._log(f"Lỗi: {str(e)}")
            import traceback
            self._log(traceback.format_exc())
        finally:
            # Kích hoạt lại nút tạo video
            self.create_button.config(state="normal")

def main():
    """Hàm chính để khởi động ứng dụng"""
    root = tk.Tk()
    app = VideoGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
