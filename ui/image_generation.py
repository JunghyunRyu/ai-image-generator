import streamlit as st
import logging
from image_processor import ImageProcessor
from ai.image_create_ai import image_gen

def generate_and_process_image(new_input, model, size, quality, style, brightness, saturation, contrast, toggle_brightness, toggle_saturation, toggle_contrast):
    try:
        generated_image = image_gen(new_input, model, size, quality, style)
        image_processor = ImageProcessor(generated_image)
        adjusted_image = image_processor.adjust_image(brightness, saturation, contrast, toggle_brightness, toggle_saturation, toggle_contrast)

        if adjusted_image:
            st.session_state.inputs.insert(0, new_input)
            st.session_state.images.insert(0, adjusted_image)
            logging.info("Image successfully generated and displayed.")
            return adjusted_image
    except Exception as e:
        st.error(f"이미지 생성 중 오류 발생: {e}")
        logging.error(f"Error generating image: {e}", exc_info=True)
        return None
