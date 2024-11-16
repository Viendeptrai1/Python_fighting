import streamlit as st
import pandas as pd
from collections import deque

class ChangeHistoryComponent:
    def __init__(self, session_state):
        self.session_state = session_state
        if 'change_history' not in self.session_state:
            self.session_state.change_history = deque(maxlen=50)

    def xem_lich_su(self):
        st.header("Change History")

        if not self.session_state.change_history:
            st.info("Chưa có thay đổi nào được ghi nhận.")
            return

        # Hiển thị lịch sử thay đổi theo thời gian
        for i, change in enumerate(reversed(self.session_state.change_history)):
            with st.expander(f"Change #{len(self.session_state.change_history) - i}", expanded=i == 0):
                self._display_change(change)

    def _display_change(self, change):
        """Hiển thị chi tiết một thay đổi"""
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write("**Type:**")
            st.write("**Time:**")
            st.write("**Details:**")
        
        with col2:
            # Hiển thị loại thay đổi với icon và màu sắc
            if change['type'] == 'add':
                st.markdown("🟢 **Added Record**")
            elif change['type'] == 'update':
                st.markdown("🟡 **Updated Record**")
            elif change['type'] == 'delete':
                st.markdown("🔴 **Deleted Record**")
            
            st.write(change['time'])
            
            # Hiển thị chi tiết thay đổi
            if change['type'] == 'add':
                self._display_added_record(change['data'])
            elif change['type'] == 'update':
                self._display_updated_record(change['old_data'], change['new_data'])
            elif change['type'] == 'delete':
                self._display_deleted_record(change['data'])

    def _display_added_record(self, data):
        """Hiển thị bản ghi mới thêm"""
        st.dataframe(
            pd.DataFrame([data]).style.apply(
                lambda _: ['background-color: lightgreen'] * len(data),
                axis=1
            ),
            hide_index=True
        )

    def _display_updated_record(self, old_data, new_data):
        """Hiển thị bản ghi được cập nhật"""
        st.write("Old values:")
        st.dataframe(pd.DataFrame([old_data]), hide_index=True)
        
        st.write("New values:")
        df = pd.DataFrame([new_data])
        
        def highlight_changes(row):
            return [
                'background-color: lightyellow' 
                if old_data.get(col) != new_data.get(col) else ''
                for col in df.columns
            ]
        
        st.dataframe(
            df.style.apply(highlight_changes, axis=1),
            hide_index=True
        )

    def _display_deleted_record(self, data):
        """Hiển thị bản ghi bị xóa"""
        st.dataframe(
            pd.DataFrame([data]).style.apply(
                lambda _: ['background-color: lightcoral'] * len(data),
                axis=1
            ),
            hide_index=True
        )

    def add_change(self, change_type, data, old_data=None, new_data=None):
        """Thêm một thay đổi vào lịch sử"""
        change = {
            'type': change_type,
            'time': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            'data': data
        }
        
        if change_type == 'update':
            change['old_data'] = old_data
            change['new_data'] = new_data
            
        self.session_state.change_history.append(change)