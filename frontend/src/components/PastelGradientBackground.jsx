import React from 'react';

export default function PastelGradientBackground({ children, className = '', ...props }) {
  return (
    <div className={`pastel-bg-container ${className}`} {...props}>
      <style>
        {`
          .pastel-bg-container {
            position: relative;
            width: 100%;
            height: 100%;
            min-height: 100vh;
            overflow: hidden;
            background: linear-gradient(135deg, #ffe8f3, #d9f3ff);
          }
          @keyframes rotate-bg {
            0% { transform: translate(-50%, -50%) rotate(0deg); }
            100% { transform: translate(-50%, -50%) rotate(360deg); }
          }
          @keyframes rotate-bg-reverse {
            0% { transform: translate(-50%, -50%) rotate(0deg); }
            100% { transform: translate(-50%, -50%) rotate(-360deg); }
          }
          
          .pastel-bg-overlay {
            position: absolute;
            inset: 0;
            pointer-events: none;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.2), rgba(0, 0, 0, 0.1));
            z-index: 1;
          }

          .pastel-bg-layer-1 {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 200%;
            height: 200%;
            pointer-events: none;
            overflow: hidden;
            opacity: 0.8;
            filter: blur(50px);
            background: conic-gradient(from 0deg, #ff9aa2, #ffb7b2, #ffdac1, #e2f0cb, #a2e4ff, #c9afff, #ffb7b2, #ff9aa2);
            animation: rotate-bg 8s linear infinite;
            z-index: 2;
          }
          .pastel-bg-layer-2 {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 180%;
            height: 180%;
            pointer-events: none;
            overflow: hidden;
            opacity: 0.6;
            filter: blur(50px);
            background: conic-gradient(from 0deg, #ff9aa2, #ffb7b2, #ffdac1, #e2f0cb, #a2e4ff, #c9afff, #ffb7b2, #ff9aa2);
            animation: rotate-bg-reverse 10s linear infinite;
            z-index: 2;
          }
          
          .pastel-bg-content {
            position: relative;
            z-index: 10;
            width: 100%;
            height: 100%;
          }

          @keyframes float-blob {
            0%, 100% { transform: translateY(10px) translateX(0); }
            50% { transform: translateY(-10px) translateX(5px); }
          }

          .blob {
            position: absolute;
            border-radius: 50%;
            filter: blur(100px);
            opacity: 0.7;
            pointer-events: none;
            z-index: 3;
            animation: float-blob 6s ease-in-out infinite;
          }

          /* Sage */
          .blob-sage {
            background-color: #E8EFE8;
            width: 40vw;
            height: 40vw;
            top: -10%;
            left: -10%;
            animation-delay: 0s;
          }

          /* Lavender */
          .blob-lavender {
            background-color: #EFEDF4;
            width: 50vw;
            height: 50vw;
            bottom: -20%;
            right: -10%;
            animation-delay: -2s;
          }

          /* Peach */
          .blob-peach {
            background-color: #FFB7B2;
            width: 35vw;
            height: 35vw;
            top: 20%;
            left: 30%;
            animation-delay: -4s;
          }
        `}
      </style>

      {/* Container Background (Radial) */}
      <div className="pastel-bg-overlay" />

      {/* Rotating Layers */}
      <div className="pastel-bg-layer-1" />
      <div className="pastel-bg-layer-2" />

      {/* Aesthetic Floating Blobs */}
      <div className="blob blob-sage" />
      <div className="blob blob-lavender" />
      <div className="blob blob-peach" />

      {/* Content */}
      <div className="pastel-bg-content">
        {children}
      </div>
    </div>
  );
}
