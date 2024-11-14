import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from DocDuLieu.docdulieu import *
class GiaoDien:
    def __init__(self):
        st.set_page_config(page_title="Dự đoán giá bảo hiểm y tế", layout="wide")
        
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
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            search = st.text_input("Search...")
        with col2:
            filter_column = st.selectbox("Filter Column", [""] + list(st.session_state.data.columns))
        with col3:
            if filter_column:
                filter_operator = st.selectbox("Filter Operator", ["contains", "equals", "greater than", "less than"])
            else:
                filter_operator = ""
        with col4:
            if filter_column and filter_operator:
                if filter_operator in ["equals", "greater than", "less than"]:
                    filter_value = st.number_input("Filter Value", step=1.0)
                else:
                    filter_value = st.text_input("Filter Value")
            else:
                filter_value = ""

        # Sort
        col1, col2 = st.columns(2)
        with col1:
            sort_column = st.selectbox("Sort By", [""] + list(st.session_state.data.columns))
        with col2:
            if sort_column:
                sort_ascending = st.checkbox("Sort Ascending", value=True)
            else:
                sort_ascending = True

        # Apply filters
        df = st.session_state.data.copy()
        if search:
            mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
            df = df[mask]

        if filter_column and filter_operator and filter_value:
            if filter_operator == "contains":
                df = df[df[filter_column].astype(str).str.contains(filter_value, case=False)]
            elif filter_operator == "equals":
                df = df[df[filter_column] == float(filter_value)]
            elif filter_operator == "greater than":
                df = df[df[filter_column] > float(filter_value)]
            elif filter_operator == "less than":
                df = df[df[filter_column] < float(filter_value)]

        # Sort
        if sort_column:
            df = df.sort_values(by=sort_column, ascending=sort_ascending)

        # Display data with pagination
        items_per_page = 10
        total_pages = len(df) // items_per_page + (1 if len(df) % items_per_page > 0 else 0)
        current_page = st.session_state.get("current_page", 1)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("Previous") and current_page > 1:
                st.session_state.current_page = current_page - 1
        with col2:
            st.write(f"Page {current_page} of {total_pages}")
        with col3:
            if st.button("Next") and current_page < total_pages:
                st.session_state.current_page = current_page + 1

        start_idx = (current_page - 1) * items_per_page
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
                "Phân bố chi phí y tế theo các yếu tố",
                "Phân bố theo giới tính và khu vực",
                "Mối quan hệ chi phí với các yếu tố khác"
            ]
        )
        
        if chart_type == "Phân bố chi phí y tế theo các yếu tố":
            self.show_cost_distribution_charts()
        elif chart_type == "Phân bố theo giới tính và khu vực":
            self.show_demographic_charts()
        else:
            self.show_correlation_charts()

    def show_cost_distribution_charts(self):
        col1, col2 = st.columns(2)
        
        with col1:
            # Phân bố tuổi
            fig = px.histogram(st.session_state.data, x='age',
                             title='Phân bố tuổi')
            st.plotly_chart(fig, use_container_width=True)

            # Phân bố BMI
            fig = px.histogram(st.session_state.data, x='bmi',
                             title='Phân bố BMI(Body Mass Index)',
                             color_discrete_sequence=['red'])
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Phí y tế theo người hút thuốc
            fig = px.histogram(st.session_state.data, x='charges',
                             color='smoker',
                             title='Phí y tế hàng năm',
                             color_discrete_sequence=['red', 'grey'])
            st.plotly_chart(fig, use_container_width=True)

            # Chi phí theo giới tính
            fig = px.histogram(st.session_state.data, x='charges',
                             color='sex',
                             title='Các khoản phí khác nhau về giới tính',
                             color_discrete_sequence=['blue', 'red'])
            st.plotly_chart(fig, use_container_width=True)

        # Chi phí theo khu vực
        fig = px.box(st.session_state.data, x='region', y='charges',
                    title='Chi phí trên các khu vực khác nhau của Hoa Kỳ')
        st.plotly_chart(fig, use_container_width=True)

    def show_demographic_charts(self):
        col1, col2 = st.columns(2)

        with col1:
            # Chi phí theo số lượng con
            fig = px.box(st.session_state.data, x='children', y='charges',
                        title='Chi phí phát sinh cho trẻ em')
            st.plotly_chart(fig, use_container_width=True)

            # Chi phí theo tuổi và người hút thuốc
            fig = px.scatter(st.session_state.data, x='age', y='charges',
                           color='smoker', opacity=0.8,
                           hover_data=['sex'],
                           title='Chi phí so với độ tuổi')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Chi phí theo BMI và người hút thuốc
            fig = px.scatter(st.session_state.data, x='bmi', y='charges',
                           color='smoker', opacity=0.8,
                           hover_data=['sex'],
                           title='Chi phí so với BMI')
            st.plotly_chart(fig, use_container_width=True)

    def show_correlation_charts(self):
        col1, col2 = st.columns(2)

        with col1:
            # Chi phí theo số lượng con (violin plot)
            fig = px.violin(st.session_state.data, x='children', y='charges',
                          title='Chi phí so với số lượng con cái')
            st.plotly_chart(fig, use_container_width=True)

            # Chi phí theo giới tính và người hút thuốc
            fig = px.box(st.session_state.data, x='sex', y='charges',
                        color='smoker',
                        title='Chi phí so với việc hút thuốc hay không hút thuốc theo giới tính')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Chi phí theo khu vực và giới tính
            fig = px.box(st.session_state.data, x='sex', y='charges',
                        color='region',
                        title='Chi phí so với vùng theo giới tính')
            st.plotly_chart(fig, use_container_width=True)

            # Ma trận tương quan
            corr_data = st.session_state.data[['age', 'bmi', 'children', 'charges']].corr()
            fig = px.imshow(corr_data,
                          title='Ma trận tương quan',
                          color_continuous_scale='RdBu')
            st.plotly_chart(fig, use_container_width=True)
if __name__ == "__main__":
    app = GiaoDien()
    app.main()