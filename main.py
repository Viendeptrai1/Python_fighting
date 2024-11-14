import streamlit as st
from DocDuLieu.docdulieu import DuLieu
from TrucQuanHoa.trucquanhoa import TrucQuanHoa
from XuLyDuLieu.xulydulieu import XuLyDuLieu
from GiaoDien.giaodien import GiaoDien

def main():
    # Initialize the app
    if 'data' not in st.session_state:
        st.session_state.data = DuLieu("Data/Health_insurance.csv").lay_du_lieu()
        st.session_state.xu_ly = XuLyDuLieu(st.session_state.data)
        st.session_state.truc_quan = TrucQuanHoa(st.session_state.data)
    
    # Create and run the interface
    app = GiaoDien()
    app.main()

if __name__ == "__main__":
    main()