import pandas as pd  

class DataHandler:  
    def __init__(self, file_path):  
        self.file_path = file_path  
        self.data = self.load_data()  

    def load_data(self):  
        """Đọc dữ liệu từ file CSV."""  
        return pd.read_csv(self.file_path)  

    def create_entry(self, new_data):  
        """Thêm một hàng dữ liệu mới."""  
        new_df = pd.DataFrame([new_data])  # Chuyển đổi new_data thành DataFrame  
        self.data = pd.concat([self.data, new_df], ignore_index=True)  # Kết hợp với dữ liệu hiện tại  

    def read_data(self):  
        """Đọc và hiển thị dữ liệu."""  
        return self.data  

    def update_entry(self, invoice_id, updates):  
        """Cập nhật thông tin cho một hàng theo Invoice ID."""  
        for key, value in updates.items():  
            self.data.loc[self.data['Invoice ID'] == invoice_id, key] = value  

    def delete_entry(self, invoice_id):  
        """Xóa một hàng theo Invoice ID."""  
        self.data = self.data[self.data['Invoice ID'] != invoice_id]  

    def clean_data(self):  
        """Làm sạch dữ liệu (thay đổi theo yêu cầu cụ thể)."""  
        self.data.dropna(inplace=True)  # Ví dụ: xóa hàng có giá trị thiếu  

    def save_data(self, output_path):  
        """Lưu dữ liệu vào file mới."""  
        self.data.to_csv(output_path, index=False)

# Ví dụ sử dụng  
if __name__ == "__main__":  
    file_path = 'Data/data_sales.csv'    
    output_path = 'Data/new_data.csv'    

    handler = DataHandler(file_path)  

    # Thêm dữ liệu mới  
    new_data = {  
        'Invoice ID': '999-99-9999',  
        'Branch': 'A',  
        'City': 'Yangon',  
        'Customer type': 'Member',  
        'Gender': 'Female',  
        'Product line': 'Health and beauty',  
        'Unit price': 55.00,  
        'Quantity': 5,  
        'Tax 5%': 2.75,  
        'Total': 282.75,  
        'Date': '3/10/2019',  
        'Time': '10:30',  
        'Payment': 'Cash',  
        'cogs': 275.00,  
        'gross margin percentage': 4.761904762,  
        'gross income': 7.75,  
        'Rating': 9.0  
    }  
    handler.create_entry(new_data)  

    # Đọc và hiển thị dữ liệu  
    print(handler.read_data())  

    # Cập nhật thông tin  
    handler.update_entry('999-99-9999', {'Quantity': 6, 'Total': 330.00})  

    # Xóa dữ liệu  
    handler.delete_entry('999-99-9999')  

    # Làm sạch dữ liệu  
    handler.clean_data()  

    # Lưu dữ liệu sạch vào file mới  
    handler.save_data(output_path)