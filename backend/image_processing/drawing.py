from PIL import Image, ImageDraw

# Função para desenhar sobre a imagem
def draw_on_image(image_path, annotations):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Desenhar formas ou adicionar anotações (exemplo)
    for annotation in annotations:
        shape = annotation.get("shape", "rectangle")
        coords = annotation.get("coords", [0, 0, 100, 100])
        color = annotation.get("color", "red")
        if shape == "rectangle":
            draw.rectangle(coords, outline=color)
        elif shape == "ellipse":
            draw.ellipse(coords, outline=color)
        # Outros tipos de desenhos podem ser adicionados aqui (linhas, polígonos, etc.)

    return img
