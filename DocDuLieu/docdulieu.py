import pandas as pd
import streamlit as st

class DuLieu:
    def __init__(self, ten_file):
        self.ten_file = ten_file
        self.du_lieu = self.tai_du_lieu()

    def tai_du_lieu(self):
        try:
            return pd.read_csv(self.ten_file)
        except FileNotFoundError:
            st.error(f"Lỗi: Không tìm thấy file {self.ten_file}")
            return None

    def luu_du_lieu(self):
        if self.du_lieu is not None:
            self.du_lieu.to_csv(self.ten_file, index=False)
    def lay_du_lieu(self):
        return self.du_lieu