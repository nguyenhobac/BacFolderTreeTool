# Hướng Dẫn Sử Dụng - Sao Chép Cây Thư Mục (Copy Folder Tree)

**Phiên bản:** 1.0.0  
**Ngày cập nhật:** 04/05/2026  
**Tác giả:** TS. NGUYỄN HỒ BẮC  

---

## 1. Công dụng chi tiết
Tiện ích này giúp bạn sao chép **toàn bộ cấu trúc thư mục** (bao gồm các thư mục con nhiều lớp) từ một thư mục gốc sang một vị trí mới mà **không sao chép các tệp tin (files)** bên trong chúng. 
Điều này rất hữu ích khi bạn muốn tạo một bộ khung thư mục dự án trống dựa trên một dự án đã có sẵn. Ứng dụng hỗ trợ tốt các đường dẫn chứa ký tự tiếng Việt (Unicode).

## 2. Hướng dẫn sử dụng

### Sử dụng qua Giao diện (GUI)
1. Mở ứng dụng (nhấp đúp vào file `copy_folder_tree.py`).
2. Tại mục **Thư mục nguồn**, bấm nút **Chọn...** để chỉ định thư mục gốc bạn muốn sao chép cấu trúc.
3. Tại mục **Thư mục đích**, bấm nút **Chọn...** để chỉ định nơi bạn muốn dán cấu trúc thư mục vào.
4. Bấm nút **Thực hiện sao chép**. Ứng dụng sẽ thông báo thành công khi hoàn tất.

## 3. Nguồn tham khảo & Sự hỗ trợ
- **Tham chiếu lõi logic:** Tham khảo cách sử dụng `shutil` từ [GeeksforGeeks](https://www.geeksforgeeks.org/python-copy-directory-structure-without-files/).
- **Phát triển & Cải tiến:** Quá trình nâng cấp, chuyển đổi từ kịch bản dòng lệnh sang giao diện đồ họa (GUI) trực quan và viết tài liệu được hỗ trợ bởi Trí tuệ Nhân tạo (AI Antigravity - Google Deepmind).