import streamlit as st

class RegressionComponent:
    def __init__(self, phan_tich_va_du_doan):
        self.phan_tich_va_du_doan = phan_tich_va_du_doan

    def ve_hoi_quy_va_du_doan(self):
        st.write("### 🔍 Phân tích hồi quy")
        
        analysis_type = st.radio(
            "Chọn loại phân tích:",
            ["Hồi quy một đặc trưng", "Hồi quy nhiều đặc trưng"],
            horizontal=True
        )

        if analysis_type == "Hồi quy một đặc trưng":
            self._single_feature_regression()
        else:
            self._multi_feature_regression()
            
        self._show_prediction_form()

    def _single_feature_regression(self):
        feature = st.selectbox(
            "Chọn đặc trưng phân tích:",
            ["age", "bmi", "children"],
            help="Chọn đặc trưng để phân tích mối quan hệ với giá bảo hiểm"
        )
        
        normalization_method = st.selectbox(
            "Chọn phương pháp chuẩn hóa:",
            ["standard", "minmax"],
            help="Standard: chuẩn hóa về phân phối chuẩn, MinMax: chuẩn hóa về khoảng [0,1]"
        )
        
        if st.button("Thực hiện phân tích"):
            try:
                self.phan_tich_va_du_doan.hoi_quy_tuyen_tinh_1_dac_trung_su_dung_ham(
                    feature, 
                    self.phan_tich_va_du_doan.du_lieu,
                    normalization_method
                )
            except Exception as e:
                st.error(f"Lỗi khi thực hiện phân tích: {str(e)}")

    def _multi_feature_regression(self):
        if st.button("Thực hiện phân tích"):
            try:
                self.phan_tich_va_du_doan.hoi_quy_tuyen_tinh_nhieu_dac_trung_su_dung_ham(
                    ['age', 'bmi', 'children'],
                    self.phan_tich_va_du_doan.du_lieu
                )
            except Exception as e:
                st.error(f"Lỗi khi thực hiện phân tích: {str(e)}")

    def _show_prediction_form(self):
        st.write("### 🎯 Dự đoán giá bảo hiểm")
        with st.form("prediction_form"):
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

            if st.form_submit_button("Dự đoán"):
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
                except Exception as e:
                    st.error(f"Lỗi khi dự đoán: {str(e)}")
                    
