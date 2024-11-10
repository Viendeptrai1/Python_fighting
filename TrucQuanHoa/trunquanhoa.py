import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TrucQuanHoa:
    def __init__(self, du_lieu):
        self.du_lieu = du_lieu
        
    def ve_bieu_do_cot(self, ten_cot_x, ten_cot_y, frame):
        # Xóa biểu đồ cũ nếu có
        for widget in frame.winfo_children():
            widget.destroy()
            
        # Tạo figure mới
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(self.du_lieu[ten_cot_x], self.du_lieu[ten_cot_y], color='skyblue')
        ax.set_xlabel(ten_cot_x)
        ax.set_ylabel(ten_cot_y)
        ax.set_title(f'Biểu đồ cột của {ten_cot_y} theo {ten_cot_x}')
        plt.xticks(rotation=45)
        
        # Tạo canvas và nhúng vào frame
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def ve_bieu_do_tron(self, cot_danh_muc, frame):
        # Xóa biểu đồ cũ nếu có
        for widget in frame.winfo_children():
            widget.destroy()
            
        # Tạo figure mới
        fig, ax = plt.subplots(figsize=(8, 8))
        self.du_lieu[cot_danh_muc].value_counts().plot.pie(
            autopct='%1.1f%%', 
            startangle=140,
            ax=ax
        )
        ax.set_title(f'Biểu đồ tròn của {cot_danh_muc}')
        ax.set_ylabel('')
        
        # Tạo canvas và nhúng vào frame
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def showinfo(self):
        return self.du_lieu.info()