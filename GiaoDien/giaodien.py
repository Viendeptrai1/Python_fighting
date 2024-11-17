import streamlit as st
import pandas as pd
from collections import deque
from .components.data_list import DataListComponent
from .components.change_history import ChangeHistoryComponent
from .components.crud_form import CRUDFormComponent
from .components.charts import ChartsComponent
from .components.regression import RegressionComponent
import random

class GiaoDien:
    def __init__(self, truc_quan_hoa, du_lieu, phan_tich_va_du_doan):
        st.set_page_config(
            page_title="Dự đoán giá bảo hiểm y tế",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        self._setup_theme()
        
        self.truc_quan_hoa = truc_quan_hoa
        self.du_lieu = du_lieu
        self.phan_tich_va_du_doan = phan_tich_va_du_doan
        
        self._initialize_session_state()
        
        self.data_list = DataListComponent(st.session_state)
        self.change_history = ChangeHistoryComponent(st.session_state)
        self.crud_form = CRUDFormComponent(st.session_state)
        self.charts = ChartsComponent(truc_quan_hoa, du_lieu)
        self.regression = RegressionComponent(phan_tich_va_du_doan)

    def _setup_theme(self):
        theme_css = """
        <style>
            .main-app {
                background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
                padding: 20px;
                border-radius: 10px;
            }
            
            .regression-section {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            
            .teachers-day {
                background: linear-gradient(135deg, #FFD700, #FFA500);
                color: #800080;
                font-family: 'Arial', sans-serif;
            }
            
            .flower {
                position: fixed;
                font-size: 24px;
                animation: flowerfall 6s linear infinite;
            }
            
            @keyframes flowerfall {
                0% { transform: translateY(-10px) rotate(0deg); }
                100% { transform: translateY(100vh) rotate(360deg); }
            }
        </style>
        """
        st.markdown(theme_css, unsafe_allow_html=True)

    def _initialize_session_state(self):
        if 'original_data' not in st.session_state:
            data = self.du_lieu.lay()
            if data is not None:
                st.session_state.original_data = data.copy()
                st.session_state.original_data.insert(0, 'ID', range(1, len(st.session_state.original_data) + 1))
                st.session_state.modified_data = st.session_state.original_data.copy()
                st.session_state.modified_changes = pd.DataFrame(
                    False, 
                    index=st.session_state.modified_data.index,
                    columns=st.session_state.modified_data.columns
                )
                st.session_state.deleted_records_queue = deque(maxlen=50)
                st.session_state.show_flowers = True
            else:
                st.error("Không thể đọc dữ liệu")

    def _render_flowers(self):
        if st.session_state.show_flowers:
            flowers = "".join([
                f'<div class="flower" style="left: {random.uniform(0, 100)}%; animation-delay: {random.uniform(0, 5)}s;">🌸</div>'
                for _ in range(20)
            ])
            st.markdown(flowers, unsafe_allow_html=True)

    def chay(self):
        st.write(
            '<h1 style="text-align:center;">📚 Dự đoán giá bảo hiểm y tế 👩‍🏫</h1>', 
            unsafe_allow_html=True
        )

        menu = st.sidebar.selectbox(
            "📋 Menu",
            ["Data List", "Change History", "CRUD", "Charts", "Phân tích hồi quy"]
        )

        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        ### 🎉 Chào mừng ngày Nhà giáo Việt Nam 20/11
        *"Không thầy đố mày làm nên"*
        
        👨‍🏫 Tri ân những người đã và đang cống hiến cho sự nghiệp trồng người
        """)
        
        show_flowers = st.sidebar.checkbox(
            "🌸 Hiệu ứng hoa rơi", 
            value=st.session_state.show_flowers
        )
        st.session_state.show_flowers = show_flowers
        
        self._render_flowers()

        with st.container():
            if menu == "Data List":
                self.data_list.xem_du_lieu()
            elif menu == "Change History":
                self.change_history.xem_lich_su()
            elif menu == "CRUD":
                self.crud_form.quan_ly()
            elif menu == "Charts":
                self.charts.ve_bieu_do()
            elif menu == "Phân tích hồi quy":
                self.regression.quan_ly()
