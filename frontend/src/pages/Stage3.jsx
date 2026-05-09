import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Mascot from '../components/Mascot';
import PageTransition from '../components/PageTransition';
import { useAppStore } from '../store/useAppStore';
import { api } from '../services/api';

const QUESTIONS = [
  'I found it hard to wind down',
  'I was aware of dryness of my mouth',
  "I couldn't seem to experience any positive feeling at all",
  'I experienced breathing difficulty',
  'I found it difficult to work up the initiative to do things',
  'I tended to over-react to situations',
  'I experienced trembling',
  'I felt that I was using a lot of nervous energy',
  'I found myself in situations that made me so anxious I was most relieved when they ended',
  'I felt that I had nothing to look forward to',
  'I found myself getting agitated',
  'I found it difficult to relax',
  'I felt down-hearted and blue',
  'I was intolerant of anything that kept me from getting on with what I was doing',
  'I felt I was close to panic',
  'I was unable to become enthusiastic about anything',
  "I felt I wasn't worth much as a person",
  'I felt that I was rather touchy',
  'I was aware of the action of my heart in the absence of physical exertion',
  'I felt scared without any good reason',
  'I felt that life was meaningless',
];

const OPTIONS = [
  { value: 0, label: '0: Did not apply to me at all' },
  { value: 1, label: '1: Applied to me to some degree, or some of the time' },
  { value: 2, label: '2: Applied to me to a considerable degree, or a good part of time' },
  { value: 3, label: '3: Applied to me very much, or most of the time' }
];

const Stage3 = () => {
  const navigate = useNavigate();
  const { userName, setStage3Data, setStage3Result } = useAppStore();
  const [responses, setResponses] = useState({});
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (Object.keys(responses).length < 21) {
      setError('Please answer all 21 questions to continue.');
      return;
    }
    try {
      setLoading(true);
      const result = await api.stage3Assess(responses);
      setStage3Data(responses);
      setStage3Result(result);
      navigate('/results');
    } catch (err) {
      setError(err.message || 'Failed to submit stage 3.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageTransition>
      <div className="card" style={{ maxWidth: 920 }}>
        <Mascot mood="comforting" message={`Final step, ${userName}. Answer at your own pace.`} size={150} />
        <div style={{ display: 'grid', gap: 14, marginTop: 20 }}>
          {QUESTIONS.map((q, idx) => (
            <div key={idx} style={{ padding: 16, borderRadius: 16, background: 'rgba(255,255,255,0.72)', border: '1px solid rgba(205,180,219,0.28)' }}>
              <div style={{ marginBottom: 10, fontWeight: 600 }}>{idx + 1}. {q}</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10, flexWrap: 'wrap' }}>
                {OPTIONS.map((opt) => (
                  <label key={opt.value} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '8px 12px', borderRadius: 999, background: responses[`dass_${idx + 1}`] === opt.value ? 'rgba(230,230,250,0.85)' : 'transparent', border: '1px solid rgba(205,180,219,0.35)' }}>
                    <input type="radio" name={`dass_${idx + 1}`} checked={responses[`dass_${idx + 1}`] === opt.value} onChange={() => setResponses((prev) => ({ ...prev, [`dass_${idx + 1}`]: opt.value }))} />
                    <span style={{ fontSize: '0.95rem' }}>{opt.label}</span>
                  </label>
                ))}
              </div>
            </div>
          ))}
        </div>
        <button className="btn-primary" style={{ marginTop: 18, width: '100%' }} onClick={handleSubmit} disabled={loading}>
          {loading ? 'Computing Results…' : 'View My Results'}
        </button>
        {error ? <div className="error-text" style={{ marginTop: 12 }}>{error}</div> : null}
      </div>
    </PageTransition>
  );
};

export default Stage3;
