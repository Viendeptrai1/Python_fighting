import pandas as pd
import numpy as np

class XuLyDuLieu:
    def __init__(self, du_lieu):
        self.du_lieu = du_lieu

    def thong_ke_mo_ta(self):
        return self.du_lieu.describe()

    def phan_tich_tuong_quan(self):
        numeric_cols = self.du_lieu.select_dtypes(include=[np.number]).columns
        return self.du_lieu[numeric_cols].corr()

    def loc_du_lieu(self, column, value, operator="equals"):
        if operator == "equals":
            return self.du_lieu[self.du_lieu[column] == value]
        elif operator == "greater":
            return self.du_lieu[self.du_lieu[column] > value]
        elif operator == "less":
            return self.du_lieu[self.du_lieu[column] < value]
        return self.du_lieu

    def them_ban_ghi(self, new_record):
        new_record_df = pd.DataFrame([new_record])
        self.du_lieu = pd.concat([self.du_lieu, new_record_df], ignore_index=True)
        return "Đã thêm bản ghi mới thành công!"

    def cap_nhat_ban_ghi(self, index, column, new_value):
        self.du_lieu.at[index, column] = new_value
        return f"Đã cập nhật {column} tại index {index} thành {new_value}"

    def xoa_ban_ghi(self, index):
        self.du_lieu = self.du_lieu.drop(index).reset_index(drop=True)
        return "Đã xóa bản ghi thành công!"

    def sap_xep_du_lieu(self, column, ascending=True):
        self.du_lieu = self.du_lieu.sort_values(by=column, ascending=ascending)
