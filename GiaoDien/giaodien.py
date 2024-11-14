import streamlit as st
import pandas as pd
import numpy as np

class GiaoDien:
    def __init__(self):
        st.set_page_config(page_title="Dự đoán giá bảo hiểm y tế", layout="wide")

    def main(self):
        st.write(f'<h1 style="text-align:center;">Dự đoán giá bảo hiểm y tế</h1>', unsafe_allow_html=True)
        
        # Sidebar menu
        menu = st.sidebar.selectbox("Menu", ["Data List", "CRUD", "Charts"])
        
        if menu == "Data List":
            self.show_data_list()
        elif menu == "CRUD":
            self.show_create_form()
        else:
            self.show_charts()

    def show_data_list(self):
        st.header("Data List")
        
        # Initialize original and modified data in session_state if not already present
        if 'original_data' not in st.session_state:
            st.session_state.original_data = st.session_state.xu_ly.du_lieu.copy()
            st.session_state.modified_data = st.session_state.xu_ly.du_lieu.copy()
            st.session_state.modified_changes = pd.DataFrame(False, index=st.session_state.original_data.index, columns=st.session_state.original_data.columns)
        
        # Select data version to display (Original or Modified)
        data_version = st.selectbox("Select Data Version", ["Original", "Modified"])
        data = st.session_state.original_data if data_version == "Original" else st.session_state.modified_data

        # Search, Filter, and Sort functionality
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            # search = st.text_input("Search...")
            search = st.text_input("Search... ")
        with col2:
            filter_column = st.selectbox("Filter Column", [""] + list(data.columns))
        with col3:
            filter_operator = st.selectbox("Filter Operator", ["contains", "equals", "greater than", "less than"]) if filter_column else ""
        with col4:
            filter_value = st.text_input("Filter Value") if filter_operator == "contains" else st.number_input("Filter Value", step=1.0) if filter_operator else ""

        
        if search:
            data = data[data.apply(lambda row: row.astype(str).str.contains(search, case=False, na=False).any(), axis=1)]
        if filter_column and filter_operator and filter_value:
            if filter_operator == "contains":
                data = data[data[filter_column].astype(str).str.contains(filter_value, case=False)]
            elif filter_operator == "equals":
                data = data[data[filter_column] == float(filter_value)]
            elif filter_operator == "greater than":
                data = data[data[filter_column] > float(filter_value)]
            elif filter_operator == "less than":
                data = data[data[filter_column] < float(filter_value)]

        # Sort
        col1, col2 = st.columns(2)
        with col1:
            sort_column = st.selectbox("Sort By", [""] + list(data.columns))
        with col2:
            sort_ascending = st.checkbox("Sort Ascending", value=True) if sort_column else True
        if sort_column:
            data = data.sort_values(by=sort_column, ascending=sort_ascending)

        # Pagination
        items_per_page = 10
        total_pages = len(data) // items_per_page + (1 if len(data) % items_per_page > 0 else 0)
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
        end_idx = min(start_idx + items_per_page, len(data))

        # Highlight changes if viewing Modified data
        if data_version == "Modified":
            def highlight_changes(val):
                if st.session_state.modified_changes.loc[val.name].any():
                    return ['background-color: lightgreen' if st.session_state.modified_changes.loc[val.name, col] else '' for col in val.index]
                return ['' for _ in val.index]
            
            st.dataframe(data.iloc[start_idx:end_idx].style.apply(highlight_changes, axis=1), use_container_width=True)
            
            # Button to save modified data as new original
            if st.button("Save Modified Data"):
                st.session_state.original_data = st.session_state.modified_data.copy()
                st.session_state.modified_changes = pd.DataFrame(False, index=st.session_state.modified_data.index, columns=st.session_state.modified_data.columns)
                st.success("Modified data has been saved as the new original data.")
        else:
            # Display data without highlights
            st.dataframe(data.iloc[start_idx:end_idx], use_container_width=True)


    def show_create_form(self):
            st.header("Create/Update/Delete Data")
            df = st.session_state.modified_data
            
            # Chọn giữa tạo mới và cập nhật
            operation = st.radio("Choose Operation", ["Create New", "Update Existing", "Delete Multiple"])
            
            if operation == "Delete Multiple":
                # Checkbox for selecting multiple rows to delete
                st.write("Select rows to delete:")
                selected_indices = st.multiselect(
                    "Choose rows", options=df.index, 
                    format_func=lambda x: f"Record {x}: Age {df.iloc[x]['age']}, Region {df.iloc[x]['region']}"
                )
                
                # Button to confirm deletion
                if st.button("Delete Selected Rows") and selected_indices:
                    st.session_state.modified_data = df.drop(index=selected_indices).reset_index(drop=True)
                    st.session_state.modified_changes = st.session_state.modified_changes.drop(index=selected_indices).reset_index(drop=True)
                    st.success(f"Deleted {len(selected_indices)} selected records.")
            
            else:
                with st.form("create_form"):
                    if operation == "Update Existing":
                        index = st.selectbox("Select Record to Update/Delete", range(len(df)),
                                            format_func=lambda x: f"Record {x}: Age {df.iloc[x]['age']}, Region {df.iloc[x]['region']}")
                        current_record = df.iloc[index]
                        age = st.number_input("Age", min_value=0, max_value=100, value=int(current_record['age']))
                        sex = st.selectbox("Sex", ["male", "female"], index=0 if current_record['sex'] == 'male' else 1)
                        bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=float(current_record['bmi']))
                        children = st.number_input("Number of Children", min_value=0, max_value=10, value=int(current_record['children']))
                        smoker = st.selectbox("Smoker", ["yes", "no"], index=0 if current_record['smoker'] == 'yes' else 1)
                        region = st.selectbox("Region", ["southeast", "southwest", "northeast", "northwest"], 
                                            index=["southeast", "southwest", "northeast", "northwest"].index(current_record['region']))
                    else:
                        # Tạo mới với giá trị mặc định
                        age = st.number_input("Age", min_value=0, max_value=100, value=30)
                        sex = st.selectbox("Sex", ["male", "female"])
                        bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0)
                        children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)
                        smoker = st.selectbox("Smoker", ["yes", "no"])
                        region = st.selectbox("Region", ["southeast", "southwest", "northeast", "northwest"])

                    # Nút lưu hoặc xóa bản ghi
                    submitted = st.form_submit_button("Save")
                    delete_submitted = st.form_submit_button("Delete") if operation == "Update Existing" else None
                
                if submitted:
                    if operation == "Create New":
                        new_data = {
                            'age': age,
                            'sex': sex,
                            'bmi': bmi,
                            'children': children,
                            'smoker': smoker,
                            'region': region,
                            'charges': float(np.random.uniform(5000, 50000))
                        }
                        st.session_state.modified_data = pd.concat([st.session_state.modified_data, pd.DataFrame([new_data])], ignore_index=True)
                        st.session_state.modified_changes.loc[len(st.session_state.modified_data) - 1] = True
                        st.success("New record created successfully!")
                    else:
                        fields = {
                            'age': age,
                            'sex': sex,
                            'bmi': bmi,
                            'children': children,
                            'smoker': smoker,
                            'region': region
                        }
                        for column, value in fields.items():
                            original_value = st.session_state.original_data.at[index, column]
                            st.session_state.modified_data.at[index, column] = value
                            st.session_state.modified_changes.at[index, column] = (original_value != value)
                        st.success("Record updated successfully!")
                
                if delete_submitted:
                    st.session_state.modified_data = st.session_state.modified_data.drop(index).reset_index(drop=True)
                    st.session_state.modified_changes = st.session_state.modified_changes.drop(index).reset_index(drop=True)
                    st.success("Record deleted successfully!")


    def show_charts(self):
        st.header("Charts")
        
        # Chọn loại biểu đồ
        chart_type = st.selectbox("Select Chart Type", ["Distribution", "Relationships", "Correlation Analysis"])
        
        if chart_type == "Distribution":
            col1, col2 = st.columns(2)
            with col1:
                fig_age = st.session_state.truc_quan.ve_bieu_do_phan_phoi('age')
                st.plotly_chart(fig_age, use_container_width=True)
                
                fig_bmi = st.session_state.truc_quan.ve_bieu_do_phan_phoi('bmi')
                st.plotly_chart(fig_bmi, use_container_width=True)
            
            with col2:
                fig_smoker = st.session_state.truc_quan.ve_bieu_do_box('smoker', 'charges')
                st.plotly_chart(fig_smoker, use_container_width=True)
                
                fig_region = st.session_state.truc_quan.ve_bieu_do_box('region', 'charges')
                st.plotly_chart(fig_region, use_container_width=True)
                
        elif chart_type == "Relationships":
            col1, col2 = st.columns(2)
            with col1:
                fig_age_charges = st.session_state.truc_quan.ve_bieu_do_scatter('age', 'charges', 'smoker')
                st.plotly_chart(fig_age_charges, use_container_width=True)
            
            with col2:
                fig_bmi_charges = st.session_state.truc_quan.ve_bieu_do_scatter('bmi', 'charges', 'smoker')
                st.plotly_chart(fig_bmi_charges, use_container_width=True)
        
        else:
            fig_corr = st.session_state.truc_quan.ve_bieu_do_tuong_quan()
            st.plotly_chart(fig_corr, use_container_width=True)
