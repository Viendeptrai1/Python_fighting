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
        # Thiết lập giao diện trước
        st.set_page_config(
            page_title="Dự đoán giá bảo hiểm y tế",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Thêm CSS cho theme ngày Nhà giáo
        teachers_day_css = """
        <style>
            /* CSS cho theme 20/11 */
            .teachers-day {
                background: linear-gradient(135deg, #FFD700, #FFA500);
                color: #800080;
                font-family: 'Arial', sans-serif;
            }
            
            .teachers-day .stButton button {
                background-color: #9370DB;
                color: white;
                border: 2px solid #800080;
                border-radius: 20px;
            }
            
            .teachers-day .stSelectbox {
                background-color: #DDA0DD;
                color: #800080;
            }
            
            .teachers-day h1, .teachers-day h2, .teachers-day h3 {
                color: #800080;
                text-shadow: 2px 2px 4px #FFD700;
            }
            
            /* Hiệu ứng hoa rơi */
            @keyframes flowerfall {
                0% { transform: translateY(-10px) rotate(0deg); }
                100% { transform: translateY(100vh) rotate(360deg); }
            }
            
            .flower {
                position: fixed;
                font-size: 24px;
                animation: flowerfall 6s linear infinite;
            }
            
            /* Hiệu ứng viền cho dataframe */
            .teachers-day .dataframe {
                border: 2px solid #800080;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(128, 0, 128, 0.3);
            }
        </style>
        """
        st.markdown(teachers_day_css, unsafe_allow_html=True)

        # Khởi tạo trạng thái hoa rơi trong session_state nếu chưa có
        if 'show_flowers' not in st.session_state:
            st.session_state.show_flowers = True

        # Sau đó mới khởi tạo các thuộc tính
        self.truc_quan_hoa = truc_quan_hoa
        self.du_lieu = du_lieu
        self.phan_tich_va_du_doan = phan_tich_va_du_doan
        
        # Tiếp theo là khởi tạo session_state
        self._initialize_session_state()
        
        # Cuối cùng mới khởi tạo các components
        self.data_list = DataListComponent(st.session_state)
        self.change_history = ChangeHistoryComponent(st.session_state)
        self.crud_form = CRUDFormComponent(st.session_state)
        self.charts = ChartsComponent(truc_quan_hoa, du_lieu)
        self.regression = RegressionComponent(phan_tich_va_du_doan)

    def _initialize_session_state(self):
        """Khởi tạo các giá trị trong session state"""
        if 'original_data' not in st.session_state:
            data = self.du_lieu.lay()
            if data is not None:
                st.session_state.original_data = data.copy()
                
                # Kiểm tra và thêm cột ID nếu chưa tồn tại
                if 'ID' not in st.session_state.original_data.columns:
                    st.session_state.original_data.insert(0, 'ID', range(1, len(st.session_state.original_data) + 1))
                
                # Khởi tạo các session state khác
                st.session_state.modified_data = st.session_state.original_data.copy()
                st.session_state.modified_changes = pd.DataFrame(
                    False, 
                    index=st.session_state.modified_data.index,
                    columns=st.session_state.modified_data.columns
                )
                st.session_state.deleted_records_queue = deque(maxlen=50)
            else:
                st.error("Không thể đọc dữ liệu")
                return

    def chay(self):
        st.write(f'<h1 style="text-align:center;">📚 Dự đoán giá bảo hiểm y tế 👩‍🏫</h1>', unsafe_allow_html=True)

        # Menu sidebar với icon giáo dục
        menu = st.sidebar.selectbox(
            "📋 Menu",
            ["Data List", "Change History", "CRUD", "Charts", "Xem hồi quy"]
        )

        # Thêm thông điệp ngày Nhà giáo và nút bật/tắt hoa rơi
        st.sidebar.markdown("""
        ---
        ### 🎉 Chào mừng ngày Nhà giáo Việt Nam 20/11
        *"Không thầy đố mày làm nên"*
        
        👨‍🏫 Tri ân những người đã và đang cống hiến cho sự nghiệp trồng người
        """)
        
        # Nút bật/tắt hoa rơi
        show_flowers = st.sidebar.checkbox("🌸 Hiệu ứng hoa rơi", value=st.session_state.show_flowers)
        st.session_state.show_flowers = show_flowers

        # Thêm hiệu ứng hoa rơi nếu được bật
        if show_flowers:
            flowers = "".join([
                f'<div class="flower" style="left: {random.uniform(0, 100)}%; animation-delay: {random.uniform(0, 5)}s;">🌸</div>'
                for _ in range(20)
            ])
            st.markdown(flowers, unsafe_allow_html=True)

        # Render component tương ứng
        if menu == "Data List":
            self.data_list.xem_du_lieu()
        elif menu == "Change History":
            self.change_history.xem_lich_su()
        elif menu == "CRUD":
            self.crud_form.quan_ly()
        elif menu == "Charts":
            self.charts.ve_bieu_do()
        elif menu == "Xem hồi quy":
            self.regression.ve_hoi_quy_va_du_doan()
