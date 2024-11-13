import pandas as pd

class XuLyDuLieu:
    """
    Class này thực hiện các bước xử lý và biến đổi dữ liệu.
    """

    def __init__(self, du_lieu):
        """
        Khởi tạo đối tượng XuLyDuLieu.

        Args:
          du_lieu: DataFrame chứa dữ liệu.
        """
        self.du_lieu = du_lieu

    
   