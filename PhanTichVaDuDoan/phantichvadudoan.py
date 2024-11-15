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
            
            equation_text = f'y = {a:.2f} * x + {b:.2f}' if b > 0 else f'y = {a:.2f} * x {b:.2f}'
            plt.text(0.05, 0.90,
                 equation_text, 
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
        dau_vao_df = du_lieu[dac_trung]
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
        equation_text = f'y = {a:.2f} * x + {b:.2f}' if b > 0 else f'y = {a:.2f} * x {b:.2f}'
        plt.text(0.05, 0.90,
                 equation_text, 
                 transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
        
        loss = tinh_rmse(chi_phi_thuc_te_df, chi_phi_duoc_uoc_tinh)
                         
        plt.text(0.05, 0.95, f'RMSE Loss: {loss:.2f}',
                 transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

        plt.show()


    def hoi_quy_tuyen_tinh_nhieu_dac_trung_su_dung_ham(self, dac_trung, du_lieu):
        model = LinearRegression()
        dau_vao_df = du_lieu[dac_trung]
        chi_phi_thuc_te_df = du_lieu['charges']

        model.fit(dau_vao_df, chi_phi_thuc_te_df)

        chi_phi_duoc_uoc_tinh = model.predict(dau_vao_df)

        def tinh_rmse(thuc_te, du_doan):
            sai_so = thuc_te - du_doan
            sai_so_binh_phuong = sai_so ** 2
            trung_binh_sai_so_binh_phuong = np.mean(sai_so_binh_phuong)
            rmse = np.sqrt(trung_binh_sai_so_binh_phuong)
            return rmse
        
        loss = tinh_rmse(chi_phi_thuc_te_df, chi_phi_duoc_uoc_tinh)
        for i, dac_trung_don in enumerate(dac_trung):
            fig = px.scatter(du_lieu, x=dac_trung_don, y='charges', color='smoker', title=f'{dac_trung_don} vs Charges')
            
            a = model.coef_[i]
            b = model.intercept_
            fig.add_annotation(x=0.05, y=0.95,
                               xref='paper', yref='paper',
                               text=f'RMSE Loss: {loss:.2f}', showarrow=False, 
                               font=dict(size=12, color='black'), bgcolor='white', opacity=0.5)
            fig.show()


        
    
        
        


        

        
        
