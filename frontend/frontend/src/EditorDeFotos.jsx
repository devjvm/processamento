import React, { useState } from 'react';
import './EditorDeFotos.css';  // Importando o CSS

function EditorDeFotos() {
  const [image, setImage] = useState(null); // Imagem original carregada
  const [uploadedImage, setUploadedImage] = useState(null); // Imagem enviada ao backend
  const [drawnImage, setDrawnImage] = useState(null); // Imagem com desenho
  const [markedImage, setMarkedImage] = useState(null); // Imagem com retângulo
  const [message, setMessage] = useState(''); // Mensagem para o usuário

  // Função para carregar a imagem e preparar para edição
  const loadImage = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const img = new Image();
        img.src = reader.result;
        img.onload = () => {
          setImage(img);  // Define a imagem original
          setMessage('');  // Limpa a mensagem se uma imagem for carregada
        };
      };
      reader.readAsDataURL(file);
    } else {
      setMessage('CARREGUE SUA IMAGEM'); // Exibe a mensagem caso nenhum arquivo seja carregado
    }
  };

  // Função para aplicar o filtro azul
  const applyBlueFilter = async () => {
    const file = document.querySelector('input[type="file"]').files[0]; // Pega o arquivo de imagem carregado
  
    if (!file) {
      console.error('Nenhuma imagem carregada.');
      setMessage('CARREGUE SUA IMAGEM');  // Exibe a mensagem se não houver imagem
      return;
    }
  
    const formData = new FormData();
    formData.append('file', file); // Envia o arquivo de imagem no FormData
  
    try {
      const response = await fetch('http://localhost:5000/image-blue', {
        method: 'POST',
        body: formData,  // Envia o FormData com a imagem
      });
  
      const data = await response.json();
      if (response.ok) {
        console.log('Imagem transformada para azul');
        window.open(data.blue_image_url, "_blank");  // Abre a imagem azul em uma nova janela
      } else {
        console.error('Erro ao aplicar o filtro azul:', data.error);
      }
    } catch (error) {
      console.error('Erro de conexão com o backend:', error);
    }
  };

  // Função para desenhar na imagem
  const handleDraw = async () => {
    const file = document.querySelector('input[type="file"]').files[0]; // Pega o arquivo de imagem carregado
  
    if (!file) {
      console.error('Nenhuma imagem carregada.');
      setMessage('CARREGUE SUA IMAGEM');  // Exibe a mensagem se não houver imagem
      return;
    }
  
    const formData = new FormData();
    formData.append('file', file); // Envia o arquivo de imagem no FormData
  
    try {
      const response = await fetch('http://localhost:5000/draw', {
        method: 'POST',
        body: formData,  // Envia o FormData com a imagem
      });
  
      const data = await response.json();
      if (response.ok) {
        console.log('Imagem desenhada');
        setDrawnImage(data.drawn_image_url);  // Atualiza a imagem desenhada
        setMarkedImage(null); // Limpa a imagem com retângulo
      } else {
        console.error('Erro ao desenhar na imagem:', data.error);
      }
    } catch (error) {
      console.error('Erro de conexão com o backend:', error);
    }
  };

  // Função para marcar o retângulo na imagem
  const handleMarkRectangle = async () => {
    const file = document.querySelector('input[type="file"]').files[0]; // Pega o arquivo de imagem carregado
  
    if (!file) {
      console.error('Nenhuma imagem carregada.');
      setMessage('CARREGUE SUA IMAGEM');  // Exibe a mensagem se não houver imagem
      return;
    }
  
    const formData = new FormData();
    formData.append('file', file); // Envia o arquivo de imagem no FormData
  
    try {
      const response = await fetch('http://localhost:5000/marcar-retangulo', {
        method: 'POST',
        body: formData,  // Envia o FormData com a imagem
      });
  
      const data = await response.json();
      if (response.ok) {
        console.log('Retângulo desenhado');
        setMarkedImage(data.retangulo_image_url);  // Atualiza a imagem com o retângulo
        setDrawnImage(null); // Limpa a imagem desenhada
      } else {
        console.error('Erro ao desenhar o retângulo:', data.error);
      }
    } catch (error) {
      console.error('Erro de conexão com o backend:', error);
    }
  };

  // Função para limpar a imagem e recarregar
  const refreshPage = () => {
    setImage(null);  // Limpa a imagem carregada
    setUploadedImage(null);  // Limpa a imagem enviada ao backend
    setDrawnImage(null);  // Limpa a imagem desenhada
    setMarkedImage(null);  // Limpa a imagem com retângulo
    setMessage('');  // Limpa a mensagem de erro
    document.querySelector('input[type="file"]').value = '';  // Limpa o campo de upload
  };

  return (
    <div className="editor-container">
      <h2>Editor de Fotos Interativo</h2>

      {/* Exibe a mensagem se não houver imagem carregada */}
      {message && <p style={{ color: 'red' }}>{message}</p>}

      <div style={{ display: 'flex', alignItems: 'center' }}>
        <input
          type="file"
          accept="image/*"
          onChange={loadImage}
          style={{ marginRight: '10px' }}
        />
        {/* Botão de refresh */}
        <button onClick={refreshPage} style={{ backgroundColor: 'red', color: 'white' }}>
          Refresh
        </button>
      </div>

      <div style={{ position: 'relative' }}>
        {/* Exibe o texto "CARREGUE SUA IMAGEM" quando não houver imagem */}
        {!image && !message && <p>CARREGUE SUA IMAGEM</p>}

        {/* Exibe a imagem carregada (original) */}
        {image && (
          <img
            src={image.src}
            alt="Imagem para editar"
            style={{ display: 'block', marginTop: '20px', maxWidth: '100%' }}
          />
        )}
      </div>

      <div>
        <button onClick={() => setImage(null)}>Limpar Imagem</button>
        <button onClick={applyBlueFilter}>Imagem AZUL</button>
        <button onClick={handleDraw}>Desenhar na Imagem</button>
        <button onClick={handleMarkRectangle}>Marcar Retângulo</button>  {/* Novo botão para marcar o retângulo */}
      </div>

      {/* Exibe a imagem desenhada */}
      {drawnImage && (
        <div>
          <h3>Imagem Desenhada</h3>
          <img
            src={drawnImage}
            alt="Imagem desenhada"
            style={{ maxWidth: '100%' }}
          />
        </div>
      )}

      {/* Exibe a imagem com o retângulo desenhado */}
      {markedImage && (
        <div>
          <h3>Imagem com Retângulo</h3>
          <img
            src={markedImage}
            alt="Imagem com retângulo"
            style={{ maxWidth: '100%' }}
          />
        </div>
      )}
    </div>
  );
}

export default EditorDeFotos;
