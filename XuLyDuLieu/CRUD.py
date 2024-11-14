import pandas as pd
import numpy as np

def transform_insurance_data(df):
    
    df_transformed = df.copy()
    
   #Thêm cột smorker_code (1: có, 0: không)
    df_transformed['smoker_code'] = (df_transformed['smoker'] == 'yes').astype(int)
    
    #Thêm cột sex_code  (1: male, 0: female)
    df_transformed['sex_code'] = (df_transformed['sex'] == 'male').astype(int)
    
    # Tạo các cột được mã hóa một lần cho các vùng
    df_transformed['northeast'] = (df_transformed['region'] == 'northeast').astype(float)
    df_transformed['northwest'] = (df_transformed['region'] == 'northwest').astype(float)
    df_transformed['southeast'] = (df_transformed['region'] == 'southeast').astype(float)
    df_transformed['southwest'] = (df_transformed['region'] == 'southwest').astype(float)
    
    return df_transformed

# Đọc dữ liệu ban đầu và chuyển đổi nó
df = pd.read_csv("data\Health_insurance.csv")
df = transform_insurance_data(df)

def add_new_record():
    """Thêm một bản ghi mới vào DataFrame"""
    global df
    print("\n=== Thêm bản ghi mới ===")
    new_record = {}
    new_record['age'] = int(input("Nhập tuổi: "))
    new_record['sex'] = input("Nhập giới tính (male/female): ")
    new_record['bmi'] = float(input("Nhập BMI: "))
    new_record['children'] = int(input("Nhập số con: "))
    new_record['smoker'] = input("Nhập tình trạng hút thuốc (yes/no): ")
    new_record['region'] = input("Nhập khu vực (southwest/southeast/northwest/northeast): ")
    new_record['charges'] = float(input("Nhập chi phí: "))
    
    # Tạo một DataFrame tạm thời với bản ghi mới
    temp_df = pd.DataFrame([new_record])
    temp_df = transform_insurance_data(temp_df)
    
    # Thêm bản ghi đã chuyển đổi
    df = pd.concat([df, temp_df], ignore_index=True)
    return "Đã thêm bản ghi mới thành công!"

def update_record():
    """Cập nhật một giá trị trong DataFrame"""
    global df
    print("\n=== Cập nhật bản ghi ===")
    print("Dữ liệu hiện tại:")
    print(df)
    index = int(input("\nNhập index cần cập nhật: "))
    column = input("Nhập tên cột cần cập nhật: ")
    new_value = input("Nhập giá trị mới: ")
    
    # Chuyển đổi kiểu dữ liệu phù hợp
    if column in ['age', 'children']:
        new_value = int(new_value)
    elif column in ['bmi', 'charges']:
        new_value = float(new_value)
    
    df.at[index, column] = new_value
    
    # Nếu cập nhật một cột ảnh hưởng đến các cột được mã hóa, thực hiện lại phép chuyển đổi
    if column in ['sex', 'smoker', 'region']:
        df = transform_insurance_data(df)
    
    return f"Đã cập nhật {column} tại index {index} thành {new_value}"

def delete_records():
    """Xóa các bản ghi theo index"""
    global df
    print("\n=== Xóa bản ghi ===")
    print("Dữ liệu hiện tại:")
    print(df)
    index = int(input("\nNhập index cần xóa: "))
    df = df.drop(index)
    return "Đã xóa bản ghi thành công!"

def sort_data():
    """Sắp xếp DataFrame theo cột được chọn"""
    global df
    print("\n=== Sắp xếp dữ liệu ===")
    column = input("Nhập tên cột cần sắp xếp: ")
    order = input("Sắp xếp tăng dần? (yes/no): ")
    df = df.sort_values(by=column, ascending=(order.lower() == 'yes'))
    return "Đã sắp xếp dữ liệu thành công!"

def search_data():
    """Tìm kiếm dữ liệu theo cột và giá trị"""
    print("\n=== Tìm kiếm dữ liệu ===")
    column = input("Nhập tên cột cần tìm kiếm: ")
    value = input("Nhập giá trị cần tìm: ")
    
    # Chuyển đổi kiểu dữ liệu phù hợp
    if column in ['age', 'children']:
        value = int(value)
    elif column in ['bmi', 'charges']:
        value = float(value)
    
    result = df[df[column] == value]
    print("\nKết quả tìm kiếm:")
    print(result)

def show_statistics():
    """Hiển thị thống kê cơ bản"""
    print("\n=== Thống kê cơ bản ===")
    print("\nThống kê mô tả:")
    print(df.describe())
    print("\nChi phí trung bình theo khu vực:")
    print(df.groupby('region')['charges'].mean())
    print("\nTỷ lệ theo giới tính và hút thuốc:")
    print("Sex code (1=male, 0=female):", df['sex_code'].value_counts(normalize=True))
    print("Smoker code (1=yes, 0=no):", df['smoker_code'].value_counts(normalize=True))

def display_data():
    """Hiển thị toàn bộ dữ liệu"""
    print("\n=== Dữ liệu hiện tại ===")
    print(df)

def main():
    while True:
        print("\n=== MENU QUẢN LÝ DỮ LIỆU BẢO HIỂM ===")
        print("1. Hiển thị dữ liệu")
        print("2. Thêm bản ghi mới")
        print("3. Cập nhật bản ghi")
        print("4. Xóa bản ghi")
        print("5. Sắp xếp dữ liệu")
        print("6. Tìm kiếm dữ liệu")
        print("7. Xem thống kê")
        print("0. Thoát")
        
        choice = input("\nNhập lựa chọn của bạn: ")
        
        try:
            if choice == '1':
                display_data()
            elif choice == '2':
                print(add_new_record())
            elif choice == '3':
                print(update_record())
            elif choice == '4':
                print(delete_records())
            elif choice == '5':
                print(sort_data())
            elif choice == '6':
                search_data()
            elif choice == '7':
                show_statistics()
            elif choice == '0':
                print("Cảm ơn bạn đã sử dụng chương trình!")
                break
            else:
                print("Lựa chọn không hợp lệ!")
        except Exception as e:
            print(f"Có lỗi xảy ra: {str(e)}")
            print("Vui lòng thử lại!")
            
if __name__ == "__main__":
    main()