import streamlit as st

class UIConfig:
    def __init__(self):
        self.model_options = ["dall-e-3"]
        self.style_options = {"Natural": "natural", "Vivid": "vivid"}
        self.quality_options = {"Standard": "standard", "HD": "hd"}
        self.size_options = {"1024x1024": "1024x1024", "1792x1024": "1792x1024", "1024x1792": "1024x1792"}

    def select_model(self):
        return st.sidebar.selectbox("Model", self.model_options, index=0)

    def select_style(self):
        selected_style = st.sidebar.selectbox("Style", list(self.style_options.keys()))
        return self.style_options[selected_style]

    def select_quality(self):
        selected_quality = st.sidebar.selectbox("Quality", list(self.quality_options.keys()))
        return self.quality_options[selected_quality]

    def select_size(self):
        selected_size = st.sidebar.selectbox("Size", list(self.size_options.keys()))
        return self.size_options[selected_size]
