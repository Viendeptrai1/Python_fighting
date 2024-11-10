import matplotlib.pyplot as plt
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

    
    def ve_bieu_do_duong_theo_thoi_gian(self, cot_thoi_gian, cot_gia_tri, 
                                       cot_nhom=None, title=None, figsize=(12, 6)):
        """
        Vẽ biểu đồ đường theo thời gian, có thể phân tách theo nhóm.
        """
        plt.figure(figsize=figsize)
        try:
            if cot_nhom:
                for name, group in self.du_lieu.groupby(cot_nhom):
                    plt.plot(group[cot_thoi_gian], group[cot_gia_tri], 
                            label=name, marker='o', linestyle='-')
                plt.legend(title=cot_nhom)
            else:
                plt.plot(self.du_lieu[cot_thoi_gian], self.du_lieu[cot_gia_tri], 
                        marker='o', linestyle='-')
            
            plt.title(title or f'Biểu đồ xu hướng {cot_gia_tri} theo thời gian')
            plt.xlabel(cot_thoi_gian)
            plt.ylabel(cot_gia_tri)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Lỗi khi vẽ biểu đồ đường: {str(e)}")

    def ve_dashboard_tong_quan(self, figsize=(15, 10)):
        """
        Vẽ dashboard tổng quan với nhiều biểu đồ khác nhau.
        """
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)
            
            # Biểu đồ 1: Doanh thu theo loại khách hàng
            self.du_lieu.groupby('Customer type')['Total'].mean().plot(
                kind='bar', ax=ax1, color=self.colors[0])
            ax1.set_title('Doanh thu trung bình theo loại KH')
            ax1.set_ylabel('Doanh thu')
            
            # Biểu đồ 2: Số lượng theo dòng sản phẩm
            self.du_lieu.groupby('Product line')['Quantity'].sum().plot(
                kind='bar', ax=ax2, color=self.colors[1])
            ax2.set_title('Số lượng bán theo dòng SP')
            ax2.tick_params(axis='x', rotation=45)
            
            # Biểu đồ 3: Phân bố điểm đánh giá
            sns.boxplot(x='Branch', y='Rating', data=self.du_lieu, ax=ax3, color=self.colors[2])
            ax3.set_title('Phân bố điểm đánh giá theo chi nhánh')
            
            # Biểu đồ 4: Tỷ lệ thanh toán
            payment_data = self.du_lieu['Payment'].value_counts()
            ax4.pie(payment_data, labels=payment_data.index, autopct='%1.1f%%', colors=self.colors)
            ax4.set_title('Tỷ lệ phương thức thanh toán')
            
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Lỗi khi vẽ dashboard: {str(e)}")

    def luu_bieu_do(self, filename, dpi=300):
        """
        Lưu biểu đồ hiện tại thành file ảnh.
        """
        try:
            plt.savefig(filename, dpi=dpi, bbox_inches='tight')
        except Exception as e:
            print(f"Lỗi khi lưu biểu đồ: {str(e)}")





    def ve_bieu_do_cot(self, ten_cot_x, ten_cot_y):
        """
        Vẽ biểu đồ cột.
        """
        plt.figure(figsize=(10, 6))
        plt.bar(self.du_lieu[ten_cot_x], self.du_lieu[ten_cot_y], color='skyblue')
        plt.xlabel(ten_cot_x)
        plt.ylabel(ten_cot_y)
        plt.title(f'Biểu đồ cột của {ten_cot_y} theo {ten_cot_x}')
        plt.xticks(rotation=45)
        plt.show()

    def ve_bieu_do_tron(self, cot_danh_muc):
        """
        Vẽ biểu đồ tròn cho phân phối của một cột danh mục.
        """
        plt.figure(figsize=(8, 8))
        self.du_lieu[cot_danh_muc].value_counts().plot.pie(autopct='%1.1f%%', startangle=140)
        plt.title(f'Biểu đồ tròn của {cot_danh_muc}')
        plt.ylabel('')
        plt.show()
        
    
    def ve_doanh_thu_trung_binh_theo_loai_KH(self, xu_ly_du_lieu):
        plt.figure(figsize=(8, 6))
        xu_ly_du_lieu.doanh_thu_trung_binh_theo_loai_KH().plot(kind = "bar", color = "blue", edgecolor = "black")    
        plt.xticks(rotation = 0)
        plt.show()
    
    def ve_so_luong_san_pham_theo_dong_SP(self, xu_ly_du_lieu):
        plt.figure(figsize=(8, 6))
        xu_ly_du_lieu.so_luong_san_pham_theo_dong_SP().plot(kind = "bar", color = "blue", edgecolor = "black")    
        plt.xticks(rotation = 0)
        plt.show()
        
    def ve_loi_nhuan_gop_trung_binh_theo_CN(self, xu_ly_du_lieu):
        plt.figure(figsize=(8, 6))
        xu_ly_du_lieu.loi_nhuan_gop_trung_binh_theo_CN().plot(kind = "bar", color = "blue", edgecolor = "black")    
        plt.xticks(rotation = 0)
        plt.show()
        
    def ve_diem_danh_gia_trung_binh_theo_dong_SP(self, xu_ly_du_lieu):
        plt.figure(figsize=(8, 6))
        xu_ly_du_lieu.diem_danh_gia_trung_binh_theo_dong_SP().plot(kind = "bar", color = "blue", edgecolor = "black")    
        plt.xticks(rotation = 0)
        plt.show()
        
    
    def ve_bieu_do_so_luong_moi_gioi_tinh_theo_SP(self, df):
        plt.figure(figsize=(12, 6))
        sns.countplot(x='Product line', hue='Gender', data = df)
        plt.title('Number of Each Gender by Product line')
        plt.xlabel('Product line')
        plt.ylabel('Count')
        plt.legend(title='Gender')
        plt.show()

    
