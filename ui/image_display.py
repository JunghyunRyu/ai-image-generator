import streamlit as st
from util.download_utils import get_image_download_link  # get_image_download_link 함수가 정의된 utils 모듈

def display_images_with_download_links():
    for idx, (inp, img) in enumerate(zip(st.session_state.inputs, st.session_state.images)):
        display_idx = idx + 1
        st.text(f"Input description: {inp}")
        st.image(img, caption=f'Generated Image {display_idx}')
        st.markdown(get_image_download_link(img), unsafe_allow_html=True)
