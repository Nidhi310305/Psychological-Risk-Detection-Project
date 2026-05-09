import React from 'react';

const moodImages = {
  greeting: '/assets/images/mascot_greeting.png',
  thinking: '/assets/images/mascot_thinking.png',
  encouraging: '/assets/images/mascot_encouraging.png',
  celebration: '/assets/images/mascot_celebration.png',
  comforting: '/assets/images/mascot_comforting.png'
};

const moodLabels = {
  greeting: 'greeting',
  thinking: 'thinking',
  encouraging: 'encouraging',
  celebration: 'celebration',
  comforting: 'comforting'
};

const Mascot = ({ mood = 'greeting', message = '', size = 140 }) => {
  const label = moodLabels[mood] || 'greeting';
  const imageSrc = moodImages[mood] || moodImages.greeting;

  return (
    <div style={{ textAlign: 'center', maxWidth: '100%' }}>
      <div
        aria-hidden="true"
        style={{
          width: size,
          height: size,
          margin: '0 auto',
          borderRadius: '50%',
          background: 'radial-gradient(circle at 30% 30%, rgba(255,255,255,0.95), rgba(255,200,221,0.6) 45%, rgba(205,180,219,0.55) 100%)',
          boxShadow: '0 10px 30px rgba(205,180,219,0.22), inset 0 0 0 2px rgba(255,255,255,0.55)',
          display: 'grid',
          placeItems: 'center',
          overflow: 'hidden',
          transform: 'translateZ(0)',
        }}
      >
        <img
          src={imageSrc}
          alt={`Mascot cat — ${label}`}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            borderRadius: '50%',
          }}
          onError={(e) => {
            // Fallback to emoji if image fails to load
            e.target.style.display = 'none';
            e.target.parentElement.textContent = '🐾';
            e.target.parentElement.style.fontSize = `${size * 0.38}px`;
            e.target.parentElement.style.lineHeight = '1';
          }}
        />
      </div>
      {message ? (
        <div style={{ marginTop: 12, color: 'var(--color-text)', fontWeight: 500 }}>
          {message}
        </div>
      ) : null}
      <div style={{ marginTop: 6, color: 'var(--color-text-light)', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
        {label}
      </div>
    </div>
  );
};

export default Mascot;
