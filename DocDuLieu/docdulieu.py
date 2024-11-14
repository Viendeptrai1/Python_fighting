import pandas as pd
import streamlit as st
class DuLieu:
    def __init__(self, ten_file):
        try:
            self.du_lieu = pd.read_csv(ten_file)
        except FileNotFoundError:
            st.error(f"Lỗi: Không tìm thấy file {ten_file}")
            self.du_lieu = None

    def lay_du_lieu(self):
        return self.du_lieu