import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Welcome from './pages/Welcome.jsx';
import Intro from './pages/Intro.jsx';
import Stage1 from './pages/Stage1.jsx';
import Stage2 from './pages/Stage2.jsx';
import Stage3 from './pages/Stage3.jsx';
import Results from './pages/Results.jsx';
import PastelGradientBackground from './components/PastelGradientBackground.jsx';

function App() {
  return (
    <BrowserRouter>
      <PastelGradientBackground>
        <div className="app-shell">
          <Routes>
            <Route path="/" element={<Navigate to="/welcome" replace />} />
            <Route path="/welcome" element={<Welcome />} />
            <Route path="/intro" element={<Intro />} />
            <Route path="/stage1" element={<Stage1 />} />
            <Route path="/stage2" element={<Stage2 />} />
            <Route path="/stage3" element={<Stage3 />} />
            <Route path="/results" element={<Results />} />
            <Route path="*" element={<Navigate to="/welcome" replace />} />
          </Routes>
        </div>
      </PastelGradientBackground>
    </BrowserRouter>
  );
}

export default App;
