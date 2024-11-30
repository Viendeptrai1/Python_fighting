import streamlit as st
from XuLyDuLieu.CRUD import CRUD
from .change_history import ChangeHistoryComponent
import time
class CRUDFormComponent:
    def __init__(self, session_state):
        self.session_state = session_state
        self.crud = CRUD(self.session_state.modified_data)
        self.change_history = ChangeHistoryComponent(session_state)
        if 'show_success_message' not in self.session_state:
            self.session_state.show_success_message = None

    def quan_ly(self):
        st.header("Create/Update/Delete Data")
        operation = st.radio("Choose Operation", ["Create New", "Update Existing", "Delete Multiple"])

        if operation == "Create New":
            self._create_new_record()
        elif operation == "Update Existing":
            self._update_record()
        else:  # Delete Multiple
            self._delete_records()

        # Thêm trạng thái xác nhận vào session state nếu chưa có
        if 'confirm_save' not in st.session_state:
            st.session_state.confirm_save = False
            
        # Nút lưu chính
        if st.button("Lưu vào dữ liệu gốc"):
            st.session_state.confirm_save = True
            
        # Hiển thị dialog xác nhận khi đã bấm nút lưu
        if st.session_state.confirm_save:
            st.warning("⚠️ Bạn có chắc muốn lưu các thay đổi vào dữ liệu gốc?")
            
            col1, col2 = st.columns([1,1])
            
            with col1:
                if st.button("✔️ Xác nhận"):
                    try:
                        # Cập nhật dữ liệu gốc
                        st.session_state.du_lieu.du_lieu = st.session_state.modified_data
                        st.session_state.du_lieu.luu()
                        
                        # Cập nhật session state
                        st.session_state.original_data = st.session_state.modified_data.copy()
                        
                        # Hiển thị thông báo thành công
                        st.success("✅ Đã lưu thành công vào dữ liệu gốc!")
                        
                        # Reset trạng thái xác nhận
                        st.session_state.confirm_save = False
                        
                        # Tự động refresh sau 2s
                        time.sleep(2)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Lỗi khi lưu dữ liệu: {str(e)}")
                        st.session_state.confirm_save = False
                        
            with col2:
                if st.button("❌ Hủy"):
                    st.session_state.confirm_save = False
                    st.rerun()
                    

    def _create_new_record(self):
        with st.form("create_form"):
            cols = st.columns(3)
            with cols[0]:
                age = st.number_input("Age", min_value=18, max_value=100, value=30)
                bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0)
            with cols[1]:
                sex = st.selectbox("Sex", ["male", "female"])
                smoker = st.selectbox("Smoker", ["yes", "no"])
            with cols[2]:
                children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)
                region = st.selectbox("Region", ["southeast", "southwest", "northeast", "northwest"])

            charges = st.number_input("Charges", min_value=0.0, value=5000.0, step=100.0, format="%.4f")
            submitted = st.form_submit_button("Add Record")

        if submitted:
            new_record = {
                'age': age,
                'sex': sex,
                'bmi': bmi,
                'children': children,
                'smoker': smoker,
                'region': region,
                'charges': charges
            }

            try:
                new_df = self.crud.them(new_record)
                self.session_state.modified_data = new_df
                
                self.change_history.add_change(
                    change_type='add',
                    data=new_record
                )
                
                self.session_state.show_success_message = "Thêm bản ghi mới thành công!"
                self._show_success_message("Thêm bản ghi mới thành công!")
                
            except Exception as e:
                st.error(f"Lỗi khi thêm bản ghi: {str(e)}")

    def _update_record(self):
        df = self.session_state.modified_data
        index = st.selectbox(
            "Select Record to Update",
            df.index,
            format_func=lambda x: f"Record {x + 1}: Age {df.iloc[x]['age']}, Region {df.iloc[x]['region']}"
        )

        if index is not None:
            current_record = df.loc[index]
            with st.form("update_form"):
                cols = st.columns(3)
                with cols[0]:
                    age = st.number_input("Age", min_value=0, max_value=100, value=int(current_record['age']))
                    bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=float(current_record['bmi']))
                with cols[1]:
                    sex = st.selectbox("Sex", ["male", "female"], index=0 if current_record['sex'] == 'male' else 1)
                    smoker = st.selectbox("Smoker", ["yes", "no"], index=0 if current_record['smoker'] == 'yes' else 1)
                with cols[2]:
                    children = st.number_input("Number of Children", min_value=0, max_value=10, value=int(current_record['children']))
                    region = st.selectbox(
                        "Region",
                        ["southeast", "southwest", "northeast", "northwest"],
                        index=["southeast", "southwest", "northeast", "northwest"].index(current_record['region'])
                    )

                charges = st.number_input("Charges", min_value=0.0, value=float(current_record['charges']), step=100.0)
                submitted = st.form_submit_button("Update Record")

            if submitted:
                updated_record = {
                    'age': age,
                    'sex': sex,
                    'bmi': bmi,
                    'children': children,
                    'smoker': smoker,
                    'region': region,
                    'charges': charges
                }

                try:
                    old_record = df.loc[index].to_dict()
                    new_df = self.crud.sua(index, updated_record)
                    self.session_state.modified_data = new_df
                    
                    self.change_history.add_change(
                        change_type='update',
                        data=updated_record,
                        old_data=old_record,
                        new_data=updated_record
                    )
                    self.session_state.show_success_message = "Cập nhật bản ghi thành công!"
                    self._show_success_message("Cập nhật bản ghi thành công!")
                    
                except Exception as e:
                    st.error(f"Lỗi khi cập nhật bản ghi: {str(e)}")

    def _delete_records(self):
        df = self.session_state.modified_data
        selected_indices = st.multiselect(
            "Choose records to delete",
            options=df.index,
            format_func=lambda x: f"Record {x + 1}: Age {df.iloc[x]['age']}, Region {df.iloc[x]['region']}"
        )

        if st.button("Delete Selected Records"):
            if selected_indices:
                try:
                    for idx in selected_indices:
                        deleted_record = df.loc[idx].to_dict()
                        self.session_state.deleted_records_queue.append(deleted_record)
                        self.change_history.add_change(
                            change_type='delete',
                            data=deleted_record
                        )

                    new_df = self.crud.xoa(selected_indices)
                    self.session_state.modified_data = new_df
                    
                    self.session_state.show_success_message = f"Đã xóa {len(selected_indices)} bản ghi!"
                    self._show_success_message(f"Đã xóa {len(selected_indices)} bản ghi!")
                    
                except Exception as e:
                    st.error(f"Lỗi khi xóa bản ghi: {str(e)}")
            else:
                st.warning("Vui lòng chọn ít nhất một bản ghi để xóa.")

    def _show_success_message(self, message):
        if self.session_state.show_success_message == message:
            col1, col2 = st.columns([10,1])
            with col1:
                st.success(message)
            with col2:
                if st.button("✖"):
                    self.session_state.show_success_message = None
                    st.rerun()