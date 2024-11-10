import pandas as pd

class XuLyDuLieu:
    """
    Class này thực hiện các bước xử lý và biến đổi dữ liệu.
    """

    def __init__(self, du_lieu):
        """
        Khởi tạo đối tượng XuLyDuLieu.

        Args:
          du_lieu: DataFrame chứa dữ liệu.
        """
        self.du_lieu = du_lieu

    def lam_sach_du_lieu(self):
        """
        Thay thế giá trị ngoại lai bằng giá trị trung bình.
        """
        for cot in ['Unit price', 'Quantity', 'Total']:  # Chọn các cột số cần xử lý
            Q1 = self.du_lieu[cot].quantile(0.25)
            Q3 = self.du_lieu[cot].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            self.du_lieu[cot] = self.du_lieu[cot].mask(
                (self.du_lieu[cot] < lower_bound) | (self.du_lieu[cot] > upper_bound), 
                self.du_lieu[cot].mean()
            )
    def doanh_thu_trung_binh_theo_loai_KH(self):
        # Doanh thu trung bình theo loại khách hàng
        return self.du_lieu.groupby('Customer type')['Total'].mean()

    def so_luong_san_pham_theo_dong_SP(self):
        # Số lượng sản phẩm bán ra theo dòng sản phẩm
        return self.du_lieu.groupby('Product line')['Quantity'].sum()

    def loi_nhuan_gop_trung_binh_theo_CN(self):
        # Lợi nhuận gộp trung bình theo chi nhánh
        return self.du_lieu.groupby('Branch')['gross income'].mean()
    
    def doanh_thu_trung_binh_theo_ngay(self):
        # Doanh thu trung bình theo ngày trong tuần
        return self.du_lieu.groupby('Date')['Total'].mean()
    
    def diem_danh_gia_trung_binh_theo_dong_SP(self):
        # Điểm đánh giá trung bình theo dòng sản phẩm
        return self.du_lieu.groupby('Product line')['Rating'].mean()
    
    def ty_le_khach_hang_theo_gioi_tinh(self):
        # Tỷ lệ khách hàng theo giới tính
        return self.du_lieu['Gender'].value_counts(normalize = True)*100
    
        
    def chuyen_doi_du_lieu(self):
        """
        Chuyển đổi dữ liệu sang định dạng phù hợp.
        """
        # Chuyển đổi cột 'Date' sang định dạng datetime
        if not pd.api.types.is_datetime64_any_dtype(self.du_lieu['Date']):
            self.du_lieu['Date'] = pd.to_datetime(self.du_lieu['Date'], errors='coerce')
        
        # Xử lý NaT nếu có
        self.du_lieu = self.du_lieu.dropna(subset=['Date'])

        # Chuyển đổi cột 'Gender' từ Male/Female sang 1/0
        self.du_lieu['Gender'] = self.du_lieu['Gender'].map({'Male': 1, 'Female': 0})
      