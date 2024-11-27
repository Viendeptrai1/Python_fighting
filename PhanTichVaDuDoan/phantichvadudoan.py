import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import streamlit as st

class PhanTichVaDuDoan:
    """
    Class này thực hiện các bước phân tích và dự đoán dữ liệu.
    """

    def __init__(self, du_lieu):
        """
        Khởi tạo đối tượng PhanTichVaDuDoan.

        Args:
          du_lieu: DataFrame chứa dữ liệu.
        """
        self.du_lieu = du_lieu
    
    def tinh_rmse(self, thuc_te, du_doan):
        """Tính toán Root Mean Square Error"""
        sai_so = thuc_te - du_doan
        sai_so_binh_phuong = sai_so ** 2
        trung_binh_sai_so_binh_phuong = np.mean(sai_so_binh_phuong)
        rmse = np.sqrt(trung_binh_sai_so_binh_phuong)
        return rmse

    def hoi_quy_tuyen_tinh_1_dac_trung_thu_cong(self, dac_trung, du_lieu, a, b):
        """Thực hiện hồi quy tuyến tính bằng thủ công"""
        def uoc_tinh_chi_phi(tmp, a, b):
            return a * tmp + b 

        # Kiểm tra dữ liệu đầu vào
        if dac_trung not in du_lieu.columns:
            raise ValueError(f"Đặc trưng '{dac_trung}' không tồn tại trong dữ liệu.")
        if du_lieu.empty:
            raise ValueError("Dữ liệu trống.")

        dau_vao_df = du_lieu[dac_trung]
        chi_phi_thuc_te_df = du_lieu['charges']
        chi_phi_duoc_uoc_tinh = uoc_tinh_chi_phi(dau_vao_df, a, b)

        plt.close('all')  
        plt.figure(figsize=(10, 6))

        # Vẽ biểu đồ
        plt.plot(dau_vao_df, chi_phi_duoc_uoc_tinh, 'r', alpha=0.9)
        plt.scatter(dau_vao_df, chi_phi_thuc_te_df, s=8, alpha=0.8)
        plt.xlabel(dac_trung)
        plt.ylabel('Charges')
        plt.legend(['Estimate', 'Actual'])

        equation_text = f'y = {a:.2f} * x + {b:.2f}' if b > 0 else f'y = {a:.2f} * x {b:.2f}'
        plt.text(0.05, 0.90, equation_text, 
                transform=plt.gca().transAxes, fontsize=12, 
                verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

        loss = self.tinh_rmse(chi_phi_thuc_te_df, chi_phi_duoc_uoc_tinh)
        plt.text(0.05, 0.95, f'RMSE Loss: {loss:.2f}',
                transform=plt.gca().transAxes, fontsize=12, 
                verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

        st.pyplot(plt.gcf())

    def hoi_quy_tuyen_tinh_1_dac_trung_su_dung_ham(self, dac_trung, du_lieu):
        model = LinearRegression()
        dau_vao_df = du_lieu[dac_trung].values.reshape(-1, 1)
        chi_phi_thuc_te_df = du_lieu['charges']
    
        model.fit(dau_vao_df, chi_phi_thuc_te_df)
    
        chi_phi_duoc_uoc_tinh = model.predict(dau_vao_df)
    
        plt.figure(figsize=(10, 6))
        plt.plot(dau_vao_df, chi_phi_duoc_uoc_tinh, 'r', alpha=0.9)
        plt.scatter(dau_vao_df, chi_phi_thuc_te_df, s=8, alpha=0.8)
        plt.xlabel(dac_trung)
        plt.ylabel('Charges')
        plt.legend(['Estimate', 'Actual'])

        a = model.coef_[0]
        b = model.intercept_
        equation_text = f'y = {a:.2f} * x + {b:.2f}' if b > 0 else f'y = {a:.2f} * x {b:.2f}'
        plt.text(0.05, 0.90, equation_text, 
                 transform=plt.gca().transAxes, fontsize=12, 
                 verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
        
        loss = self.tinh_rmse(chi_phi_thuc_te_df, chi_phi_duoc_uoc_tinh)
        plt.text(0.05, 0.95, f'RMSE Loss: {loss:.2f}',
                 transform=plt.gca().transAxes, fontsize=12, 
                 verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

        st.pyplot(plt.gcf())

    def hoi_quy_tuyen_tinh_nhieu_dac_trung_su_dung_ham(self, dac_trung, du_lieu):
        model = LinearRegression()
        dau_vao_df = du_lieu[dac_trung]
        chi_phi_thuc_te_df = du_lieu['charges']

        model.fit(dau_vao_df, chi_phi_thuc_te_df)

        chi_phi_duoc_uoc_tinh = model.predict(dau_vao_df)
        
        loss = self.tinh_rmse(chi_phi_thuc_te_df, chi_phi_duoc_uoc_tinh)
        for i, dac_trung_don in enumerate(dac_trung):
            fig = px.scatter(du_lieu, x=dac_trung_don, y='charges', color='smoker', color_discrete_sequence=['red','blue'], title=f'{dac_trung_don} vs Charges')
            
            a = model.coef_[i]
            b = model.intercept_
            fig.add_annotation(x=0.05, y=0.95,
                               xref='paper', yref='paper',
                               text=f'RMSE Loss: {loss:.2f}', showarrow=False, 
                               font=dict(size=12, color='black'), bgcolor='white', opacity=0.5)
            st.plotly_chart(fig)

    def du_doan(self, input_data):
        """
        Dự đoán giá bảo hiểm dựa trên dữ liệu đầu vào.
    
        Args:
            input_data (dict): Dictionary chứa thông tin người dùng với các key:
                - 'age': Tuổi
                - 'sex': Giới tính ('male'/'female')
                - 'bmi': Chỉ số BMI
                - 'children': Số con
                - 'smoker': Tình trạng hút thuốc ('yes'/'no')
                - 'region': Khu vực ('southwest'/'southeast'/'northwest'/'northeast')
    
        Returns:
            float: Giá bảo hiểm dự đoán
        """
        # Kiểm tra dữ liệu đầu vào
        required_fields = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
        for field in required_fields:
            if field not in input_data:
                raise ValueError(f"Thiếu trường dữ liệu: {field}")
    
        # Tạo DataFrame từ dữ liệu đầu vào
        input_df = pd.DataFrame([input_data])
    
        # Chuẩn bị dữ liệu huấn luyện
        X_train = self.du_lieu.copy()
        y_train = X_train.pop('charges')
    
        # Tiền xử lý dữ liệu
        # 1. Chuyển đổi categorical thành numerical
        categorical_columns = ['sex', 'smoker', 'region']
    
        # Tạo bản sao để tránh ảnh hưởng đến dữ liệu gốc
        X_train_encoded = X_train.copy()
        input_df_encoded = input_df.copy()
    
        for column in categorical_columns:
            # Lấy unique values từ cả training và input data
            unique_values = list(set(X_train[column].unique()) | set(input_df[column].unique()))
        
            # Tạo mapping
            value_to_int = {value: index for index, value in enumerate(unique_values)}
        
            # Áp dụng encoding
            X_train_encoded[column] = X_train[column].map(value_to_int)
            input_df_encoded[column] = input_df[column].map(value_to_int)
    
        # 2. Chuẩn hóa dữ liệu số
        numerical_columns = ['age', 'bmi', 'children']
    
        # Tính mean và std từ training data
        means = {}
        stds = {}
        for column in numerical_columns:
            means[column] = X_train[column].mean()
            stds[column] = X_train[column].std()
        
            # Chuẩn hóa
            X_train_encoded[column] = (X_train[column] - means[column]) / stds[column]
            input_df_encoded[column] = (input_df[column] - means[column]) / stds[column]
    
        # Huấn luyện mô hình
        model = LinearRegression()
        model.fit(X_train_encoded, y_train)
    
        # Dự đoán
        prediction = model.predict(input_df_encoded)
    
        # Trả về kết quả dự đoán
        return float(prediction[0])