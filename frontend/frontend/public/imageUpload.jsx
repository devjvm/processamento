import { useState } from 'react';

function ImageUpload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  // Função para lidar com o envio de arquivo
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Nenhuma imagem selecionada!');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message);
      } else {
        setMessage(data.error);
      }
    } catch (error) {
      setMessage('Erro ao enviar a imagem.');
    }
  };

  return (
    <div>
      <h2>Carregar Imagem</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <p>{message}</p>
    </div>
  );
}

export default ImageUpload;
