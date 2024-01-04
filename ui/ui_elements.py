import streamlit as st

def display_header():
    st.markdown("""
        <h1 style='text-align: center; color: #ff6347; font-family: Comic Sans MS;'>
            🎨 AI Generated Images Gallery 🌌
        </h1>
        <p style='text-align: center; font-size: 20px; font-family: Comic Sans MS;'>
            Explore the creativity of AI-generated art! ✨
        </p>
    """, unsafe_allow_html=True)

def get_user_input():
    return st.text_area("Enter your image description here:")

def image_adjustment_controls(default_brightness=50, default_saturation=50, default_contrast=50):
    with st.expander("설정"):
        col1, col2, col3 = st.columns(3)
        brightness, saturation, contrast = default_brightness, default_saturation, default_contrast
        toggle_brightness, toggle_saturation, toggle_contrast = False, False, False

        with col1:
            toggle_brightness = st.toggle("명도 조절", False)
            if toggle_brightness:
                brightness = st.slider("명도", 0, 100, default_brightness)
            st.write(f"현재 명도: {brightness}%")

        with col2:
            toggle_saturation = st.toggle("채도 조절", False)
            if toggle_saturation:
                saturation = st.slider("채도", 0, 100, default_saturation)
            st.write(f"현재 채도: {saturation}%")

        with col3:
            toggle_contrast = st.toggle("대비 조절", False)
            if toggle_contrast:
                contrast = st.slider("대비", 0, 100, default_contrast)
            st.write(f"현재 대비: {contrast}%")
        
        return brightness, saturation, contrast, toggle_brightness, toggle_saturation, toggle_contrast
