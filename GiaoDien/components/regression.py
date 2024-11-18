import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

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
            help="Chọn đặc trưng để phân tích mối quan hệ với giá bảo hiểm",
            key="feature_select"
        )
        
        group_type = st.selectbox(
            "Chọn loại nhóm:",
            ["smoker", "region"],
            help="Chọn tiêu chí phân nhóm dữ liệu",
            key="group_type_select"
        )

        if group_type == "smoker":
            group_value = st.radio(
                "Chọn nhóm đối tượng:",
                ["Người hút thuốc", "Người không hút thuốc"],
                horizontal=True,
                key="smoker_group"
            )
        else:
            group_value = st.radio(
                "Chọn khu vực:",
                ["southwest", "southeast", "northwest", "northeast"],
                horizontal=True,
                key="region_group"
            )
        
        regression_method = st.radio(
            "Chọn phương pháp hồi quy:",
            ["Thủ công", "Sử dụng hàm"],
            horizontal=True,
            key="regression_method"
        )

        if group_type == "smoker":
            filter_value = 'yes' if group_value == "Người hút thuốc" else 'no'
            df_filtered = self.phan_tich_va_du_doan.du_lieu[
                self.phan_tich_va_du_doan.du_lieu['smoker'] == filter_value
            ]
        else:
            df_filtered = self.phan_tich_va_du_doan.du_lieu[
                self.phan_tich_va_du_doan.du_lieu['region'] == group_value
            ]

        if regression_method == "Thủ công":
            if 'regression_params' not in st.session_state:
                st.session_state.regression_params = {
                    'a': 1.00,
                    'b': 0.00
                }

            col1, col2 = st.columns(2)
            
            with col1:
                a = st.number_input(
                    "Nhập hệ số a:",
                    value=float(st.session_state.regression_params['a']),
                    key="param_a"
                )
            
            with col2:
                b = st.number_input(
                    "Nhập hệ số b:",
                    value=float(st.session_state.regression_params['b']),
                    key="param_b"
                )
                
            st.session_state.regression_params['a'] = a
            st.session_state.regression_params['b'] = b

            if st.button("Vẽ biểu đồ", key="plot_button"):
                try:
                    self.phan_tich_va_du_doan.hoi_quy_tuyen_tinh_1_dac_trung_thu_cong(
                        feature, df_filtered, a, b
                    )
                except Exception as e:
                    st.error(f"Lỗi khi vẽ biểu đồ: {str(e)}")
        else:
            if st.button("Thực hiện phân tích", key="analyze_button"):
                try:
                    self.phan_tich_va_du_doan.hoi_quy_tuyen_tinh_1_dac_trung_su_dung_ham(
                        [feature], df_filtered
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
                    
