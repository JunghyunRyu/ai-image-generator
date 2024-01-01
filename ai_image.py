import logging

import streamlit as st
from io import BytesIO
from PIL import Image as PILImage
import requests
import base64
from openai import OpenAI
import os


# 로그 파일을 저장할 디렉토리 생성
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# 로깅 설정
log_file_path = os.path.join(log_directory, 'app.log')
logging.basicConfig(filename=log_file_path, filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# CSS 스타일 정의
st.markdown("""
    <style>
    .css-2trqyj {
        font-size: 14px; /* 글자 크기 조정 */
        font-family: Arial, sans-serif; /* 폰트 변경 */
    }
    </style>
""", unsafe_allow_html=True)


OpenAI.api_key=st.secrets['OPENAI_API_KEY']

client = OpenAI()

def generate_image(prompt, model, size, quality, style, num_images=1):
    try:
        response = client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=num_images,
            style=style
        )        
        image_url = response.data[0].url
        response = requests.get(image_url)

        if response.status_code == 200:
            image = PILImage.open(BytesIO(response.content))
            return image
        else:
            error_message = f"Failed to download the image. Status code: {response.status_code}"
            st.error(error_message)
            logging.error(error_message)            
            return None
    except Exception as e:
        error_message = f"An error occurred: {e}"
        st.error(error_message)
        logging.error(error_message, exc_info=True)
        return None

def get_image_download_link(img, filename="generated_image.png", text="Download Image"):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

# Initialize or get the session state for storing inputs and images
if 'inputs' not in st.session_state:
    st.session_state.inputs = []
if 'images' not in st.session_state:
    st.session_state.images = []
# Text area for new input


# Model selection
model = st.sidebar.selectbox("Model", ["dall-e-3"], index=0)

# Style selection
# Mapping Korean options to English values
style_options = {"Natural": "natural", "Vidid": "vivid"}
quality_options = {"Standard": "standard", "HD": "hd"}
size_options = {"1024x1024": "1024x1024", "1792x1024": "1792x1024", "1024x1792": "1024x1792"}


# Style selection
selected_style = st.sidebar.selectbox("Style", list(style_options.keys()))
style = style_options[selected_style]

# Quality selection
selected_quality = st.sidebar.selectbox("Quality", list(quality_options.keys()))
quality = quality_options[selected_quality]

# Size selection
selected_size = st.sidebar.selectbox("Size", list(size_options.keys()))
size = size_options[selected_size]

# AI 생성 이미지 헤더 추가 (이모지 및 스타일리시한 폰트 포함)
st.markdown("""
    <h1 style='text-align: center; color: #ff6347; font-family: Comic Sans MS;'>
        🎨 AI Generated Images Gallery 🌌
    </h1>
    <p style='text-align: center; font-size: 20px; font-family: Comic Sans MS;'>
        Explore the creativity of AI-generated art! ✨
    </p>
""", unsafe_allow_html=True)

new_input = st.text_area("Enter your image description here:")

if st.button('Generate Image'):
    st.session_state.inputs.append(new_input)
    with st.spinner('Generating image...'):
        generated_image = generate_image(new_input,model,size,quality,style)
        if generated_image:
            st.session_state.images.append(generated_image)

# Display all the generated images and their download links
for idx, (inp, img) in enumerate(zip(st.session_state.inputs, st.session_state.images)):
    st.text(f"Input {idx+1}: {inp}")
    st.image(img, caption=f'Generated Image {idx+1}')
    st.markdown(get_image_download_link(img), unsafe_allow_html=True)