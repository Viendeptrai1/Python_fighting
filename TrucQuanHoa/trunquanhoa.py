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
        if self.du_lieu is not None:
            # Tạo header
            print("\nAbout this file")
            print("-" * 80)
            print("Supermarket sales data")
            print("-" * 80 + "\n")

            columns_info = {
                'Invoice ID': {
                    'desc': 'Computer generated sales slip invoice identification number',
                    'show_unique': True
                },
                'Branch': {
                    'desc': 'Branch of supercenter (3 branches are available identified by A, B and C)',
                    'show_dist': True
                },
                'City': {
                    'desc': 'Location of supercenters',
                    'show_dist': True
                },
                'Customer type': {
                    'desc': 'Type of customers, recorded by Members for customers using member card and Normal for without member card',
                    'show_dist': True
                },
                'Gender': {
                    'desc': 'Gender type of customer',
                    'show_dist': True
                },
                'Product line': {
                    'desc': 'General item categorization groups',
                    'show_dist': True
                },
                'Unit price': {
                    'desc': 'Price of each product in $',
                    'show_dist': False,
                    'show_stats': True
                },
                'Quantity': {
                    'desc': 'Number of products purchased by customer',
                    'show_stats': True
                },
                'Tax 5%': {
                    'desc': '5% tax fee for customer buying',
                    'show_stats': True
                },
                'Total': {
                    'desc': 'Total price including tax',
                    'show_stats': True
                }
            }

            for col, info in columns_info.items():
                print(f"\n=> {col}")
                print(info['desc'])
                
                if col in self.du_lieu.columns:
                    if info.get('show_unique', False):
                        unique_count = self.du_lieu[col].nunique()
                        print(f"\n{unique_count:,} unique values")
                        print("\nExample values:")
                        print("\n".join(self.du_lieu[col].head(5).astype(str).tolist()))

                    if info.get('show_dist', False):
                        value_counts = self.du_lieu[col].value_counts()
                        total = len(self.du_lieu)
                        print("\nValue distribution:")
                        for val, count in value_counts.items():
                            percentage = (count/total) * 100
                            print(f"{val:<15} {percentage:>6.1f}%")
                    
                    if info.get('show_stats', False):
                        series = self.du_lieu[col]
                        stats = series.describe()
                        print(f"\nMin: {stats['min']:.2f}")
                        print(f"Max: {stats['max']:.2f}")
                        print(f"Mean: {stats['mean']:.2f}")
                        print(f"Std: {stats['std']:.2f}")

                    print("\n" + "-" * 80)
