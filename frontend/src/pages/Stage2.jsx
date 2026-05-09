import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Mascot from '../components/Mascot';
import PageTransition from '../components/PageTransition';
import { useAppStore } from '../store/useAppStore';
import { api } from '../services/api';

const Stage2 = () => {
  const navigate = useNavigate();
  const { userId, userName, setStage2Data, setStage2Result } = useAppStore();
  const [image, setImage] = useState(null);
  const [response, setResponse] = useState('');
  const [error, setError] = useState('');
  const [loadingImage, setLoadingImage] = useState(true);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const loadImage = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_FRONTEND_API_BASE_URL || 'http://localhost:8000'}/stage2/image/${userId}`);
        if (res.ok) {
          setImage(await res.json());
        }
      } catch (e) {
        setError('Could not load image.');
      } finally {
        setLoadingImage(false);
      }
    };
    loadImage();
  }, [userId]);

  const handleSubmit = async () => {
    if (response.trim().split(/\s+/).filter(Boolean).length < 10) {
      setError('Please write at least 10 words.');
      return;
    }
    try {
      const result = await api.stage2Assess(response, image?.id);
      setStage2Data({ response, image_id: image?.id, image_path: image?.file });
      setStage2Result(result);
      navigate('/stage3');
    } catch (err) {
      setError(err.message || 'Failed to submit stage 2.');
    }
  };

  return (
    <PageTransition>
      <div className="card" style={{ maxWidth: 760 }}>
        <Mascot mood="encouraging" message={`Take a look, ${userName}. Share what you notice.`} size={150} />
        {loadingImage ? (
          <div style={{ padding: 24, textAlign: 'center', color: 'var(--color-text-light)' }}>Loading image…</div>
        ) : (
          <>
            <div style={{ marginTop: 18, borderRadius: 18, overflow: 'hidden', position: 'relative' }}>
              {image?.file ? <img src={`/${image.file}`} alt={image.title} style={{ width: '100%', display: 'block', maxHeight: 360, objectFit: 'cover' }} /> : null}
              <button className="btn-secondary" style={{ position: 'absolute', right: 14, bottom: 14 }} onClick={() => setShowModal(true)}>
                Open Image
              </button>
            </div>
            <textarea
              className="input-field"
              style={{ marginTop: 18 }}
              rows={6}
              value={response}
              onChange={(e) => setResponse(e.target.value)}
              placeholder="Describe what you notice in the image..."
            />
            <button className="btn-primary" style={{ marginTop: 16, width: '100%' }} onClick={handleSubmit}>
              Complete Stage 2
            </button>
            {error ? <div className="error-text" style={{ marginTop: 12 }}>{error}</div> : null}
          </>
        )}
      </div>

      {showModal && image?.file ? (
        <div
          role="dialog"
          aria-modal="true"
          onClick={() => setShowModal(false)}
          style={{ position: 'fixed', inset: 0, background: 'rgba(20,20,30,0.55)', display: 'grid', placeItems: 'center', zIndex: 20, padding: 16 }}
        >
          <div onClick={(e) => e.stopPropagation()} style={{ maxWidth: '92vw', maxHeight: '88vh' }}>
            <button className="btn-secondary" onClick={() => setShowModal(false)} style={{ marginBottom: 12, float: 'right' }}>Close</button>
            <img src={`/${image.file}`} alt={image.title} style={{ maxWidth: '92vw', maxHeight: '82vh', borderRadius: 18, display: 'block' }} />
          </div>
        </div>
      ) : null}
    </PageTransition>
  );
};

export default Stage2;
