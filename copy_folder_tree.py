"""  This is to copy the folder structure without files """

import shutil
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox


def get_base_path():
    """Lấy đường dẫn gốc của thư mục chứa ứng dụng, hỗ trợ cả khi chạy từ script và từ exe"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def copy_tree(src, dest, merge_existing, log_callback):
    """Copies source folder structure to destination folder without files
    and reports progress via log_callback.
    """
    try:
        if os.path.exists(dest) and not merge_existing:
            return False, "Thư mục đích đã tồn tại (Bạn chưa chọn Gộp cấu trúc)."
            
        if not os.path.exists(dest):
            os.makedirs(dest)
            log_callback(f"Tạo: {dest}")
        else:
            log_callback(f"Gộp vào: {dest}")

        count = 0
        for root_dir, dirs, files in os.walk(src):
            rel_path = os.path.relpath(root_dir, src)
            if rel_path == '.':
                continue # Đã xử lý thư mục gốc ở trên

            target_dir = os.path.join(dest, rel_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
                log_callback(f"Tạo: {target_dir}")
                count += 1
            else:
                log_callback(f"Bỏ qua (đã có): {target_dir}")
        
        return True, f"Hoàn tất. Đã tạo mới {count} thư mục con."
    except Exception as e:
        return False, str(e)


def run_gui():
    root = tk.Tk()
    root.title("Sao chép Cây Thư mục - v1.0.0 (04/05/2026) - TS. NGUYỄN HỒ BẮC")
    root.geometry("600x500")
    root.resizable(False, False)

    try:
        root.iconbitmap(os.path.join(get_base_path(), 'icon.ico'))
    except Exception:
        pass

    # Khung chứa cho Thư mục Nguồn
    frame_src = tk.Frame(root)
    frame_src.pack(pady=10, padx=10, fill='x')
    tk.Label(frame_src, text="Thư mục nguồn:", width=15, anchor='w').pack(side=tk.LEFT)
    src_var = tk.StringVar()
    tk.Entry(frame_src, textvariable=src_var, width=50).pack(side=tk.LEFT, padx=5)
    
    def browse_src():
        folder = filedialog.askdirectory(title="Chọn thư mục nguồn")
        if folder:
            src_var.set(folder)
            
    tk.Button(frame_src, text="Chọn...", command=browse_src).pack(side=tk.LEFT)

    # Khung chứa cho Thư mục Đích
    frame_dest = tk.Frame(root)
    frame_dest.pack(pady=5, padx=10, fill='x')
    tk.Label(frame_dest, text="Thư mục đích:", width=15, anchor='w').pack(side=tk.LEFT)
    dest_var = tk.StringVar()
    tk.Entry(frame_dest, textvariable=dest_var, width=50).pack(side=tk.LEFT, padx=5)

    def browse_dest():
        folder = filedialog.askdirectory(title="Chọn thư mục đích")
        if folder:
            dest_var.set(folder)
            
    tk.Button(frame_dest, text="Chọn...", command=browse_dest).pack(side=tk.LEFT)

    # Checkbox Gộp thư mục
    merge_existing_var = tk.BooleanVar(value=True)
    tk.Checkbutton(root, text="Gộp cấu trúc nếu thư mục đã tồn tại (Không xóa / không chép đè)", variable=merge_existing_var).pack(pady=5)

    # Log Box
    frame_log = tk.Frame(root)
    frame_log.pack(pady=5, padx=15, fill='both', expand=True)
    
    scrollbar = tk.Scrollbar(frame_log)
    scrollbar.pack(side=tk.RIGHT, fill='y')
    
    log_text = tk.Text(frame_log, height=12, yscrollcommand=scrollbar.set, state=tk.DISABLED, bg='#f9f9f9', fg='#333', font=('Consolas', 9))
    log_text.pack(side=tk.LEFT, fill='both', expand=True)
    scrollbar.config(command=log_text.yview)

    def log_message(msg):
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, msg + "\n")
        log_text.see(tk.END)
        log_text.config(state=tk.DISABLED)
        root.update_idletasks() # Cập nhật UI ngay lập tức

    # Nút Thực hiện
    def start_copy():
        log_text.config(state=tk.NORMAL)
        log_text.delete(1.0, tk.END)
        log_text.config(state=tk.DISABLED)

        src = src_var.get().strip()
        dest = dest_var.get().strip()
        
        if not src or not dest:
            log_message("⚠️ CẢNH BÁO: Vui lòng chọn đầy đủ thư mục nguồn và đích!")
            return
            
        src_abs = os.path.abspath(src)
        dest_abs = os.path.abspath(dest)

        # Lấy tên thư mục nguồn để tạo thành thư mục con trong đích
        src_folder_name = os.path.basename(src_abs)
        if not src_folder_name:
            # Xử lý trường hợp src là thư mục gốc của ổ đĩa (vd: 'C:\')
            src_folder_name = src_abs.replace(':', '').replace('\\', '').replace('/', '') + "_copy"

        actual_dest = os.path.join(dest_abs, src_folder_name)

        if src_abs == actual_dest or src_abs == dest_abs:
            log_message("⚠️ LỖI: Thư mục nguồn và thư mục đích không được trùng nhau!")
            return
            
        if not os.path.exists(src):
            log_message(f"⚠️ LỖI: Thư mục nguồn không tồn tại:\n{src}")
            return
            
        # Tránh trường hợp thư mục đích nằm trong thư mục nguồn (gây lặp vô hạn)
        try:
            if os.path.commonpath([src_abs, actual_dest]) == src_abs:
                log_message("⚠️ LỖI: Thư mục đích không được nằm bên trong thư mục nguồn!")
                return
        except ValueError:
            pass # Hai đường dẫn nằm ở hai ổ đĩa khác nhau

        log_message("⏳ BẮT ĐẦU SAO CHÉP...\n" + "-"*40)
        try:
            success, msg = copy_tree(src_abs, actual_dest, merge_existing_var.get(), log_message)
            log_message("-" * 40)
            if success:
                log_message(f"✅ {msg}")
                log_message(f"✅ Đường dẫn lưu trữ: {actual_dest}")
            else:
                log_message(f"❌ LỖI: {msg}")
        except Exception as e:
            log_message(f"❌ LỖI KHÔNG XÁC ĐỊNH: {str(e)}")

    # Khung chứa các nút bấm
    frame_buttons = tk.Frame(root)
    frame_buttons.pack(pady=10)

    def show_help():
        readme_path = os.path.join(get_base_path(), 'README.md')
        try:
            os.startfile(readme_path)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở file trợ giúp: {e}")

    def open_dest_folder():
        dest = dest_var.get().strip()
        if not dest or not os.path.exists(dest):
            messagebox.showwarning("Cảnh báo", "Thư mục đích chưa được chọn hoặc không tồn tại!")
            return
        try:
            os.startfile(dest)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở thư mục đích: {e}")

    tk.Button(frame_buttons, text="Trợ giúp", command=show_help, width=10, height=2, bg='#17a2b8', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="Mở Đích", command=open_dest_folder, width=10, height=2, bg='#ffc107', fg='black', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="Thực hiện sao chép", command=start_copy, width=18, height=2, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="Thoát", command=root.destroy, width=10, height=2, bg='#dc3545', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == '__main__':
    run_gui()
