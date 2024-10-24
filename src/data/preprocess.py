# Xử lý việc tiền xử lý dữ liệu
import load_data

df = load_data.ReadFile("data/raw/data_raw.csv")

def DataFrame_No_Missing(df):
    """Lọc những dòng bị thiếu dữ liệu"""
    df_no_missing = df[df.notnull().all(axis=1)]
    return df_no_missing

def DataFrame_No_Duplicate(df):
    """Lọc những dòng bị trùng"""
    
def Doc_theo_Quoc_gia(df):
    """Xuất ra dataframe theo quốc gia"""
    
def Doc_theo_nam(df):
    """Xuất ra dataframe của tất cả quốc gia theo năm"""
    
def Update(df):
    """Sửa dữ liệu theo dòng"""
    
def Remove(df):
    """Xoá theo quốc gia, theo năm"""
    

    
    
    
    
    
if __name__ == "__main__":  
    print(DataFrame_No_Missing(df))