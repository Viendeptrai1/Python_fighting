import streamlit as st

class RegressionComponent:
    def __init__(self, phan_tich_va_du_doan):
        self.phan_tich_va_du_doan = phan_tich_va_du_doan

    def ve_hoi_quy(self):
        if self.phan_tich_va_du_doan.du_lieu is None:
            st.error("Không có dữ liệu để phân tích")
            return
        
        st.header("Phân tích hồi quy tuyến tính")
        
        # Chọn đặc trưng cho mô hình
        st.write("### 1. Chọn các đặc trưng cho mô hình")
        
        col1, col2 = st.columns(2)
        with col1:
            use_numeric = st.checkbox("Các đặc trưng số", value=True)
            if use_numeric:
                numeric_features = st.multiselect(
                    "Chọn đặc trưng số:",
                    self.phan_tich_va_du_doan.dac_trung_so,
                    default=self.phan_tich_va_du_doan.dac_trung_so
                )
            else:
                numeric_features = []
                
        with col2:
            use_categorical = st.checkbox("Các đặc trưng phân loại", value=True)
            if use_categorical:
                categorical_features = st.multiselect(
                    "Chọn đặc trưng phân loại:",
                    self.phan_tich_va_du_doan.dac_trung_nhi_phan + ['region'],
                    default=['smoker', 'region']
                )
            else:
                categorical_features = []
        
        selected_features = numeric_features + categorical_features
        
        if not selected_features:
            st.warning("Vui lòng chọn ít nhất một đặc trưng")
            return
                
        # Thực hiện phân tích hồi quy
        if st.button("Phân tích hồi quy"):
            try:
                with st.spinner("Đang phân tích..."):
                    results = self.phan_tich_va_du_doan.phan_tich(selected_features)
                    
                    # Hiển thị kết quả
                    self.phan_tich_va_du_doan.ve_ket_qua(
                        results,
                        dac_trung=numeric_features[0] if numeric_features else None
                    )
                    
                    st.success("Phân tích hồi quy hoàn tất!")
                    
            except Exception as e:
                st.error(f"Lỗi khi thực hiện phân tích hồi quy: {str(e)}")
                return
                    
        # Công cụ dự đoán
        if self.phan_tich_va_du_doan.mo_hinh is not None:
            st.write("### 2. Dự đoán giá bảo hiểm")
            st.write("Nhập thông tin để dự đoán giá bảo hiểm:")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                age = st.number_input("Tuổi", min_value=18, max_value=100, value=30)
                sex = st.selectbox("Giới tính", ['male', 'female'])
            with col2:
                bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0)
                smoker = st.selectbox("Hút thuốc", ['no', 'yes'])
            with col3:
                children = st.number_input("Số con", min_value=0, max_value=10, value=0)
                region = st.selectbox("Khu vực", ['southwest', 'southeast', 'northwest', 'northeast'])
                
            if st.button("Dự đoán"):
                try:
                    input_data = {
                        'age': age,
                        'sex': sex,
                        'bmi': bmi,
                        'children': children,
                        'smoker': smoker,
                        'region': region
                    }
                    prediction = self.phan_tich_va_du_doan.du_doan(input_data)
                    
                    st.success(f"Giá bảo hiểm dự đoán: ${prediction:,.2f}")
                    
                    st.info("""
                    **Lưu ý về kết quả dự đoán:**
                    - Kết quả dự đoán dựa trên mô hình hồi quy tuyến tính
                    - Độ chính xác phụ thuộc vào các đặc trưng được chọn
                    - Giá trị thực tế có thể khác với dự đoán
                    """)
                    
                except Exception as e:
                    st.error(f"Lỗi khi dự đoán: {str(e)}")