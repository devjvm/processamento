from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS  # type: ignore # Importando o CORS
import os
import base64
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

# Variáveis globais para controle de desenho
drawing = False
ix, iy = -1, -1
img = None  # Imagem global para controle do desenho
coordinates = []

# Configurações
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov'}  # Adicionando formatos de vídeo
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Limite de 50MB para o upload de vídeo


# Função para verificar se o arquivo é permitido
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Função para capturar coordenadas do clique e marcar os pontos clicados com vermelho
def capturar_coordenadas(event, x, y, flags, param):
    global ix, iy, drawing, img, coordinates
    if event == cv2.EVENT_LBUTTONDOWN:  # Evento de clique do botão esquerdo
        if len(coordinates) < 4:
            coordinates.append((x, y))  # Armazena as coordenadas do clique
            print(f"Coordenadas do clique: x={x}, y={y}, total de cliques: {len(coordinates)}")
            # Desenha um círculo vermelho onde o usuário clicou
            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)  # Ponto vermelho
            if len(coordinates) == 4:
                # Desenha o retângulo após capturar os 4 pontos
                ponto_superior_esquerdo = coordinates[0]
                ponto_inferior_direito = coordinates[2]
                cor = (0, 0, 255)  # Cor do retângulo (vermelho)
                espessura = 2      # Espessura da linha
                cv2.rectangle(img, ponto_superior_esquerdo, ponto_inferior_direito, cor, espessura)
                print(f"Retângulo desenhado: {ponto_superior_esquerdo} - {ponto_inferior_direito}")


# Função para desenhar na imagem
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, img
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.line(img, (ix, iy), (x, y), (0, 0, 255), 5)
            ix, iy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(img, (ix, iy), (x, y), (0, 0, 255), 5)

# Rota para upload de imagem
@app.route('/upload', methods=['POST'])
def upload_image():
    global coordinates  # Adicionamos aqui para garantir que as coordenadas sejam limpas a cada upload
    coordinates = []  # Limpa as coordenadas sempre que uma nova imagem for carregada
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo encontrado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({"message": "Imagem carregada com sucesso", "filename": filename}), 200
    else:
        return jsonify({"error": "Arquivo não permitido"}), 400

# Rota para upload de vídeo
@app.route('/upload-video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo encontrado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({"message": "Vídeo carregado com sucesso", "filename": filename}), 200
    else:
        return jsonify({"error": "Arquivo não permitido"}), 400

# Rota para aplicar o filtro azul na imagem
@app.route('/image-blue', methods=['POST'])
def image_blue():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo encontrado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        img = cv2.imread(filepath)

        if img is None:
            return jsonify({"error": "Imagem não carregada corretamente"}), 400

        # Manipular os canais da imagem para aplicar o filtro azul
        blue_image = img.copy()
        blue_image[:, :, 1] = 0  # Zera o canal verde
        blue_image[:, :, 2] = 0  # Zera o canal vermelho

        # Salvar a imagem modificada
        blue_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"blue_{filename}")
        cv2.imwrite(blue_image_path, blue_image)

        # Retorna a URL da imagem processada para o frontend
        return jsonify({
            "message": "Imagem transformada para azul com sucesso!",
            "blue_image_url": f'http://localhost:5000/uploads/blue_{filename}'
        }), 200
    else:
        return jsonify({"error": "Arquivo não permitido"}), 400

# Rota para desenhar na imagem
@app.route('/draw', methods=['POST'])
def draw_on_image():
    global img
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo encontrado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        img = cv2.imread(filepath)

        if img is None:
            return jsonify({"error": "Imagem não carregada corretamente"}), 400

        # Exibir a imagem e permitir que o usuário desenhe
        cv2.imshow('Imagem desenhar', img)
        cv2.setMouseCallback('Imagem desenhar', draw_circle)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Salvar a imagem modificada
        drawn_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"drawn_{filename}")
        cv2.imwrite(drawn_image_path, img)

        return jsonify({
            "message": "Imagem desenhada com sucesso!",
            "drawn_image_url": f'http://localhost:5000/uploads/drawn_{filename}'
        }), 200
    else:
        return jsonify({"error": "Arquivo não permitido"}), 400

# Rota para marcar o retângulo na imagem   
@app.route('/marcar-retangulo', methods=['POST'])
def marcar_retangulo():
    global img, coordinates
    coordinates = []  # Limpa as coordenadas toda vez que a rota é chamada
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo encontrado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        img = cv2.imread(filepath)

        if img is None:
            return jsonify({"error": "Imagem não carregada corretamente"}), 400

        # Exibir a imagem e permitir que o usuário clique nos pontos
        cv2.imshow('Imagem', img)
        cv2.setMouseCallback('Imagem', capturar_coordenadas)  # Chama a função para capturar coordenadas
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Verifica se temos 4 coordenadas
        if len(coordinates) == 4:
            # Salva a imagem com o retângulo desenhado
            retangulo_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"retangulo_{filename}")
            cv2.imwrite(retangulo_image_path, img)

            return jsonify({
                "message": "Retângulo desenhado com sucesso!",
                "retangulo_image_url": f'http://localhost:5000/uploads/retangulo_{filename}'
            }), 200
        else:
            return jsonify({"error": "Você deve clicar em 4 pontos para marcar o retângulo."}), 400
    else:
        return jsonify({"error": "Arquivo não permitido"}), 400

# Rota para a detecção de faces em vídeos
@app.route('/face-detection', methods=['POST'])
def face_detection():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo encontrado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Carregar o classificador Haar para detectar faces
        face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

        # Verificar se o classificador foi carregado corretamente
        if face_cascade.empty():
            return jsonify({"error": "Erro ao carregar o classificador Haar!"}), 400

        # Abrir o vídeo
        cap = cv2.VideoCapture(filepath)

        # Verificar se o vídeo foi aberto corretamente
        if not cap.isOpened():
            return jsonify({"error": "Erro ao abrir o vídeo!"}), 400

        # Prepare o arquivo de saída para salvar o vídeo com faces detectadas
        output_filename = f"output_{filename}"
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para o vídeo de saída
        out = cv2.VideoWriter(output_filepath, fourcc, 20.0, (640, 480))

        # Processar o vídeo quadro por quadro
        while True:
            ret, frame = cap.read()

            if not ret:
                break  # Se não houver mais quadros, saímos do loop

            # Converter o quadro para escala de cinza
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detectar as faces no quadro atual
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Desenhar um retângulo ao redor de cada face detectada
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)  # Desenhar retângulo vermelho

            # Exibir o quadro com a detecção de faces em tempo real
            cv2.imshow('Detecção de Faces', frame)

            # Esperar 1ms e verificar se a tecla 'q' foi pressionada para sair
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Escrever o quadro com a detecção de faces no arquivo de saída
            out.write(frame)

        # Liberar o vídeo e fechar a janela de exibição
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        return jsonify({
            "message": "Detecção de faces realizada com sucesso!",
            "output_video_url": f'http://localhost:5000/uploads/{output_filename}'
        }), 200

    else:
        return jsonify({"error": "Arquivo não permitido"}), 400

# Rota para servir as imagens estáticas
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
