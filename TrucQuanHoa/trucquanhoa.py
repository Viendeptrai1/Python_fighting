import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

class TrucQuanHoa:
    """
    Class thực hiện việc trực quan hóa dữ liệu với nhiều loại biểu đồ khác nhau.
    """
    def __init__(self, du_lieu):
        """
        Khởi tạo đối tượng TrucQuanHoa.
        Args:
            du_lieu: DataFrame chứa dữ liệu cần trực quan hóa
        """
        self.du_lieu = du_lieu
        plt.style.use('default')  
        sns.set_style("whitegrid")  

    def ve_bieu_do_histogram(self, cot_gia_tri, cot_nhom=None,
                           nhan_x=None, nhan_y=None, chu_thich=None,
                           bien=None, mau_cu_the=None, so_khoang=None, 
                           mau_phan_loai=None, title=None):
        """Vẽ biểu đồ histogram"""
        fig = px.histogram(
            self.du_lieu,
            x=cot_gia_tri,
            y=cot_nhom,
            marginal=bien,
            color=mau_phan_loai,
            nbins=so_khoang or 30,
            color_discrete_sequence=mau_cu_the,
            title=title or f'Histogram của {cot_gia_tri}'
        )
        fig.update_layout(
            bargap=0.1,
            xaxis_title=nhan_x,
            yaxis_title=nhan_y,
            legend_title=chu_thich,
        )
        return fig

    def ve_bieu_do_scatter(self, cot_gia_tri, cot_nhom, du_lieu=None,
                          mau_cu_the=None, mau_phan_loai=None, do_mo=None, du_lieu_them=None, title=None):
        """Vẽ biểu đồ scatter"""
        if du_lieu is None:
            du_lieu = self.du_lieu
        fig = px.scatter(
            du_lieu,
            x=cot_gia_tri,
            y=cot_nhom,
            color=mau_phan_loai,
            color_discrete_sequence=mau_cu_the,
            opacity=do_mo,
            hover_data=du_lieu_them,
            title=title
        )
        fig.update_traces(marker=dict(size=5, symbol='circle'))
        return fig

    def ve_bieu_do_violin(self, cot_gia_tri, cot_nhom, title=None):
        """Vẽ biểu đồ violin"""
        fig = px.violin(
            self.du_lieu,
            x=cot_gia_tri,
            y=cot_nhom,
            title=title or f'Phân phối chi tiết {cot_gia_tri} theo {cot_nhom}'
        )
        return fig

    def ve_bieu_do_barplot(self, cot_gia_tri, cot_nhom, du_lieu_phan_biet=None, title=None):
        """Vẽ biểu đồ thanh"""
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(
            data=self.du_lieu,
            x=cot_gia_tri,
            y=cot_nhom,
            hue=du_lieu_phan_biet,
            ax=ax
        )
        ax.set_title(title)
        plt.tight_layout()
        return fig

    def ve_bieu_do_heatmap(self, corr_matrix, title=None):
        """Vẽ biểu đồ nhiệt"""
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(
            corr_matrix,
            cmap='Blues',
            annot=True,
            fmt=".2f",
            ax=ax
        )
        ax.set_title(title)
        plt.xticks(rotation=0)
        plt.tight_layout()
        return fig
