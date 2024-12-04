import streamlit as st

class ChartsComponent:
    def __init__(self, truc_quan_hoa, du_lieu):
        self.truc_quan_hoa = truc_quan_hoa
        self.du_lieu = du_lieu

    def ve_bieu_do(self):
        st.header("Phân tích trực quan dữ liệu")
        
        # Thêm radio button để chọn nguồn dữ liệu
        data_source = st.radio(
            "Chọn nguồn dữ liệu:",
            ["Dữ liệu gốc", "Dữ liệu đã chỉnh sửa"],
            horizontal=True
        )
        
        # Lấy dữ liệu tương ứng
        if data_source == "Dữ liệu gốc":
            data = st.session_state.original_data
        else:
            data = st.session_state.modified_data
            
        # Cập nhật dữ liệu cho TrucQuanHoa
        self.truc_quan_hoa.cap_nhat_du_lieu(data)
        
        if data is None:
            st.error("Không có dữ liệu để vẽ biểu đồ")
            return

        # Hiển thị thông tin về dữ liệu đang sử dụng
        st.info(f"Đang sử dụng {data_source} với {len(data)} bản ghi")

        tab1, tab2, tab3 = st.tabs([
            "Phân bố chi phí y tế theo các yếu tố",
            "Phân bố theo đặc điểm nhân khẩu học",
            "Mối quan hệ chi phí với các yếu tố"
        ])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                # Biểu đồ phân bố tuổi
                fig_age = self.truc_quan_hoa.ve_bieu_do_histogram(
                    cot_gia_tri='age',
                    bien='box',
                    so_khoang=47,
                    title='Phân bố tuổi'
                )
                st.plotly_chart(fig_age, use_container_width=True, key="hist_age")

                # Biểu đồ phí theo giới tính
                fig_charges_sex = self.truc_quan_hoa.ve_bieu_do_histogram(
                    cot_gia_tri='charges',
                    mau_phan_loai='sex',
                    mau_cu_the=['red', 'blue'],
                    title='Các khoản phí khác nhau về giới tính'
                )
                st.plotly_chart(fig_charges_sex, use_container_width=True, key="hist_charges_sex")

                # Biểu đồ phí theo khu vực
                fig_charges_region = self.truc_quan_hoa.ve_bieu_do_histogram(
                    cot_gia_tri='charges',
                    bien='box',
                    mau_phan_loai='region',
                    title='Chi phí trên các khu vực khác nhau của Hoa Kỳ'
                )
                st.plotly_chart(fig_charges_region, use_container_width=True, key="hist_charges_region")

            with col2:
                # Biểu đồ phân bố BMI
                fig_bmi = self.truc_quan_hoa.ve_bieu_do_histogram(
                    cot_gia_tri='bmi',
                    bien='box',
                    mau_cu_the=['red'],
                    title='Phân bố BMI (Body Mass Index)'
                )
                st.plotly_chart(fig_bmi, use_container_width=True, key="hist_bmi")

                # Biểu đồ phí theo người hút thuốc
                fig_charges_smoker = self.truc_quan_hoa.ve_bieu_do_histogram(
                    cot_gia_tri='charges',
                    bien='box',
                    mau_phan_loai='smoker',
                    mau_cu_the=['red', 'grey'],
                    title='Phí y tế hàng năm'
                )
                st.plotly_chart(fig_charges_smoker, use_container_width=True, key="hist_charges_smoker")

                # Biểu đồ hút thuốc theo giới tính
                fig_smoker_sex = self.truc_quan_hoa.ve_bieu_do_histogram(
                    cot_gia_tri='smoker',
                    mau_phan_loai='sex',
                    mau_cu_the=['red', 'blue'],
                    title='Số lượng hút thuốc và không hút thuốc theo nam và nữ'
                )
                st.plotly_chart(fig_smoker_sex, use_container_width=True, key="hist_smoker_sex")

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                # Biểu đồ chi phí theo số con
                fig_charges_children = self.truc_quan_hoa.ve_bieu_do_histogram(
                    cot_gia_tri='charges',
                    bien='box',
                    mau_phan_loai='children',
                    title='Chi phí phát sinh cho trẻ em'
                )
                st.plotly_chart(fig_charges_children, use_container_width=True, key="hist_charges_children")
                
                # Biểu đồ scatter BMI và chi phí
                fig_bmi_charges = self.truc_quan_hoa.ve_bieu_do_scatter(
                    cot_gia_tri='bmi',
                    cot_nhom='charges',
                    mau_phan_loai='smoker',
                    mau_cu_the=['red', 'blue'],
                    do_mo=0.8,
                    du_lieu_them=['sex'],
                    title='Chi phí so với BMI'
                )
                st.plotly_chart(fig_bmi_charges, use_container_width=True, key="scatter_bmi_charges")

            with col2:
                # Biểu đồ scatter tuổi và chi phí
                fig_age_charges = self.truc_quan_hoa.ve_bieu_do_scatter(
                    cot_gia_tri='age',
                    cot_nhom='charges',
                    mau_phan_loai='smoker',
                    mau_cu_the=['red', 'blue'],
                    do_mo=0.8,
                    du_lieu_them=['sex'],
                    title='Chi phí so với độ tuổi'
                )
                st.plotly_chart(fig_age_charges, use_container_width=True, key="scatter_age_charges")

        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                # Biểu đồ violin cho số con
                fig_violin = self.truc_quan_hoa.ve_bieu_do_violin(
                    cot_gia_tri='children',
                    cot_nhom='charges',
                    title='Chi phí so với số lượng con cái'
                )
                st.plotly_chart(fig_violin, use_container_width=True, key="violin_children_charges")

                # Biểu đồ bar cho giới tính và hút thuốc
                fig_sex_smoke = self.truc_quan_hoa.ve_bieu_do_barplot(
                    cot_gia_tri='sex',
                    cot_nhom='charges',
                    du_lieu_phan_biet='smoker',
                    title='Chi phí so với việc hút thuốc hay không hút thuốc theo giới tính'
                )
                st.pyplot(fig_sex_smoke)

            with col2:
                # Biểu đồ histogram cho giới tính và khu vực
                fig_sex_region = self.truc_quan_hoa.ve_bieu_do_histogram(
                    cot_gia_tri='sex',
                    cot_nhom='charges',
                    mau_phan_loai='region',
                    nhan_y='Tổng chi phí',
                    nhan_x='Giới tính',
                    title='Chi phí so với vùng theo giới tính'
                )
                st.plotly_chart(fig_sex_region, use_container_width=True, key="hist_sex_region")

                # Ma trận tương quan
                fig_corr = self.truc_quan_hoa.ve_bieu_do_heatmap(
                    corr_matrix=self.du_lieu.lay()[['age', 'bmi', 'children', 'charges']].corr(),
                    title='Ma trận tương quan'
                )
                st.pyplot(fig_corr)
