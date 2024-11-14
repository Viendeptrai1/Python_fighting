import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class TrucQuanHoa:
    def __init__(self, du_lieu):
        self.du_lieu = du_lieu
        self.color_sequence = px.colors.qualitative.Set3

    def ve_bieu_do_histogram(self, cot_gia_tri, bien=None, cot_nhom=None, mau_phan_loai=None, 
                            so_khoang=None, mau_cu_the=None, do_mo=0.7, du_lieu_them=None,
                            nhan_x=None, nhan_y=None, title=None):
        fig = go.Figure()

        if bien == 'box':
            # Vẽ biểu đồ box plot
            if mau_phan_loai:
                fig = px.box(self.du_lieu, x=cot_gia_tri, color=mau_phan_loai)
            else:
                fig = px.box(self.du_lieu, x=cot_gia_tri)
        else:
            # Vẽ biểu đồ histogram
            if mau_phan_loai:
                fig = px.histogram(self.du_lieu, x=cot_gia_tri, color=mau_phan_loai,
                                 nbins=so_khoang if so_khoang else 30,
                                 opacity=do_mo)
            else:
                fig = px.histogram(self.du_lieu, x=cot_gia_tri,
                                 nbins=so_khoang if so_khoang else 30,
                                 opacity=do_mo)

        if mau_cu_the:
            fig.update_traces(marker_color=mau_cu_the[0])

        if title:
            fig.update_layout(title=title)
        if nhan_x:
            fig.update_xaxes(title=nhan_x)
        if nhan_y:
            fig.update_yaxes(title=nhan_y)

        return fig

    def ve_bieu_do_scatter(self, cot_gia_tri, cot_nhom, mau_phan_loai=None, 
                          do_mo=0.7, du_lieu_them=None, title=None):
        fig = px.scatter(self.du_lieu, x=cot_gia_tri, y=cot_nhom, 
                        color=mau_phan_loai,
                        opacity=do_mo,
                        hover_data=du_lieu_them if du_lieu_them else None,
                        title=title if title else f'Scatter Plot: {cot_gia_tri} vs {cot_nhom}')
        return fig

    def ve_bieu_do_violin(self, cot_gia_tri, cot_nhom, title=None):
        fig = px.violin(self.du_lieu, x=cot_gia_tri, y=cot_nhom,
                       title=title if title else f'Violin Plot: {cot_gia_tri} vs {cot_nhom}')
        return fig

    def ve_bieu_do_barplot(self, cot_gia_tri, cot_nhom, du_lieu_phan_biet=None, title=None):
        if du_lieu_phan_biet:
            fig = px.bar(self.du_lieu, x=cot_gia_tri, y=cot_nhom, 
                        color=du_lieu_phan_biet,
                        barmode='group',
                        title=title if title else f'Bar Plot: {cot_gia_tri} vs {cot_nhom}')
        else:
            fig = px.bar(self.du_lieu, x=cot_gia_tri, y=cot_nhom,
                        title=title if title else f'Bar Plot: {cot_gia_tri} vs {cot_nhom}')
        return fig

    def ve_bieu_do_heatmap(self, corr_matrix, title=None):
        fig = px.imshow(corr_matrix,
                       title=title if title else 'Heatmap',
                       color_continuous_scale='RdBu')
        return fig

    # Giữ lại các phương thức cũ để đảm bảo tương thích ngược
    def ve_bieu_do_phan_phoi(self, col_name):
        return self.ve_bieu_do_histogram(col_name, title=f'Phân phối của {col_name}')

    def ve_bieu_do_box(self, x_col, y_col, color_col=None):
        fig = px.box(self.du_lieu, x=x_col, y=y_col, color=color_col,
                    title=f'Box Plot của {y_col} theo {x_col}')
        return fig

    def ve_bieu_do_scatter_old(self, x_col, y_col, color_col=None):
        fig = px.scatter(self.du_lieu, x=x_col, y=y_col, color=color_col,
                        title=f'Scatter Plot của {y_col} vs {x_col}')
        return fig

    def ve_bieu_do_tuong_quan(self):
        numeric_cols = self.du_lieu.select_dtypes(include=[np.number]).columns
        corr_matrix = self.du_lieu[numeric_cols].corr()
        return self.ve_bieu_do_heatmap(corr_matrix, title='Ma trận tương quan')