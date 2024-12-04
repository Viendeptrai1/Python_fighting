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
        
        # Thêm lựa chọn phân nhóm
        group_by = st.checkbox("Phân tích theo nhóm", 
                             help="Chọn để phân tích riêng cho từng nhóm đối tượng")
        
        if group_by:
            group_type = st.selectbox(
                "Chọn loại nhóm:",
                ["smoker", "region"],
                help="Chọn tiêu chí phân nhóm dữ liệu"
            )

            if group_type == "smoker":
                group_value = st.radio(
                    "Chọn nhóm đối tượng:",
                    ["Người hút thuốc", "Người không hút thuốc"],
                    horizontal=True
                )
                filter_value = 'yes' if group_value == "Người hút thuốc" else 'no'
                du_lieu = self.phan_tich_va_du_doan.du_lieu[
                    self.phan_tich_va_du_doan.du_lieu['smoker'] == filter_value
                ]
            else:
                group_value = st.radio(
                    "Chọn khu vực:",
                    ["southwest", "southeast", "northwest", "northeast"],
                    horizontal=True
                )
                du_lieu = self.phan_tich_va_du_doan.du_lieu[
                    self.phan_tich_va_du_doan.du_lieu['region'] == group_value
                ]
        else:
            du_lieu = self.phan_tich_va_du_doan.du_lieu
        
        is_manual = st.checkbox("Sử dụng hồi quy thủ công", 
                              help="Chọn để nhập hệ số a, b thủ công")
        
        if is_manual:
            col1, col2 = st.columns(2)
            with col1:
                a = st.number_input("Hệ số a", value=1.0)
            with col2:
                b = st.number_input("Hệ số b", value=0.0)
        else:
            normalization_method = st.selectbox(
                "Chọn phương pháp chuẩn hóa:",
                ["standard", "minmax"],
                help="Standard: chuẩn hóa về phân phối chuẩn, MinMax: chuẩn hóa về khoảng [0,1]"
            )
        
        if st.button("Thực hiện phân tích"):
            try:
                if is_manual:
                    self.phan_tich_va_du_doan.hoi_quy_tuyen_tinh_1_dac_trung_thu_cong(
                        feature,
                        du_lieu,
                        a, b
                    )
                else:
                    self.phan_tich_va_du_doan.hoi_quy_tuyen_tinh_1_dac_trung_su_dung_ham(
                        feature,
                        du_lieu,
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
                    
