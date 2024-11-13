import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from DocDuLieu.docdulieu import *
class InsuranceApp:
    def __init__(self):
        st.set_page_config(page_title="Dự đoán giá bảo hiểm y tế", layout="wide")
        if 'data' not in st.session_state:
            # Tạo dữ liệu mẫu
            st.session_state.data = DuLieu("/Users/kotori/Documents/Code/python_code/tryagain/Python_fighting/Data/Health_insurance.csv").lay_du_lieu()

    def main(self):
        st.title("Dự đoán giá bảo hiểm y tế")
        
        # Sidebar navigation
        menu = st.sidebar.selectbox(
            "Menu",
            ["Data List", "Create New", "Charts"]
        )
        
        if menu == "Data List":
            self.show_data_list()
        elif menu == "Create New":
            self.show_create_form()
        else:
            self.show_charts()

    def show_data_list(self):
        st.header("Data List")
        
        # Search and Filter
        col1, col2, col3 = st.columns(3)
        with col1:
            search = st.text_input("Search...")
        with col2:
            filter_column = st.selectbox("Filter Column", st.session_state.data.columns)
        with col3:
            sort_column = st.selectbox("Sort By", st.session_state.data.columns)
        
        # Apply filters
        df = st.session_state.data.copy()
        if search:
            mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
            df = df[mask]
        
        # Sort
        df = df.sort_values(by=sort_column)
        
        # Display data with pagination
        items_per_page = 10
        total_pages = len(df) // items_per_page + (1 if len(df) % items_per_page > 0 else 0)
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            page = st.slider('Page', 1, max(1, total_pages), 1)
        
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(df))
        
        # Display data
        st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True)
        
        # Delete functionality
        if st.button("Delete Selected"):
            st.warning("Delete functionality would go here")

    def show_create_form(self):
        st.header("Create/Update Data")
        
        with st.form("create_form"):
            age = st.number_input("Age", min_value=0, max_value=100, value=30)
            bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0)
            children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)
            smoker = st.selectbox("Smoker", ["yes", "no"])
            region = st.selectbox("Region", ["southeast", "southwest", "northeast", "northwest"])
            
            submitted = st.form_submit_button("Save")
            
            if submitted:
                new_data = {
                    'id': len(st.session_state.data) + 1,
                    'age': age,
                    'bmi': bmi,
                    'children': children,
                    'smoker': smoker,
                    'region': region,
                    'charges': np.random.uniform(5000, 50000)  # Placeholder for predicted charges
                }
                st.session_state.data = pd.concat([
                    st.session_state.data,
                    pd.DataFrame([new_data])
                ], ignore_index=True)
                st.success("Data saved successfully!")

    def show_charts(self):
        st.header("Charts")
        
        chart_type = st.selectbox(
            "Select Chart Type",
            [
                "Biểu đồ Phân tích Dữ liệu Khám Phá (EDA)",
                "Biểu đồ Tương Quan và Mối Quan Hệ",
                "Biểu đồ Mô hình Hồi Quy",
                "Mức Độ Quan Trọng Của Các Biến"
            ]
        )
        
        if chart_type == "Biểu đồ Phân tích Dữ liệu Khám Phá (EDA)":
            self.show_eda_charts()
        elif chart_type == "Biểu đồ Tương Quan và Mối Quan Hệ":
            self.show_correlation_charts()
        elif chart_type == "Biểu đồ Mô hình Hồi Quy":
            self.show_regression_charts()
        else:
            self.show_feature_importance()

    def show_eda_charts(self):
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution
            fig = px.histogram(st.session_state.data, x='age', title='Age Distribution')
            st.plotly_chart(fig, use_container_width=True)
            
            # BMI distribution
            fig = px.histogram(st.session_state.data, x='bmi', title='BMI Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Charges by smoker
            fig = px.box(st.session_state.data, x='smoker', y='charges', title='Charges by Smoker Status')
            st.plotly_chart(fig, use_container_width=True)
            
            # Charges by region
            fig = px.box(st.session_state.data, x='region', y='charges', title='Charges by Region')
            st.plotly_chart(fig, use_container_width=True)

    def show_correlation_charts(self):
        # Scatter plot of Age vs Charges
        fig = px.scatter(st.session_state.data, x='age', y='charges', 
                        color='smoker', title='Age vs Charges by Smoker Status')
        st.plotly_chart(fig, use_container_width=True)
        
        # BMI vs Charges
        fig = px.scatter(st.session_state.data, x='bmi', y='charges',
                        color='smoker', title='BMI vs Charges by Smoker Status')
        st.plotly_chart(fig, use_container_width=True)

    def show_regression_charts(self):
        # Simple linear regression plot
        fig = px.scatter(st.session_state.data, x='age', y='charges',
                        trendline="ols", title='Age vs Charges (with trend line)')
        st.plotly_chart(fig, use_container_width=True)

    def show_feature_importance(self):
        # Simulated feature importance
        features = ['age', 'bmi', 'children', 'smoker', 'region']
        importance = np.random.uniform(0, 1, len(features))
        importance = importance / importance.sum()
        
        fig = px.bar(x=features, y=importance,
                    title='Feature Importance',
                    labels={'x': 'Features', 'y': 'Importance Score'})
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    app = InsuranceApp()
    app.main()