import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class TrucQuanHoa:
    """
    Class này chịu trách nhiệm vẽ các biểu đồ trực quan hóa dữ liệu.
    """

    def __init__(self, du_lieu):
        """
        Khởi tạo đối tượng TrucQuanHoa.

        Args:
          du_lieu: DataFrame chứa dữ liệu.
        """
        self.du_lieu = du_lieu

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
