from PIL import Image

# Função para mesclar duas imagens
def blend_images(base_image_path, overlay_image_path):
    base_img = Image.open(base_image_path)
    overlay_img = Image.open(overlay_image_path)

    # Redimensionar a imagem sobreposta para o tamanho da imagem base, se necessário
    overlay_img = overlay_img.resize(base_img.size)

    # Mesclar as imagens
    blended_img = Image.blend(base_img, overlay_img, alpha=0.5)  # alpha controla a transparência
    return blended_img
