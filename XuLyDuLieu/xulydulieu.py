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