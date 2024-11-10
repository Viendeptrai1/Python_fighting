from DocDuLieu.docdulieu import DuLieu
from XuLyDuLieu.xulydulieu import XuLyDuLieu
from TrucQuanHoa.trunquanhoa import TrucQuanHoa
from GiaoDien.giaodien import GiaoDien
import customtkinter as ctk
import matplotlib.pyplot as plt

def main():
    du_lieu = DuLieu("Data/data_sales.csv")
    if du_lieu.lay_du_lieu() is None:
        return
    xu_ly_du_lieu = XuLyDuLieu(du_lieu.lay_du_lieu())
    xu_ly_du_lieu.lam_sach_du_lieu()
    xu_ly_du_lieu.chuyen_doi_du_lieu()
    
    truc_quan_hoa = TrucQuanHoa(du_lieu.lay_du_lieu())

    # Khởi tạo cửa sổ giao diện chính
    root = ctk.CTk()  
    root.geometry("800x600") 

    # Khởi tạo giao diện và truyền các đối tượng cần thiết
    GiaoDien(root, xu_ly_du_lieu, truc_quan_hoa)  

    # Chạy giao diện
    root.mainloop()  

if __name__ == "__main__":
    main()