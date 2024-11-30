import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom';
import './App.css';

// Importando os componentes das páginas
import EditorDeFotos from './EditorDeFotos';
import SistemaDeVigilancia from './SistemaDeVigilancia';
import DP from './DP';

// Componente da Sidebar
function Sidebar() {
  const location = useLocation();

  return (
    <div className="sidebar">
      <ul>
        <li>
          <Link to="/EditorDeFotos" className={location.pathname === '/EditorDeFotos' ? 'active' : ''}>
            Editor de Fotos Interativo
          </Link>
        </li>
        <li>
          <Link to="/sistema-vigilancia" className={location.pathname === '/sistema-vigilancia' ? 'active' : ''}>
            Sistema de Vigilância
          </Link>
        </li>
        <li>
          <Link to="/dp" className={location.pathname === '/dp' ? 'active' : ''}>
            DP
          </Link>
        </li>
      </ul>
    </div>
  );
}

// Componente principal com as rotas
function App() {
  return (
    <Router>
      <div className="app">
        <Sidebar />
        <div className="content">
          <Routes>
            <Route path="/EditorDeFotos" element={<EditorDeFotos />} />
            <Route path="/sistema-vigilancia" element={<SistemaDeVigilancia />} />
            <Route path="/dp" element={<DP />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
