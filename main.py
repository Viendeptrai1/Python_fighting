import streamlit as st
from DocDuLieu.docdulieu import DuLieu
from TrucQuanHoa.trucquanhoa import TrucQuanHoa
from XuLyDuLieu.xulydulieu import XuLyDuLieu
from GiaoDien.giaodien import GiaoDien
from PhanTichVaDuDoan.phantichvadudoan import PhanTichVaDuDoan

def main():
    # Khởi tạo dữ liệu và lưu trữ trong session_state
    if 'du_lieu' not in st.session_state:
        du_lieu = DuLieu("Data/Health_insurance.csv")
        data = du_lieu.lay()
        
        if data is not None:
            st.session_state.du_lieu = du_lieu
            st.session_state.truc_quan = TrucQuanHoa(data)
            st.session_state.xu_ly = XuLyDuLieu(data)
            st.session_state.phan_tich_va_du_doan = PhanTichVaDuDoan(data)
        else:
            st.error("Không thể đọc dữ liệu. Vui lòng kiểm tra file dữ liệu.")
            return

    app = GiaoDien(
        truc_quan_hoa=st.session_state.truc_quan,
        du_lieu=st.session_state.du_lieu,
        phan_tich_va_du_doan=st.session_state.phan_tich_va_du_doan
    )
    app.chay()

if __name__ == "__main__":
    main()
