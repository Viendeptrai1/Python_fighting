import customtkinter as ctk
from io import StringIO
import sys

ctk.set_appearance_mode("light")

class ScrollableTabFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Loại bỏ height từ kwargs nếu có để tránh xung đột
        kwargs.pop('height', None)
        super().__init__(master, **kwargs)
        
        # Container cho canvas và scrollbar
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill='x')
        
        # Tạo canvas với background phù hợp và chiều cao cố định
        self.canvas = ctk.CTkCanvas(self.container, bg='#2a2d2e', highlightthickness=0, height=52)
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
        self.frame_tabs = ScrollableTabFrame(master, fg_color="#2a2d2e")
        self.frame_tabs.pack(fill='x', padx=20, pady=(10, 5))

        # Các nút tab
        self.tabs = [
            "Biểu đồ cột", 
            "Biểu đồ tròn", 
            "Xem Info dataframe",
            "Biểu đồ đường",
            "Biểu đồ scatter",
            "Biểu đồ box",
            "Biểu đồ violin",
            "Biểu đồ heat map",
            "Biểu đồ bar stack",
            "Biểu đồ area",
            "Biểu đồ bubble",
            "Thống kê mô tả",
            "Phân tích tương quan"
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
        
        # Thêm scrollbar ngang
        self.text_info_x_scrollbar = ctk.CTkScrollbar(
            self.frame_content,
            orientation="horizontal",
            command=self.text_info.xview
        )
        self.text_info.configure(xscrollcommand=self.text_info_x_scrollbar.set)

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
            if tab_name == "Xem Info dataframe":
                self.frame_chart.pack_forget()
                self.text_info.pack(fill='both', expand=True, padx=10, pady=10)
                self.text_info.configure(state="normal")
                self.text_info.delete("1.0", "end")
                info_text = self.capture_output(self.truc_quan_hoa.showinfo)
                self.text_info.insert("1.0", info_text)
                self.text_info.configure(state="disabled")
                
            else:
                self.text_info.pack_forget()
                self.frame_chart.pack(fill='both', expand=True, padx=10, pady=10)
                if tab_name == "Biểu đồ cột":
                    self.truc_quan_hoa.ve_bieu_do_cot("Branch", "Total", self.frame_chart)
                elif tab_name == "Biểu đồ tròn":
                    self.truc_quan_hoa.ve_bieu_do_tron("Product line", self.frame_chart)
            
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