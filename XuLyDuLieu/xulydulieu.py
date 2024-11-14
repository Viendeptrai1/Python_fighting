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
    
    def chuyen_doi_du_lieu(self):
        smoker_values = {'no': 0, 'yes': 1}
        self.du_lieu['smoker_numeric'] = self.du_lieu['smoker'].map(smoker_values)
    
        sex_values = {'female': 0, 'male': 1}
        self.du_lieu['sex_numeric'] = self.du_lieu['sex'].map(sex_values)
    
   