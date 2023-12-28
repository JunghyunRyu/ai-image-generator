import streamlit as st
from io import BytesIO
from PIL import Image as PILImage
import requests
import base64
from openai import OpenAI
import os
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

client = OpenAI()

def generate_image(prompt, model, size, quality, style, num_images=1):
    try:
        # response = client.images.generate(
        #     model="dall-e-3",
        #     prompt=prompt,
        #     size="1792x1024",
        #     quality="hd",
        #     n=num_images,
        #     style="natural"
        # )
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
            st.error("Failed to download the image.")
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
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
style_options = {"자연스러운": "natural", "생생한": "vivid"}
quality_options = {"표준": "standard", "HD": "hd"}
size_options = {"1024x1024": "1024x1024", "1792x1024": "1792x1024", "1024x1792": "1024x1792"}


# Style selection
selected_style = st.sidebar.selectbox("스타일", list(style_options.keys()))
style = style_options[selected_style]

# Quality selection
selected_quality = st.sidebar.selectbox("품질", list(quality_options.keys()))
quality = quality_options[selected_quality]

# Size selection
selected_size = st.sidebar.selectbox("크기", list(size_options.keys()))
size = size_options[selected_size]

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