# Có thể chịu trách nhiệm tải dữ liệu
import pandas as pd


def ReadFile(_PATH):
    """Read file raw"""
    data_temp = pd.read_csv(_PATH)
    
    return data_temp
