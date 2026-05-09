import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Mascot from '../components/Mascot';
import PageTransition from '../components/PageTransition';
import { useAppStore } from '../store/useAppStore';

const Welcome = () => {
  const navigate = useNavigate();
  const resetStore = useAppStore(state => state.resetStore);

  useEffect(() => {
    resetStore();
  }, [resetStore]);

  return (
    <PageTransition>
      <div className="card" style={{ textAlign: 'center', maxWidth: 760 }}>
        <Mascot mood="greeting" message="A calm space to check in with yourself." size={170} />
        <h1 style={{ marginTop: 18, fontSize: '2.4rem' }}>Mental Wellness Assessment</h1>
        <p className="font-cursive" style={{ marginTop: 10, maxWidth: 560, marginLeft: 'auto', marginRight: 'auto', fontSize: '1.8rem' }}>
          A gentle, supportive flow to reflect, express, and get personalized guidance.
        </p>
        <button className="btn-primary" style={{ marginTop: 22, minWidth: 220 }} onClick={() => navigate('/intro')}>
          Begin
        </button>
      </div>
    </PageTransition>
  );
};

export default Welcome;
