import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import pandas as pd
import numpy as np

class TrucQuanHoa:
    """
    Class thực hiện việc trực quan hóa dữ liệu với nhiều loại biểu đồ khác nhau.
    """
    def __init__(self, du_lieu):
        """
        Khởi tạo đối tượng TrucQuanHoa.
        Args:
            du_lieu: DataFrame chứa dữ liệu cần trực quan hóa
        """
        self.du_lieu = du_lieu
        # Thay đổi cách thiết lập style
        plt.style.use('default')  # Sử dụng style mặc định thay vì seaborn
        sns.set_style("whitegrid")  # Thiết lập style cho seaborn riêng
        self.colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#99CCFF']

    def ve_bieu_do_cot_so_sanh(self, cot_nhom, cot_gia_tri, title=None, figsize=(12, 6), 
                              rotation=45, legend_title=None, stacked=False):
        """
        Vẽ biểu đồ cột so sánh các giá trị theo nhóm.
        """
        plt.figure(figsize=figsize)
        try:
            if stacked and isinstance(cot_nhom, (list, tuple)) and len(cot_nhom) == 2:
                pivot_df = self.du_lieu.pivot_table(
                    index=cot_nhom[0], 
                    columns=cot_nhom[1], 
                    values=cot_gia_tri,
                    aggfunc='sum'
                )
                pivot_df.plot(kind='bar', stacked=True, color=self.colors)
            else:
                if isinstance(cot_nhom, (list, tuple)):
                    cot_nhom = cot_nhom[0]
                data_grouped = self.du_lieu.groupby(cot_nhom)[cot_gia_tri].mean()
                data_grouped.plot(kind='bar', color=self.colors[0])
        
            plt.title(title or f'Biểu đồ so sánh {cot_gia_tri} theo {cot_nhom}')
            plt.xticks(rotation=rotation)
            if legend_title:
                plt.legend(title=legend_title)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Lỗi khi vẽ biểu đồ cột: {str(e)}")

    def ve_bieu_do_phan_phoi(self, cot_gia_tri, cot_nhom=None, title=None, figsize=(12, 6)):
        """
        Vẽ biểu đồ phân phối (histogram và kernel density) cho một biến số.
        """
        plt.figure(figsize=figsize)
        if cot_nhom:
            for name, group in self.du_lieu.groupby(cot_nhom):
                sns.kdeplot(data=group, x=cot_gia_tri, label=name)
            plt.legend(title=cot_nhom)
        else:
            sns.histplot(data=self.du_lieu, x=cot_gia_tri, kde=True)
        
        plt.title(title or f'Phân phối của {cot_gia_tri}')
        plt.xlabel(cot_gia_tri)
        plt.ylabel('Tần số/Mật độ')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
        
    def ve_bieu_do_histogram(self, cot_gia_tri, so_khoang = None, title=None,  figsize=(12, 6)):
        """
        Vẽ biểu đồ histogram cho một biến số.
        """
        fig = px.histogram(self.du_lieu, 
                   x = cot_gia_tri, 
                   marginal='box', 
                   nbins= so_khoang or 30,
                   color_discrete_sequence = self.colors,
                   title = title or f'Histogram của {cot_gia_tri}')
        fig.update_layout(bargap=0.1)
        fig.show()

    def ve_bieu_do_scatter_matrix(self, danh_sach_cot, figsize=(12, 12)):
        """
        Vẽ ma trận biểu đồ scatter plot cho nhiều biến số.
        """
        sns.set(style="ticks")
        sns.pairplot(self.du_lieu[danh_sach_cot])
        plt.tight_layout()
        plt.show()
        
    def ve_bieu_do_heatmap(self, pivot_index, pivot_columns, pivot_values, 
                          title=None, figsize=(12, 8), fmt='.2f'):
        """
        Vẽ biểu đồ nhiệt (heatmap) cho dữ liệu pivot.
        """
        plt.figure(figsize=figsize)
        pivot_table = self.du_lieu.pivot_table(
            index=pivot_index,
            columns=pivot_columns,
            values=pivot_values,
            aggfunc='mean'
        )
        
        sns.heatmap(pivot_table, annot=True, fmt=fmt, cmap='YlOrRd', 
                   center=pivot_table.mean().mean())
        plt.title(title or f'Heatmap của {pivot_values}')
        plt.tight_layout()
        plt.show()

    def ve_bieu_do_box(self, cot_gia_tri, cot_nhom, title=None, figsize=(12, 6)):
        """
        Vẽ biểu đồ box plot để so sánh phân phối giữa các nhóm.
        """
        plt.figure(figsize=figsize)
        sns.boxplot(x=cot_nhom, y=cot_gia_tri, data=self.du_lieu, palette=self.colors)
        plt.title(title or f'Phân phối {cot_gia_tri} theo {cot_nhom}')
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    def ve_bieu_do_violin(self, cot_gia_tri, cot_nhom, title=None, figsize=(12, 6)):
        """
        Vẽ biểu đồ violin để so sánh phân phối chi tiết giữa các nhóm.
        """
        plt.figure(figsize=figsize)
        sns.violinplot(x=cot_nhom, y=cot_gia_tri, data=self.du_lieu, palette=self.colors)
        plt.title(title or f'Phân phối chi tiết {cot_gia_tri} theo {cot_nhom}')
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
        

    
