import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import pandas as pd
import numpy as np


class PhanTichVaDuDoan:
    """
    Class này thực hiện các bước phân tích và dự đoán dữ liệu.
    """

    def __init__(self, du_lieu):
        """
        Khởi tạo đối tượng PhanTichVaDuDoan.

        Args:
          du_lieu: DataFrame chứa dữ liệu.
        """
        self.du_lieu = du_lieu
    
    def hoi_quy_tuyen_tinh_dua_tren_1_dac_trung_tuoi(self):
        nguoi_khong_hut_thuoc_df = self.du_lieu[self.du_lieu['smoker'] == 'no']
        plt.title('Chi phí so với độ tuổi dựa trên đối tượng không hút thuốc')
        sns.scatterplot(data=nguoi_khong_hut_thuoc_df, x='age', y='charges', alpha=0.7, s=15)
        plt.show()
        
        def uoc_tinh_chi_phi(tuoi, a, b):
            return a * tuoi + b 

        def tinh_rmse(thuc_te, du_doan):
            sai_so = thuc_te - du_doan
            sai_so_binh_phuong = sai_so ** 2
            trung_binh_sai_so_binh_phuong = np.mean(sai_so_binh_phuong)
            rmse = np.sqrt(trung_binh_sai_so_binh_phuong)
            return rmse
        
        def thu_tham_so(w, b, data):
            tuoi_df = data['age']
            chi_phi_thuc_te_df = data['charges']
    
            chi_phi_duoc_uoc_tinh = uoc_tinh_chi_phi(tuoi_df, w, b)
    
            plt.plot(tuoi_df, chi_phi_duoc_uoc_tinh, 'r', alpha=0.9)
            plt.scatter(tuoi_df, chi_phi_thuc_te_df, s=8, alpha=0.8)
            plt.xlabel('Age')
            plt.ylabel('Charges')
            plt.legend(['Estimate', 'Actual'])
    
            loss = tinh_rmse(chi_phi_thuc_te_df, chi_phi_duoc_uoc_tinh)
                             
            plt.text(0.05, 0.95, f'RMSE Loss: {loss:.2f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
    
            plt.show()
        
        # thu_tham_so(259,-1700, nguoi_khong_hut_thuoc_df)
        # thu_tham_so(259,-1700, nguoi_khong_hut_thuoc_df)    
        # thu_tham_so(259,-1700, nguoi_khong_hut_thuoc_df)
        thu_tham_so(259,-1700, nguoi_khong_hut_thuoc_df)
    
        
        


        

        
        
