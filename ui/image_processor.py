from PIL import ImageEnhance

class ImageProcessor:
    def __init__(self, image):
        self.image = image

    # 이미지 생성 및 조정 함수
    def adjust_image(self, brightness=50, saturation=50, contrast=50, toggle_brightness=False, toggle_saturation=False, toggle_contrast=False):
        # PIL의 기준에 맞게 값 변환
        brightness_scale = brightness / 50  # 예: 100 -> 2.0, 50 -> 1.0, 0 -> 0.0
        saturation_scale = saturation / 50
        contrast_scale = contrast / 50

        # 명도 조정
        if toggle_brightness:
            enhancer = ImageEnhance.Brightness(self.image)
            self.image = enhancer.enhance(brightness_scale)

        # 채도 조정
        if toggle_saturation:
            enhancer = ImageEnhance.Color(self.image)
            self.image = enhancer.enhance(saturation_scale)

        # 대비 조정
        if toggle_contrast:
            enhancer = ImageEnhance.Contrast(self.image)
            self.image = enhancer.enhance(contrast_scale)

        return self.image
