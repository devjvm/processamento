import React, { useState } from 'react';
import './SistemaDeVigilancia.css';

function SistemaDeVigilancia() {
  const [videoFile, setVideoFile] = useState(null); // Vídeo carregado
  const [videoUrl, setVideoUrl] = useState(null); // URL do vídeo para exibição
  const [outputVideoUrl, setOutputVideoUrl] = useState(null); // URL do vídeo processado com faces detectadas
  const [message, setMessage] = useState(''); // Mensagem para o usuário

  // Função para carregar o vídeo e preparar para exibição
  const handleVideoUpload = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('video/')) {
      setVideoFile(file);
      setVideoUrl(URL.createObjectURL(file)); // Exibe o vídeo na tela
    } else {
      setMessage('Por favor, envie um arquivo de vídeo.');
    }
  };

  // Função para chamar o endpoint de detecção de faces
  const handleFaceDetection = async () => {
    if (!videoFile) {
      setMessage('Por favor, carregue um vídeo primeiro.');
      return;
    }

    const formData = new FormData();
    formData.append('file', videoFile); // Envia o arquivo de vídeo no FormData

    try {
      const response = await fetch('http://localhost:5000/face-detection', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setOutputVideoUrl(data.output_video_url); // Exibe o vídeo com faces detectadas
        setMessage('Detecção de faces concluída com sucesso!');
      } else {
        setMessage(data.error || 'Erro ao processar o vídeo.');
      }
    } catch (error) {
      console.error('Erro de conexão com o backend:', error);
      setMessage('Erro ao conectar com o backend.');
    }
  };

  return (
    <div className="vigilancia-container">
      <h2>Sistema de Vigilância - Detecção de Faces</h2>

      {/* Exibe mensagem de erro ou sucesso */}
      {message && <p>{message}</p>}

      {/* Formulário de upload de vídeo */}
      <input type="file" accept="video/*" onChange={handleVideoUpload} />
      
      {/* Exibe o vídeo carregado */}
      {videoUrl && (
        <div>
          <h3>Vídeo Carregado</h3>
          <video width="600" controls>
            <source src={videoUrl} type="video/mp4" />
            Seu navegador não suporta a tag de vídeo.
          </video>
        </div>
      )}

      {/* Botão para realizar a detecção de faces */}
      <button onClick={handleFaceDetection}>Face Detection</button>

      {/* Exibe o vídeo com faces detectadas após processamento */}
      {outputVideoUrl && (
        <div>
          <h3>Vídeo com Detecção de Faces</h3>
          <video width="600" controls>
            <source src={outputVideoUrl} type="video/mp4" />
            Seu navegador não suporta a tag de vídeo.
          </video>
        </div>
      )}
    </div>
  );
}

export default SistemaDeVigilancia;
