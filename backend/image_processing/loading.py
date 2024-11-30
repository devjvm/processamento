from PIL import Image, ImageEnhance

# Função para carregar e corrigir a imagem (ajustando brilho, por exemplo)
def load_and_fix_image(image_path, brightness_factor=1.2):
    img = Image.open(image_path)

    # Ajuste de brilho
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness_factor)

    # Outros ajustes podem ser feitos aqui, como redimensionamento ou ajuste de contraste.
    return img
