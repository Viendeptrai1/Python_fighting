import pandas as pd
from typing import Dict, List

class CRUD:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self._validate_columns()
        
    def _validate_columns(self) -> None:
        required_columns = {'ID', 'age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges'}
        missing_columns = required_columns - set(self.df.columns)
        if missing_columns:
            raise ValueError(f"DataFrame thiếu các cột: {missing_columns}")

    def _validate_record(self, record: Dict) -> None:
        if not isinstance(record.get('age'), (int, float)) or record['age'] < 0:
            raise ValueError("Tuổi phải là số không âm")
        if record.get('sex') not in ['male', 'female']:
            raise ValueError("Giới tính phải là 'male' hoặc 'female'")
        if not isinstance(record.get('bmi'), (int, float)) or record['bmi'] < 0:
            raise ValueError("BMI phải là số không âm")
        if not isinstance(record.get('children'), int) or record['children'] < 0:
            raise ValueError("Số con phải là số nguyên không âm")
        if record.get('smoker') not in ['yes', 'no']:
            raise ValueError("Smoker phải là 'yes' hoặc 'no'")
        if record.get('region') not in ['southwest', 'southeast', 'northwest', 'northeast']:
            raise ValueError("Region không hợp lệ")
        if not isinstance(record.get('charges'), (int, float)) or record['charges'] < 0:
            raise ValueError("Chi phí bảo hiểm phải là số không âm")
        
        # Chuyển đổi charges về float với 4 chữ số thập phân
        record['charges'] = float(format(record['charges'], '.4f'))

    def them(self, record: Dict) -> pd.DataFrame:
        """Thêm bản ghi mới và trả về DataFrame đã cập nhật"""
        self._validate_record(record)
        
        # Tạo ID mới
        new_id = self.df['ID'].max() + 1 if not self.df.empty else 1
        record['ID'] = new_id
        
        # Thêm bản ghi mới với ID
        new_df = pd.concat([self.df, pd.DataFrame([record])], ignore_index=True)
        
        # Đảm bảo cột ID ở đầu
        cols = ['ID'] + [col for col in new_df.columns if col != 'ID']
        new_df = new_df[cols]
        
        return new_df

    def sua(self, index: int, record: Dict) -> pd.DataFrame:
        """Sửa bản ghi và trả về DataFrame đã cập nhật"""
        if index not in self.df.index:
            raise ValueError(f"Không tìm thấy bản ghi với index {index}")
        
        self._validate_record(record)
        
        # Giữ nguyên ID cũ
        record['ID'] = self.df.loc[index, 'ID']
        
        new_df = self.df.copy()
        new_df.loc[index] = record
        
        # Đảm bảo cột ID ở đầu
        cols = ['ID'] + [col for col in new_df.columns if col != 'ID']
        new_df = new_df[cols]
        
        return new_df

    def xoa(self, indices: List[int]) -> pd.DataFrame:
        """Xóa các bản ghi và trả về DataFrame đã cập nhật"""
        invalid_indices = [idx for idx in indices if idx not in self.df.index]
        if invalid_indices:
            raise ValueError(f"Không tìm thấy các bản ghi với index: {invalid_indices}")
            
        new_df = self.df.drop(indices).reset_index(drop=True)
        
        # Đảm bảo cột ID ở đầu và liên tục
        new_df['ID'] = range(1, len(new_df) + 1)
        cols = ['ID'] + [col for col in new_df.columns if col != 'ID']
        new_df = new_df[cols]
        
        return new_df
