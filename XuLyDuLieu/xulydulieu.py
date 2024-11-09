import pandas as pd

class XuLyDuLieu:
    """
    Class này thực hiện các bước xử lý và biến đổi dữ liệu.
    """

    def __init__(self, du_lieu):
        """
        Khởi tạo đối tượng XuLyDuLieu.

        Args:
          du_lieu: DataFrame chứa dữ liệu.
        """
        self.du_lieu = du_lieu

    def lam_sach_du_lieu(self):
        """
        Thay thế giá trị ngoại lai bằng giá trị trung bình.
        """
        for cot in ['Unit price', 'Quantity', 'Total']:  # Chọn các cột số cần xử lý
            Q1 = self.du_lieu[cot].quantile(0.25)
            Q3 = self.du_lieu[cot].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            self.du_lieu[cot] = self.du_lieu[cot].mask(
                (self.du_lieu[cot] < lower_bound) | (self.du_lieu[cot] > upper_bound), 
                self.du_lieu[cot].mean()
            )

    def tinh_them_chi_so(self):
        """
        Tính toán thêm các chỉ số mới.
        """
        
    def chuyen_doi_du_lieu(self):
        """
        Chuyển đổi dữ liệu sang định dạng phù hợp.
        """
      