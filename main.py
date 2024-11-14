from DocDuLieu.docdulieu import DuLieu
from PhanTichVaDuDoan.phantichvadudoan import PhanTichVaDuDoan
from XuLyDuLieu.xulydulieu import XuLyDuLieu
from TrucQuanHoa.trucquanhoa import TrucQuanHoa
from GiaoDien.giaodien import GiaoDien
import customtkinter as ctk
import matplotlib.pyplot as plt

def main():
    du_lieu = DuLieu("Data/Health_insurance.csv")
    if du_lieu.lay_du_lieu() is None:
        return
    xu_ly_du_lieu = XuLyDuLieu(du_lieu.lay_du_lieu())
    xu_ly_du_lieu.chuyen_doi_du_lieu()
    truc_quan_hoa = TrucQuanHoa(du_lieu.lay_du_lieu())
    phan_tich_va_du_doan = PhanTichVaDuDoan(du_lieu.lay_du_lieu())
    
    
    # Khởi tạo cửa sổ giao diện chính
    root = ctk.CTk()  
    root.geometry("800x600") 

    # Khởi tạo giao diện và truyền các đối tượng cần thiết
    GiaoDien(root, xu_ly_du_lieu, truc_quan_hoa, phan_tich_va_du_doan, du_lieu)  

    # Chạy giao diện
    root.mainloop()  

if __name__ == "__main__":
    main()

