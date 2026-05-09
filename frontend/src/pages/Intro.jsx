import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Mascot from '../components/Mascot';
import PageTransition from '../components/PageTransition';
import { useAppStore } from '../store/useAppStore';

const Intro = () => {
  const navigate = useNavigate();
  const { userName, setUserName } = useAppStore();
  const [localName, setLocalName] = useState(userName || '');

  const handleContinue = () => {
    if (localName.trim()) {
      setUserName(localName.trim());
      navigate('/stage1');
    }
  };

  return (
    <PageTransition>
      <div className="card" style={{ maxWidth: 560, textAlign: 'center' }}>
        <Mascot mood="greeting" message="Hi. What name should I use for you?" size={160} />
        <input
          className="input-field"
          style={{ marginTop: 18 }}
          value={localName}
          onChange={(e) => setLocalName(e.target.value)}
          placeholder="Enter your name"
          onKeyDown={(e) => e.key === 'Enter' && handleContinue()}
        />
        <button className="btn-primary" style={{ marginTop: 18, width: '100%' }} onClick={handleContinue} disabled={!localName.trim()}>
          Continue
        </button>
      </div>
    </PageTransition>
  );
};

export default Intro;
