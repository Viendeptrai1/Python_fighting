import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Tạo hình ảnh tiêu đề
def create_styled_title(text):
    # Tạo ảnh nền trắng
    img = Image.new('RGB', (800, 100), color=(255, 255, 255))
    
    # Thêm văn bản lên ảnh
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('path/to/font.ttf', size=50)
    w, h = draw.textsize(text, font)
    draw.text(((800-w)/2,(100-h)/2), text, font=font, fill=(73, 144, 226))
    
    return np.array(img)

# Hiển thị tiêu đề
st.image(create_styled_title("**Dự đoán giá bảo hiểm y tế**"), use_column_width=True)