import logging

import streamlit as st

from util.logging_utils import setup_logging
from ui.ui_config import UIConfig
from ui.ui_elements import display_header, get_user_input, image_adjustment_controls
from ui.image_generation import generate_and_process_image
from ui.image_display import display_images_with_download_links

setup_logging()

# CSS 파일을 읽고 스타일 적용
def load_css(css_file):
    with open(css_file, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("static/style.css")

# Initialize or get the session state for storing inputs and images
if 'inputs' not in st.session_state:
    st.session_state.inputs = []
if 'images' not in st.session_state:
    st.session_state.images = []
# Text area for new input

# UIConfig 클래스 인스턴스 생성
ui_config = UIConfig()

# 사용자 인터페이스 설정
model = ui_config.select_model()
style = ui_config.select_style()
quality = ui_config.select_quality()
size = ui_config.select_size()

# UI 요소 표시
display_header()
new_input = get_user_input()
brightness, saturation, contrast, toggle_brightness, toggle_saturation, toggle_contrast = image_adjustment_controls()

# 이미지 생성 관련 UI 및 기능
if st.button('Generate Image'):
    logging.info(f"Image generation requested with prompt: {new_input}")
    with st.spinner('Generating image...'):
        generate_and_process_image(new_input, model, size, quality, style, brightness, saturation, contrast, toggle_brightness, toggle_saturation, toggle_contrast)

# 이미지 표시 및 다운로드 관련 기능
display_images_with_download_links()