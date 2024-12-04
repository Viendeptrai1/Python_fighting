import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class TienXuLyDuLieu:
    def __init__(self):
        self.categorical_columns = ['sex', 'smoker', 'region']
        self.numerical_columns = ['age', 'bmi', 'children']
        self.target_column = 'charges'
        self.standard_scaler = StandardScaler()
        self.minmax_scaler = MinMaxScaler()
        self.categorical_mappings = {}

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

        # Mã hóa dữ liệu phân loại và lưu mapping
        for column in self.categorical_columns:
            unique_values = sorted(du_lieu[column].unique())
            self.categorical_mappings[column] = {val: idx for idx, val in enumerate(unique_values)}
            du_lieu_da_xu_ly[column] = du_lieu[column].map(self.categorical_mappings[column])

        return du_lieu_da_xu_ly

    def chuan_hoa_du_lieu_moi(self, du_lieu_moi, phuong_phap='standard'):
        """
        Chuẩn hóa dữ liệu mới sử dụng các tham số đã được fit
        Args:
            du_lieu_moi: DataFrame cần chuẩn hóa
            phuong_phap: 'standard' hoặc 'minmax'
        Returns:
            DataFrame đã được chuẩn hóa
        """
        du_lieu_da_xu_ly = du_lieu_moi.copy()

        # Chuẩn hóa dữ liệu số
        if phuong_phap == 'standard':
            du_lieu_da_xu_ly[self.numerical_columns] = self.standard_scaler.transform(
                du_lieu_moi[self.numerical_columns]
            )
        else:
            du_lieu_da_xu_ly[self.numerical_columns] = self.minmax_scaler.transform(
                du_lieu_moi[self.numerical_columns]
            )

        # Sử dụng mapping đã lưu cho dữ liệu phân loại
        for column in self.categorical_columns:
            du_lieu_da_xu_ly[column] = du_lieu_moi[column].map(self.categorical_mappings[column])

        return du_lieu_da_xu_ly
