# Xử lý việc tiền xử lý dữ liệu
import load_data

df = load_data.ReadFile("data/raw/data_raw.csv")

def DataFrame_No_Missing(df):
    """Lọc những dòng bị thiếu dữ liệu"""
    df_no_missing = df[df.notnull().all(axis=1)]
    return df_no_missing

print(DataFrame_No_Missing(df))