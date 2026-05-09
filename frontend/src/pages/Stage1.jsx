import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Mascot from '../components/Mascot';
import PageTransition from '../components/PageTransition';
import { useAppStore } from '../store/useAppStore';
import { api } from '../services/api';

const QUESTIONS = [
  { id: 'q1', text: 'How have you been feeling lately? Describe your mood over the past few weeks.' },
  { id: 'q2', text: 'Describe a typical day in your life, from when you wake up to when you go to bed.' },
  { id: 'q3', text: 'When you think about the next few months, what comes to mind? What are you hoping for or planning?' },
  { id: 'q4', text: 'Tell me about the important people in your life and how you feel around them.' },
  { id: 'q5', text: 'How do you handle stress and challenges? What helps you cope, and what makes things harder?' },
  { id: 'q6', text: "How would you describe yourself to someone who doesn't know you?" }
];

const ENCOURAGEMENT_MESSAGES = [
  'Amazing start. Your words matter a lot.',
  'Beautiful reflection. Keep going, one question at a time.',
  'You are doing really well. I am proud of your honesty.',
  'Great depth in your answers. You are almost there.',
  'Wonderful effort. One final reflection left!'
];

const STICKER_IMAGES = [
  '/assets/images/mascot_greeting.png',
  '/assets/images/mascot_encouraging.png',
  '/assets/images/mascot_thinking.png',
  '/assets/images/mascot_comforting.png',
  '/assets/images/mascot_celebration.png'
];

const Stage1 = () => {
  const navigate = useNavigate();
  const { userName, stage1Data, setStage1Data, setStage1Result } = useAppStore();
  
  const [currentIndex, setCurrentIndex] = useState(0);
  const [currentText, setCurrentText] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);

  const wordCount = currentText.trim().split(/\s+/).filter(w => w.length > 0).length;

  const handleNext = async () => {
    if (wordCount < 10) {
      setError(`Please write at least 10 words. You have written ${wordCount}.`);
      return;
    }
    
    setError('');
    const newResponses = { ...stage1Data, [QUESTIONS[currentIndex].id]: currentText };
    setStage1Data(newResponses);

    if (currentIndex < QUESTIONS.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setCurrentText(newResponses[QUESTIONS[currentIndex + 1].id] || '');
    } else {
      // Submit to backend
      setIsLoading(true);
      try {
        const result = await api.stage1Assess(newResponses);
        setStage1Result(result);
        setShowConfetti(true);
        setTimeout(() => {
          navigate('/stage2');
        }, 3000);
      } catch (err) {
        setError(err.message || "Failed to submit. Please try again.");
      } finally {
        setIsLoading(false);
      }
    }
  };

  const progress = Math.round((currentIndex / QUESTIONS.length) * 100);
  const encouragementMessage = currentIndex > 0 ? ENCOURAGEMENT_MESSAGES[Math.min(currentIndex - 1, ENCOURAGEMENT_MESSAGES.length - 1)] : '';
  const stickerImage = currentIndex > 0 ? STICKER_IMAGES[(currentIndex - 1) % STICKER_IMAGES.length] : null;

  if (showConfetti) {
    return (
      <PageTransition>
        <Mascot mood="celebration" message={`You did great, ${userName}! Stage 1 completed!`} size={180} />
      </PageTransition>
    );
  }

  return (
    <PageTransition>
      <div className="stagger-1" style={{ width: '100%', maxWidth: '600px', marginBottom: '20px' }}>
        <div style={{ width: '100%', height: '8px', backgroundColor: 'var(--color-lavender)', borderRadius: '4px' }}>
          <div style={{ height: '100%', width: `${progress}%`, backgroundColor: 'var(--color-baby-blue-dark)', borderRadius: '4px', transition: 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1)' }}></div>
        </div>
      </div>

      <div className="stagger-2" style={{ display: 'flex', justifyContent: 'center' }}>
        <Mascot mood="thinking" message={QUESTIONS[currentIndex].text} size={150} />
      </div>
      
      <div className="card stagger-3" style={{ maxWidth: '600px', width: '100%', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <textarea
          value={currentText}
          onChange={(e) => {
            setCurrentText(e.target.value);
            if (error) setError('');
          }}
          placeholder="Share your thoughts here (minimum 10 words)..."
          className="input-field"
          rows={6}
        />

        {currentIndex > 0 && (
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              background: 'linear-gradient(90deg, #fff7f0 0%, #f4f7ff 100%)',
              border: '1px solid #e8dcff',
              borderRadius: '14px',
              padding: '10px 14px',
              animation: 'fadeIn 0.35s ease'
            }}
          >
            <img
              src={stickerImage}
              alt="Encouragement sticker"
              style={{ width: '44px', height: '44px', objectFit: 'contain', borderRadius: '50%' }}
              onError={(e) => {
                e.target.style.display = 'none';
                const fallback = document.createElement('span');
                fallback.textContent = '🐱';
                fallback.style.fontSize = '28px';
                e.target.parentElement.insertBefore(fallback, e.target);
              }}
            />
            <div style={{ color: 'var(--color-text)', fontWeight: 500, fontSize: '0.95rem' }}>
              {encouragementMessage}
            </div>
          </div>
        )}
        
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ color: wordCount < 10 ? 'var(--color-text-light)' : 'green', fontSize: '0.9rem' }}>
            {wordCount} words
          </span>
          <button 
            className="btn-primary" 
            onClick={handleNext}
            disabled={isLoading}
          >
            {isLoading ? 'Submitting...' : (currentIndex === QUESTIONS.length - 1 ? 'Complete Stage 1' : 'Next Question')}
          </button>
        </div>
        
        {error && <div className="error-text">{error}</div>}
      </div>
    </PageTransition>
  );
};

export default Stage1;
