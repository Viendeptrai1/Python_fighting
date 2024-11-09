import customtkinter as ctk

ctk.set_appearance_mode("light")

class GiaoDien:
    def __init__(self, master, xu_ly_du_lieu, truc_quan_hoa):
        self.master = master
        master.title("Visual Data - Tab Example")
        self.xu_ly_du_lieu = xu_ly_du_lieu
        self.truc_quan_hoa = truc_quan_hoa

        # Frame tiêu đề
        self.frame_header = ctk.CTkFrame(master, fg_color="white")
        self.frame_header.pack(fill='x')

        self.label_title = ctk.CTkLabel(
            self.frame_header, 
            text="Visual Data", 
            font=("Roboto", 24, "bold"), 
            text_color="black"
        )
        self.label_title.pack(pady=10)

        # Frame chứa các tab
        self.frame_tabs = ctk.CTkFrame(master, fg_color="#2a2d2e")
        self.frame_tabs.pack(fill='x', padx=20, pady=10)

        # Các nút tab
        self.tabs = ["Biểu đồ cột"
                     , "Biểu đồ tròn"
                     , "Biểu đồ doanh thu trung bình theo loại khách hàng"
                     , "Biểu đồ số lượng sản phẩm theo dòng sản phẩm"
                     , "Biểu đồ lợi nhuận trung bình theo chi nhánh"]
        self.buttons = []
        
        for idx, tab_name in enumerate(self.tabs):
            button = ctk.CTkButton(
                self.frame_tabs,
                text=tab_name,
                font=("Roboto", 14),
                width=130,
                height=40,
                corner_radius=10,
                command=lambda idx=idx: self.switch_tab(idx)
            )
            button.grid(row=0, column=idx, padx=5, pady=5)
            self.buttons.append(button)

        # Frame để hiển thị nội dung tab
        self.frame_content = ctk.CTkFrame(master, fg_color="white")
        self.frame_content.pack(fill='both', expand=True, padx=20, pady=20)

        # Label hiển thị biểu đồ (chỉ là ví dụ, bạn có thể thay bằng các biểu đồ thật)
        self.label_chart = ctk.CTkLabel(self.frame_content, text="", font=("Roboto", 16, "italic"))
        self.label_chart.pack(pady=20)

    def switch_tab(self, idx):
        tab_name = self.tabs[idx]
        
        # Thiết lập lại màu cho các tab để chỉ tab hiện tại có màu nổi bật
        for i, button in enumerate(self.buttons):
            button.configure(fg_color="#3b8ed0" if i == idx else "#2a2d2e")
        
        # Hiển thị loại biểu đồ tương ứng
        self.label_chart.configure(text=f"Đang hiển thị: {tab_name}")

        # Gọi hàm vẽ biểu đồ tương ứng
        try:
            if tab_name == "Biểu đồ cột":
                self.truc_quan_hoa.ve_bieu_do_cot("Branch", "Total")
            
            elif tab_name == "Biểu đồ tròn":
                self.truc_quan_hoa.ve_bieu_do_tron("Product line")
            elif tab_name == "Biểu đồ doanh thu trung bình theo loại khách hàng":
                self.truc_quan_hoa.ve_bieu_do_cot(self.xu_ly_du_lieu.doanh_thu_trung_binh_theo_loai_KH())
            elif tab_name == "Biểu đồ số lượng sản phẩm theo dòng sản phẩm":
                self.truc_quan_hoa.ve_bieu_do_cot(self.xu_ly_du_lieu.so_luong_san_pham_theo_dong_SP())
            elif tab_name == "Biểu đồ lợi nhuận trung bình theo chi nhánh":
                self.truc_quan_hoa.ve_bieu_do_cot(self.xu_ly_du_lieu.loi_nhuan_gop_trung_binh_theo_CN())
    
            else:
                print("Loại biểu đồ không hợp lệ.")
        except Exception as e:
            print(f"Đã xảy ra lỗi khi hiển thị biểu đồ: {e}")

# Khởi tạo customtkinter và cửa sổ chính
if __name__ == "__main__":
    root = ctk.CTk()
    xu_ly_du_lieu = None  # Thay thế bằng đối tượng xử lý dữ liệu của bạn
    truc_quan_hoa = None  # Thay thế bằng đối tượng trực quan hóa của bạn
    app = GiaoDien(root, xu_ly_du_lieu, truc_quan_hoa)
    root.geometry("800x600")
    root.mainloop()
