import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class TienXuLyDuLieu:
    def __init__(self):
        self.categorical_columns = ['sex', 'smoker', 'region']
        self.numerical_columns = ['age', 'bmi', 'children']
        self.target_column = 'charges'
        self.standard_scaler = StandardScaler()
        self.minmax_scaler = MinMaxScaler()
        self.label_encoders = {}

    def chuan_hoa_du_lieu(self, du_lieu, phuong_phap='standard'):
        """
        Chuẩn hóa dữ liệu với lựa chọn phương pháp
        Args:
            du_lieu: DataFrame cần chuẩn hóa
            phuong_phap: 'standard' hoặc 'minmax'
        Returns:
            DataFrame đã được chuẩn hóa
        """
        du_lieu_da_xu_ly = du_lieu.copy()

        # Chuẩn hóa dữ liệu số
        if phuong_phap == 'standard':
            du_lieu_da_xu_ly[self.numerical_columns] = self.standard_scaler.fit_transform(
                du_lieu[self.numerical_columns]
            )
        else:
            du_lieu_da_xu_ly[self.numerical_columns] = self.minmax_scaler.fit_transform(
                du_lieu[self.numerical_columns]
            )

        # Mã hóa dữ liệu phân loại
        for column in self.categorical_columns:
            du_lieu_da_xu_ly[column] = pd.Categorical(du_lieu[column]).codes

        return du_lieu_da_xu_ly
