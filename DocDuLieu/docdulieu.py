import pandas as pd

class DuLieu:
  """
  Class này chịu trách nhiệm đọc và lưu trữ dữ liệu từ file CSV.
  """
  def __init__(self, ten_file):
    """
    Khởi tạo đối tượng DuLieu.

    Args:
      ten_file: Đường dẫn tới file CSV chứa dữ liệu.
    """
    try:
        self.du_lieu = pd.read_csv(ten_file)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {ten_file}")
        self.du_lieu = None

  def lay_du_lieu(self):
    """
    Trả về DataFrame chứa dữ liệu.

    Returns:
      pd.DataFrame: DataFrame chứa dữ liệu.
    """
    return self.du_lieu