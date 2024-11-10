import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, StringVar
import pandas as pd
from io import StringIO
import sys
import platform

# Cài đặt chế độ giao diện cho customtkinter
ctk.set_appearance_mode("light")

# Class xử lý dữ liệu từ CSV
class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        """Đọc dữ liệu từ file CSV."""
        return pd.read_csv(self.file_path)

    def get_invoice_details(self, invoice_id):
        """Trả về thông tin dựa trên Invoice ID."""
        entry = self.data[self.data['Invoice ID'] == invoice_id]
        if not entry.empty:
            return entry.to_dict(orient='records')[0]
        else:
            return None

    def get_all_invoice_ids(self):
        """Trả về danh sách tất cả Invoice ID có trong dữ liệu."""
        return self.data['Invoice ID'].unique().tolist()

# Class tạo khung cuộn chứa các tab
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
        
#code Giao Dien
class GiaoDien:
    def __init__(self, master, xu_ly_du_lieu, truc_quan_hoa):
        self.master = master
        master.title("Visual Data - Tab Example")
        self.xu_ly_du_lieu = xu_ly_du_lieu
        self.truc_quan_hoa = truc_quan_hoa
        
        self.master.title("Visual Data - Invoice Lookup")
        master.title("Visual Data - Tab Example")
        
        # Tạo đối tượng xử lý dữ liệu và load Invoice IDs
        self.data_handler = DataHandler('Data/data_sales.csv')
        self.invoice_ids = self.data_handler.get_all_invoice_ids()
        
        # Tạo frame tiêu đề và chọn Invoice ID
        self.label_title = ctk.CTkLabel(master, text="Chọn Invoice ID:", font=("Roboto", 16))
        self.label_title.pack(pady=10)

        self.selected_id = StringVar(master)
        self.selected_id.set(self.invoice_ids[0])

        self.option_menu = tk.OptionMenu(master, self.selected_id, *self.invoice_ids)
        self.option_menu.config(font=("Arial", 14))
        self.option_menu.pack(pady=10)

        self.search_button = ctk.CTkButton(master, text="Tìm kiếm", command=self.show_invoice_details, font=("Roboto", 14))
        self.search_button.pack(pady=10)

        self.result_label = tk.Label(master, text="", justify='left', font=("Arial", 12))
        self.result_label.pack(pady=10)
        
        self.frame_header = ctk.CTkFrame(master, fg_color="white")
        self.frame_header.pack(fill='x')
        self.label_title = ctk.CTkLabel(
            self.frame_header, 
            text="Visual Data", 
            font=("Roboto", 24, "bold"), 
            text_color="black"
        )
        self.label_title.pack(pady=10)
        # Frame cuộn chứa các tab
        self.frame_tabs = ScrollableTabFrame(master, fg_color="#2a2d2e")
        self.frame_tabs.pack(fill='x', padx=20, pady=(10, 5))
        
        # Tạo các button tab
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
            "Phân tích tương quan",
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
            "Phân tích tương quan"]
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
        #show invoice id
    def show_invoice_details(self):
        invoice_id = self.selected_id.get()
        details = self.data_handler.get_invoice_details(invoice_id)
        
        if details:
            result = f"Biên lai cho Invoice ID: {invoice_id}\n"
            for key, value in details.items():
                result += f"{key}: {value}\n"
            self.result_label.config(text=result)
        else:
            messagebox.showerror("Không tìm thấy", "Invoice ID không hợp lệ.")

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
    #
if __name__ == "__main__":
   root = ctk.CTk()
   xu_ly_du_lieu = None
   truc_quan_hoa = None
   app = GiaoDien(root, xu_ly_du_lieu, truc_quan_hoa)
   root.geometry("800x600")
   root.mainloop()