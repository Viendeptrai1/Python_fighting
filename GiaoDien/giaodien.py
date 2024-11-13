import customtkinter as ctk
from io import StringIO
import sys
import platform

ctk.set_appearance_mode("light")

class ScrollableTabFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Loại bỏ height từ kwargs nếu có để tránh xung đột
        kwargs.pop('height', None)
        super().__init__(master, **kwargs)
        
        # Container cho canvas và scrollbar
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill='x')  # Thay đổi từ 'both' thành 'x'
        
        # Tạo canvas với background phù hợp và chiều cao cố định
        self.canvas = ctk.CTkCanvas(self.container, bg='#2a2d2e', highlightthickness=0, height=52)  # Chiều cao = button height + 2*padding
        self.scrollbar = ctk.CTkScrollbar(
            self.container, 
            orientation="horizontal",
            command=self.canvas.xview,
            height=16
        )
        
        # Frame trong canvas để chứa các button
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="#2a2d2e")
        
        # Cấu hình canvas
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        
        # Sắp xếp các widget
        self.canvas.pack(side="top", fill="x", padx=0, pady=0)
        self.scrollbar.pack(side="bottom", fill="x", padx=0)
        
        # Tạo window trong canvas
        self.canvas_frame = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )
        
        # Bind các sự kiện
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Bind sự kiện cuộn chuột
        self.bind_mouse_scroll()

    # [Giữ nguyên các phương thức khác của ScrollableTabFrame]
    def bind_mouse_scroll(self):
        if platform.system() == 'Windows':
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)
        elif platform.system() == 'Darwin':
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_macos)
            self.canvas.bind_all("<Option-MouseWheel>", self._on_mousewheel_macos_fast)
        else:
            self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
            self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _on_mousewheel_windows(self, event):
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_macos(self, event):
        self.canvas.xview_scroll(int(event.delta), "units")

    def _on_mousewheel_macos_fast(self, event):
        self.canvas.xview_scroll(int(event.delta * 2), "units")

    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self.canvas.xview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.xview_scroll(1, "units")
        
    def on_frame_configure(self, event):
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.configure(scrollregion=(bbox[0]-5, bbox[1], bbox[2]+5, bbox[3]))
        
    def on_canvas_configure(self, event):
        min_width = max(event.width, self.scrollable_frame.winfo_reqwidth())
        self.canvas.itemconfig(self.canvas_frame, width=min_width)

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

        # Frame cuộn chứa các tab với padding phù hợp
        self.frame_tabs = ScrollableTabFrame(master, fg_color="#2a2d2e")  # Đã loại bỏ height
        self.frame_tabs.pack(fill='x', padx=20, pady=(10, 5))

        # Các nút tab
        self.tabs = [
            "Hình dung về sự phân bố chi phí y tế liên quan đến các yếu tố khác như 'giới tính' và 'khu vực'.",
            "Hình dung về sự phân bố của các cột 'giới tính', 'khu vực' và 'số lượng con cái'.",
            "Hình dung về cách cột 'chi phí' liên quan đến các cột khác ('số lượng con cái', 'giới tính', 'khu vực' và 'người hút thuốc')."
        ]
        self.buttons = []
        
        # Tạo các button với padding nhỏ hơn
        for idx, tab_name in enumerate(self.tabs):
            button = ctk.CTkButton(
                self.frame_tabs.scrollable_frame,
                text=tab_name,
                font=("Roboto", 14),
                width=140,
                height=40,
                corner_radius=10,
                command=lambda idx=idx: self.switch_tab(idx)
            )
            button.grid(row=0, column=idx, padx=6, pady=6)
            self.buttons.append(button)

        # [Giữ nguyên phần còn lại của class GiaoDien]
        # Frame content
        self.frame_content = ctk.CTkFrame(master, fg_color="white")
        self.frame_content.pack(fill='both', expand=True, padx=20, pady=20)

        # Frame chart
        self.frame_chart = ctk.CTkFrame(self.frame_content, fg_color="white")
        self.frame_chart.pack(fill='both', expand=True, padx=10, pady=10)

        # Textbox với thanh cuộn
        self.text_info = ctk.CTkTextbox(
            self.frame_content,
            width=700,
            height=400,
            font=("Roboto", 12),
            fg_color="white",
            text_color="black",
            wrap="none"
        )
        self.text_info.pack_forget()

    def switch_tab(self, idx):
        tab_name = self.tabs[idx]
        
        for i, button in enumerate(self.buttons):
            if i == idx:
                button.configure(
                    fg_color="#3b8ed0",
                    hover_color="#2b7cbd"
                )
            else:
                button.configure(
                    fg_color="#2a2d2e",
                    hover_color="#404249"
                )
        
        try:
                self.text_info.pack_forget()
                self.frame_chart.pack(fill='both', expand=True, padx=10, pady=10)
                if tab_name == "Hình dung về sự phân bố chi phí y tế liên quan đến các yếu tố khác như 'giới tính' và 'khu vực'.":
                    self.truc_quan_hoa.ve_bieu_do_histogram(
                        cot_gia_tri='age',
                        bien='box',
                        so_khoang=47, 
                        title='Phân bố tuổi'
                    )
                    self.truc_quan_hoa.ve_bieu_do_histogram(
                        cot_gia_tri='bmi',
                        bien='box',
                        mau_cu_the = ['red'],
                        title='Phân bố BMI(Body Mass Index)'
                    )
                    self.truc_quan_hoa.ve_bieu_do_histogram(
                        cot_gia_tri='charges',
                        bien='box',
                        mau_phan_loai = 'smoker',
                        mau_cu_the = ['red','grey'],
                        title='Phí y tế hàng năm'
                    )
                    self.truc_quan_hoa.ve_bieu_do_histogram(
                        cot_gia_tri='charges',
                        mau_phan_loai = 'sex',
                        mau_cu_the = ['blue','red'],
                        title='Các khoản phí khác nhau về giới tính'
                    )
                    self.truc_quan_hoa.ve_bieu_do_histogram(
                        cot_gia_tri='charges',
                        bien='box',
                        mau_phan_loai = 'region',
                        title='Chi phí trên các khu vực khác nhau của Hoa Kỳ'
                    )
                    self.truc_quan_hoa.ve_bieu_do_histogram(
                        cot_gia_tri='smoker',
                        mau_phan_loai = 'sex',
                        title='Số lượng hút thuốc và không hút thuốc theo nam và nữ'
                    )
                elif tab_name == "Hình dung về sự phân bố của các cột 'giới tính', 'khu vực' và 'số lượng con cái'.":
                    self.truc_quan_hoa.ve_bieu_do_histogram(
                        cot_gia_tri='charges',
                        bien='box',
                        mau_phan_loai = 'children',
                        title='Chi phí phát sinh cho trẻ em'
                    )
                    self.truc_quan_hoa.ve_bieu_do_scatter(
                        cot_gia_tri='age',
                        cot_nhom='charges',
                        mau_phan_loai='smoker',
                        do_mo=0.8,
                        du_lieu_them=['sex'],
                        title='Chi phí so với độ tuổi'
                    )
                    self.truc_quan_hoa.ve_bieu_do_scatter(
                        cot_gia_tri='bmi',
                        cot_nhom='charges',
                        mau_phan_loai='smoker',
                        do_mo=0.8,
                        du_lieu_them=['sex'],
                        title='Chi phí so với BMI'
                    )
                elif tab_name == "Hình dung về cách cột 'chi phí' liên quan đến các cột khác ('số lượng con cái', 'giới tính', 'khu vực' và 'người hút thuốc').":
                    self.truc_quan_hoa.ve_bieu_do_violin(
                        cot_gia_tri='children',
                        cot_nhom='charges',
                        title='Chi phí so với số lượng con cái'
                    )
                    self.truc_quan_hoa.ve_bieu_do_barplot(
                        cot_gia_tri='sex',
                        cot_nhom='charges',
                        du_lieu_phan_biet='smoker',
                        title='Chi phí so với việc hút thuốc hay không hút thuốc theo giới tính'
                    )
                    self.truc_quan_hoa.ve_bieu_do_histogram(
                        cot_gia_tri='sex',
                        cot_nhom='charges',
                        mau_phan_loai='region',
                        nhan_x='Tổng chi phí',
                        nhan_y='Giới tính',
                        title='Chi phí so với vùng theo giới tính'
                    )
                    self.truc_quan_hoa.ve_bieu_do_heatmap(
                        title='Ma trận tương quan'
                    )
                    
                    
                
                    
                
                
                
                    
                
               
                    
        except Exception as e:
            self.frame_chart.pack_forget()
            self.text_info.pack(fill='both', expand=True, padx=10, pady=10)
            self.text_info.configure(state="normal")
            self.text_info.delete("1.0", "end")
            self.text_info.insert("1.0", f"Đã xảy ra lỗi: {str(e)}")
            self.text_info.configure(state="disabled")

    def capture_output(self, func):
        buffer = StringIO()
        old_stdout = sys.stdout
        sys.stdout = buffer
        func()
        sys.stdout = old_stdout
        return buffer.getvalue()

if __name__ == "__main__":
    root = ctk.CTk()
    xu_ly_du_lieu = None
    truc_quan_hoa = None
    app = GiaoDien(root, xu_ly_du_lieu, truc_quan_hoa)
    root.geometry("800x600")
    root.mainloop()