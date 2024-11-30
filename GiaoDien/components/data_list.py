import streamlit as st

class DataListComponent:
    def __init__(self, session_state):
        self.session_state = session_state

    def xem_du_lieu(self):
        if not hasattr(self.session_state, 'original_data') or self.session_state.original_data is None:
            st.error("Không có dữ liệu để hiển thị")
            return

        st.header("Data List")

        # Lựa chọn dữ liệu để hiển thị
        data_version = st.selectbox("Select Data Version", ["Original", "Modified"])
        data = self.session_state.original_data if data_version == "Original" else self.session_state.modified_data

        # Tạo container cho các bộ lọc
        with st.expander("Search and Filter Options", expanded=True):
            # Tìm kiếm nâng cao
            col1, col2 = st.columns(2)
            with col1:
                search_type = st.radio("Search Type", ["Simple", "Advanced"])
                
            with col2:
                if search_type == "Simple":
                    search = st.text_input("Search in all columns...")
                    if search:
                        mask = data.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
                        data = data[mask]
                else:
                    search_col = st.selectbox("Search in column", [""] + list(data.columns))
                    if search_col:
                        search = st.text_input(f"Search in {search_col}...")
                        if search:
                            mask = data[search_col].astype(str).str.contains(search, case=False, na=False)
                            data = data[mask]

            # Bộ lọc nâng cao
            st.write("Advanced Filters")
            col1, col2, col3 = st.columns(3)
            
            filters = []
            for i in range(3):  # Cho phép tối đa 3 bộ lọc cùng lúc
                with locals()[f'col{i+1}']:
                    filter_col = st.selectbox(f"Filter Column {i+1}", [""] + list(data.columns), key=f'filter_col_{i}')
                    if filter_col:
                        filter_op = st.selectbox(
                            f"Operator {i+1}",
                            ["equals", "not equals", "greater than", "less than", "contains", "not contains"],
                            key=f'filter_op_{i}'
                        )
                        filter_val = st.text_input(f"Value {i+1}", key=f'filter_val_{i}')
                        if filter_val:
                            filters.append((filter_col, filter_op, filter_val))

            # Áp dụng các bộ lọc
            for col, op, val in filters:
                try:
                    if op in ["equals", "not equals", "greater than", "less than"]:
                        try:
                            numeric_val = float(val)
                            if op == "equals":
                                data = data[data[col] == numeric_val]
                            elif op == "not equals":
                                data = data[data[col] != numeric_val]
                            elif op == "greater than":
                                data = data[data[col] > numeric_val]
                            elif op == "less than":
                                data = data[data[col] < numeric_val]
                        except ValueError:
                            if op == "equals":
                                data = data[data[col].astype(str) == val]
                            elif op == "not equals":
                                data = data[data[col].astype(str) != val]
                    else:
                        if op == "contains":
                            data = data[data[col].astype(str).str.contains(val, case=False, na=False)]
                        elif op == "not contains":
                            data = data[~data[col].astype(str).str.contains(val, case=False, na=False)]
                except Exception as e:
                    st.warning(f"Error applying filter on {col}: {str(e)}")

        # Sắp xếp dữ liệu
        with st.expander("Sort Options", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                sort_col1 = st.selectbox("Sort by", [""] + list(data.columns), key='sort1')
            with col2:
                sort_col2 = st.selectbox("Then by", [""] + list(data.columns), key='sort2')
            with col3:
                ascending1 = st.checkbox("Ascending", value=True, key='asc1')
                if sort_col2:
                    ascending2 = st.checkbox("Ascending (2nd)", value=True, key='asc2')

            if sort_col1:
                sort_cols = [col for col in [sort_col1, sort_col2] if col]
                ascending = [ascending1]
                if sort_col2:
                    ascending.append(ascending2)
                data = data.sort_values(by=sort_cols, ascending=ascending)

        # Hiển thị thống kê cơ bản
        st.write(f"Showing {len(data)} records")
        
        # Phân trang
        items_per_page = st.select_slider("Items per page", options=[10, 20, 50, 100], value=10)
        total_pages = max(1, len(data) // items_per_page + (1 if len(data) % items_per_page > 0 else 0))
        
        col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
        with col1:
            if st.button("◀️"):
                self.session_state.current_page = max(1, self.session_state.get("current_page", 1) - 1)
        with col2:
            current_page = st.slider("Page", min_value=1, max_value=max(2, total_pages), 
                                   value=self.session_state.get("current_page", 1))
            self.session_state.current_page = current_page
        with col3:
            if st.button("▶️"):
                self.session_state.current_page = min(total_pages, self.session_state.get("current_page", 1) + 1)
        with col4:
            st.write(f"Total: {total_pages}")

        start_idx = (current_page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(data))

        # Hiển thị dữ liệu với màu sắc và định dạng
        if data_version == "Modified":
            def highlight_changes(row):
                row_idx = row.name
                if row_idx >= len(self.session_state.modified_changes):
                    return ['background-color: lightcoral'] * len(row)
                elif self.session_state.modified_changes.iloc[row_idx].any():
                    return ['background-color: lightyellow'] * len(row)
                return [''] * len(row)

            # Định dạng số và tiền tệ
            def format_data(val):
                if isinstance(val, (int, float)):
                    if isinstance(val, float):
                        return f"{val:,.4f}"
                    return f"{val:,}"
                return val

            # Chỉ hiển thị cột ID và các cột dữ liệu
            display_columns = ['ID'] + [col for col in data.columns if col != 'ID']
            styled_data = (data.iloc[start_idx:end_idx][display_columns]  # Chọn và sắp xếp lại các cột
                          .style
                          .apply(highlight_changes, axis=1)
                          .format(format_data))
            
            st.dataframe(styled_data, use_container_width=True, hide_index=True)
        else:
            # Chỉ hiển thị cột ID và các cột dữ liệu cho dữ liệu gốc
            display_columns = ['ID'] + [col for col in data.columns if col != 'ID']
            st.dataframe(data.iloc[start_idx:end_idx][display_columns], use_container_width=True, hide_index=True)

        # Export options
        if st.button("Export to CSV"):
            csv = data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="insurance_data.csv",
                mime="text/csv"
            )