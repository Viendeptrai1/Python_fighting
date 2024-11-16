import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class XuLyDuLieu:
    """
    Class thực hiện các thao tác xử lý dữ liệu cơ bản.
    """
    def __init__(self, du_lieu):
        self.du_lieu = du_lieu
        
    def chuan_hoa_du_lieu(self, cot_so):
        """
        Chuẩn hóa dữ liệu số về khoảng [0,1]
        Args:
            cot_so: List các cột số cần chuẩn hóa
        Returns:
            DataFrame đã chuẩn hóa
        """
        scaler = StandardScaler()
        self.du_lieu[cot_so] = scaler.fit_transform(self.du_lieu[cot_so])
        return self.du_lieu
    
    def xu_ly_du_lieu_thieu(self, phuong_phap='mean'):
        """
        Xử lý dữ liệu thiếu bằng các phương pháp khác nhau
        Args:
            phuong_phap: Phương pháp xử lý ('mean', 'median', 'mode', 'drop')
        Returns:
            DataFrame đã xử lý dữ liệu thiếu
        """
        if phuong_phap == 'drop':
            self.du_lieu = self.du_lieu.dropna()
        else:
            for column in self.du_lieu.columns:
                if self.du_lieu[column].isnull().any():
                    if phuong_phap == 'mean':
                        self.du_lieu[column].fillna(self.du_lieu[column].mean(), inplace=True)
                    elif phuong_phap == 'median':
                        self.du_lieu[column].fillna(self.du_lieu[column].median(), inplace=True)
                    elif phuong_phap == 'mode':
                        self.du_lieu[column].fillna(self.du_lieu[column].mode()[0], inplace=True)
        return self.du_lieu