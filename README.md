
# README

## Descrição do Projeto

O PROJETO FOI POSTADO NO GITHUB PARA QUE SEJA MAIS FÁCIL SER VISUALIZADO

Este projeto visa criar uma aplicação de processamento de imagem e vídeo, utilizando conceitos de visão computacional para realizar detecção de faces, edição de imagens e manipulação de vídeos. O sistema foi desenvolvido utilizando **Python** e **Flask** para o backend, **OpenCV** para o processamento de imagem e vídeo, e **React/Vite** para o frontend.

### Objetivo

A aplicação é voltada para **processamento de imagens** e **vídeos**, com funcionalidades específicas para:
1. Carregar imagens e realizar correções básicas.
2. Permitir a interação do usuário com a imagem (desenho e marcação).
3. Realizar detecção de faces em vídeos.
4. Oferecer uma interface interativa para o usuário com a possibilidade de visualizar vídeos processados em tempo real.

### Funcionalidades

1. **Carregamento de Imagens**: O usuário pode enviar uma imagem para ser processada. O sistema permite realizar correções como transformar a imagem em azul (aplicando um filtro), além de possibilitar o desenho na imagem, o que pode incluir a marcação de retângulos.

![Texto alternativo](C:\Users\jvict\OneDrive\Área de Trabalho\processamento\imagens_readme\img1.png)

![Texto alternativo](C:\Users\jvict\OneDrive\Área de Trabalho\processamento\imagens_readme\img2.jpg)

2. **Detecção de Faces em Vídeos**: O sistema utiliza a biblioteca OpenCV para processar vídeos e detectar faces quadro a quadro. As faces detectadas são destacadas com retângulos vermelhos. O vídeo processado é mostrado em tempo real no backend.

3. **Frontend Interativo**: O frontend foi desenvolvido com React e Vite, onde o usuário pode:
   - Enviar imagens ou vídeos.
   - Visualizar o vídeo com a detecção de faces em tempo real.
   - Interagir com as imagens desenhando sobre elas.

---

## Funcionalidades Backend

### 1. **Upload de Imagens** (`/upload`)
- Rota para enviar uma imagem para o servidor.
- A imagem é salva no servidor e pode ser processada.

### 2. **Upload de Vídeos** (`/upload-video`)
- Rota para enviar vídeos para o servidor.
- O vídeo é salvo no servidor e pode ser utilizado para detecção de faces.

### 3. **Transformação para Imagem Azul** (`/image-blue`)
- Recebe uma imagem e aplica um filtro azul, apagando os canais vermelho e verde.
- Retorna a URL da imagem modificada.

### 4. **Desenho na Imagem** (`/draw`)
- Permite que o usuário desenhe sobre a imagem utilizando o mouse.
- O usuário pode desenhar linhas e formas sobre a imagem e visualizar as alterações em tempo real.

### 5. **Marcação de Retângulo na Imagem** (`/marcar-retangulo`)
- O usuário pode clicar em 4 pontos da imagem para desenhar um retângulo. Esse retângulo é desenhado com base nas coordenadas fornecidas pelo usuário.

### 6. **Detecção de Faces em Vídeos** (`/face-detection`)
- Realiza a detecção de faces em vídeos enviados.
- O vídeo processado é mostrado em tempo real com as faces detectadas e é salvo no servidor.

---

## Funcionalidades Frontend

### **EditorDeFotos.jsx**
- Permite que o usuário carregue uma imagem, visualize-a e aplique o filtro azul.
- Inclui a funcionalidade de desenhar na imagem utilizando o mouse. O desenho inclui a possibilidade de desenhar linhas.
- O código também permite marcar um retângulo na imagem, utilizando um clique para selecionar 4 pontos.

### **SistemaDeVigilancia.jsx**
- Permite que o usuário envie um vídeo para ser processado.
- O vídeo é exibido em tempo real com a detecção de faces, onde o usuário vê as faces sendo detectadas quadro a quadro.
- Ao clicar no botão "Face Detection", o backend processa o vídeo e retorna um vídeo com as faces detectadas, que é exibido em tempo real.

---

## Tecnologias Usadas

- **Backend**:
  - **Flask**: Framework para a criação da API.
  - **OpenCV**: Biblioteca utilizada para o processamento de imagens e vídeos (filtro azul, desenho, detecção de faces).
  - **Python**: Linguagem de programação principal utilizada no projeto.
  
- **Frontend**:
  - **React**: Framework para o desenvolvimento da interface interativa.
  - **Vite**: Ferramenta para criar e servir o aplicativo React.

---

## Como Rodar o Projeto

### Requisitos:
1. **Python 3.x**
2. **Node.js (para rodar o frontend)**

### Backend:
1. Instale as dependências do backend com o comando:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o backend:
   ```bash
   python app.py
   ```
3. O servidor estará disponível em `http://localhost:5000`.

### Frontend:
1. Instale as dependências do frontend com o comando:
   ```bash
   npm install
   ```
2. Execute o frontend:
   ```bash
   npm run dev
   ```
3. O frontend estará disponível em `http://localhost:3000`.

---

## Desafios Enfrentados

- A implementação de **detecção de faces em vídeos** foi um desafio, pois envolveu processar o vídeo quadro a quadro em tempo real, garantindo que o sistema fosse eficiente o suficiente para vídeos maiores.
- **Sincronização entre o frontend e o backend** também foi um ponto importante, principalmente ao trabalhar com vídeos de tamanho considerável, o que exigiu a implementação de um sistema eficiente de upload e processamento de arquivos.

