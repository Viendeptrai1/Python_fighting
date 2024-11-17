import pandas as pd
import streamlit as st
import logging
from pathlib import Path

class DuLieu:
    def __init__(self, ten_file):
        self.ten_file = Path(ten_file)
        self._thiet_lap_log()
        self.du_lieu = self.doc()

    def _thiet_lap_log(self):
        """Thiết lập logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('dulieu.log'),
                logging.StreamHandler()
            ]
        )

    def doc(self):
        """
        Đọc dữ liệu từ file CSV.
        Returns:
            pd.DataFrame: DataFrame chứa dữ liệu, None nếu có lỗi
        """
        try:
            if not self.ten_file.exists():
                raise FileNotFoundError(f"Không tìm thấy file {self.ten_file}")
                
            df = pd.read_csv(self.ten_file)
            logging.info(f"Đã đọc thành công file {self.ten_file}")
            return df
            
        except FileNotFoundError as e:
            logging.error(f"Lỗi: {str(e)}")
            st.error(f"Lỗi: Không tìm thấy file {self.ten_file}")
            return None
            
        except pd.errors.EmptyDataError:
            logging.error(f"File {self.ten_file} rỗng")
            st.error(f"Lỗi: File {self.ten_file} rỗng")
            return None
            
        except Exception as e:
            logging.error(f"Lỗi không xác định: {str(e)}")
            st.error(f"Lỗi không xác định khi đọc file: {str(e)}")
            return None

    def luu(self):
        """
        Lưu DataFrame vào file CSV.
        Returns:
            bool: True nếu lưu thành công, False nếu có lỗi
        """
        try:
            if self.du_lieu is not None:
                self.du_lieu.to_csv(self.ten_file, index=False)
                logging.info(f"Đã lưu thành công dữ liệu vào {self.ten_file}")
                return True
            return False
            
        except Exception as e:
            logging.error(f"Lỗi khi lưu file: {str(e)}")
            st.error(f"Lỗi khi lưu file: {str(e)}")
            return False

    def lay(self):
        """
        Trả về DataFrame hiện tại.
        Returns:
            pd.DataFrame: DataFrame chứa dữ liệu
        """
        return self.du_lieu