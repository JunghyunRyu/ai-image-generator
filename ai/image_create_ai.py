import requests
import logging
import streamlit as st

from PIL import Image as PILImage
from io import BytesIO
from openai import OpenAI

def image_gen(prompt, model, size, quality, style):
    OpenAI.api_key=st.secrets['OPENAI_API_KEY']
    client = OpenAI()    
    full_prompt = f"Try to generate the {prompt} image.\n "
    image_response = client.images.generate(
        model=model,
        prompt=f"I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: "+full_prompt,
        size=size,
        quality=quality,
        n=1,
        style=style
    )        
    image_url = image_response.data[0].url
    logging.info(f"Image generation request successful. URL: {image_url}")

    response=requests.get(image_url)

    if response.status_code == 200:
        image = PILImage.open(BytesIO(response.content))
        logging.info("Image successfully generated and downloaded")
        return image
    else:
        error_message = f"Failed to download the image. Status code: {response.status_code}"
        logging.error(error_message)            
        return None

