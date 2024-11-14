import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor


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
    
    def hoi_quy_tuyen_tinh_1_dac_trung_thu_cong(self, dac_trung, du_lieu):
        # nguoi_hut_thuoc_df = self.du_lieu[self.du_lieu['smoker'] == 'yes']
        # plt.title('Chi phí so với độ tuổi dựa trên đối tượng hút thuốc')
        # sns.scatterplot(data=nguoi_hut_thuoc_df, x='age', y='charges', alpha=0.7, s=15)
        # plt.show()
        
        def uoc_tinh_chi_phi(tmp, a, b):
            return a * tmp + b 

        def tinh_rmse(thuc_te, du_doan):
            sai_so = thuc_te - du_doan
            sai_so_binh_phuong = sai_so ** 2
            trung_binh_sai_so_binh_phuong = np.mean(sai_so_binh_phuong)
            rmse = np.sqrt(trung_binh_sai_so_binh_phuong)
            return rmse
        
        def thu_tham_so(a, b, dac_trung, du_lieu):
            dau_vao_df = du_lieu[dac_trung]
            chi_phi_thuc_te_df = du_lieu['charges']
    
            chi_phi_duoc_uoc_tinh = uoc_tinh_chi_phi(dau_vao_df, a, b)
    
            plt.plot(dau_vao_df, chi_phi_duoc_uoc_tinh, 'r', alpha=0.9)
            plt.scatter(dau_vao_df, chi_phi_thuc_te_df, s=8, alpha=0.8)
            plt.xlabel(dac_trung)
            plt.ylabel('Charges')
            plt.legend(['Estimate', 'Actual'])
            
            if b > 0:
                plt.text(0.05, 0.90,
                     f'y = {a:.2f} * x + {b:.2f}', 
                     transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
            else:
                plt.text(0.05, 0.90,
                     f'y = {a:.2f} * x {b:.2f}', 
                     transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
    
            loss = tinh_rmse(chi_phi_thuc_te_df, chi_phi_duoc_uoc_tinh)
                             
            plt.text(0.05, 0.95, f'RMSE Loss: {loss:.2f}',
                     transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
    
            plt.show()
        
        n = int(input("Nhập số lần thử tham số: "))
        for i in range(n):
            a = float(input("Nhập hệ số a: "))
            b = float(input("Nhập hệ số b: "))
            thu_tham_so(a, b, dac_trung, du_lieu)
            


    def hoi_quy_tuyen_tinh_1_dac_trung_su_dung_ham(self, dac_trung, du_lieu):
        model = LinearRegression()
        dau_vao_df = du_lieu[[dac_trung]]
        chi_phi_thuc_te_df = du_lieu['charges']
    
        model.fit(dau_vao_df, chi_phi_thuc_te_df)
    
        chi_phi_duoc_uoc_tinh = model.predict(dau_vao_df)
    
        def tinh_rmse(thuc_te, du_doan):
            sai_so = thuc_te - du_doan
            sai_so_binh_phuong = sai_so ** 2
            trung_binh_sai_so_binh_phuong = np.mean(sai_so_binh_phuong)
            rmse = np.sqrt(trung_binh_sai_so_binh_phuong)
            return rmse
    
        plt.plot(dau_vao_df, chi_phi_duoc_uoc_tinh, 'r', alpha=0.9)
        plt.scatter(dau_vao_df, chi_phi_thuc_te_df, s=8, alpha=0.8)
        plt.xlabel(dac_trung)
        plt.ylabel('Charges')
        plt.legend(['Estimate', 'Actual'])

        a = model.coef_[0]
        b = model.intercept_
        if b > 0:
            plt.text(0.05, 0.90,
                 f'y = {a:.2f} * x + {b:.2f}', 
                 transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
        else:
            plt.text(0.05, 0.90,
                 f'y = {a:.2f} * x {b:.2f}', 
                 transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
        
        loss = tinh_rmse(chi_phi_thuc_te_df, chi_phi_duoc_uoc_tinh)
                         
        plt.text(0.05, 0.95, f'RMSE Loss: {loss:.2f}',
                 transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

        plt.show()

        
        
    
        
        


        

        
        
