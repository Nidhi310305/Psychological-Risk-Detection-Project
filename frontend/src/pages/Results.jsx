import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Mascot from '../components/Mascot';
import PageTransition from '../components/PageTransition';
import { useAppStore } from '../store/useAppStore';
import { api } from '../services/api';
import { Download, Share2, Info } from 'lucide-react';
import CardSwap, { Card } from '../components/CardSwap';

const Results = () => {
  const navigate = useNavigate();
  const { userName, stage1Result, stage2Result, stage3Result, setFinalResult, resetStore } = useAppStore();
  
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [expandedSection, setExpandedSection] = useState(null);

  useEffect(() => {
    // If not completed properly, send back
    if (!stage1Result || !stage2Result || !stage3Result) {
      navigate('/welcome');
      return;
    }

    const fetchFinal = async () => {
      try {
        const result = await api.finalAssess(stage1Result, stage2Result, stage3Result);
        setFinalResult(result);
        setData(result);
      } catch (err) {
        setError(err.message || 'Failed to process final results.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchFinal();
  }, [stage1Result, stage2Result, stage3Result, navigate, setFinalResult]);

  const handleRestart = () => {
    resetStore();
    navigate('/welcome');
  };

  if (loading) {
    return <PageTransition><Mascot mood="thinking" message="Analyzing your beautiful thoughts..." size={200} /></PageTransition>;
  }

  if (error) {
    return (
      <PageTransition>
        <Mascot mood="comforting" message="Something went wrong while computing your results." size={150} />
        <div className="card" style={{ maxWidth: '500px', width: '100%', textAlign: 'center' }}>
          <p className="error-text">{error}</p>
          <button className="btn-primary" onClick={() => window.location.reload()} style={{ marginTop: '20px' }}>Try Again</button>
        </div>
      </PageTransition>
    );
  }

  const riskLevelStr = data?.risk_level || data?.overall_risk_level || data?.summary?.risk_level || 'UNKNOWN';
  const riskLevel = typeof riskLevelStr === 'string' ? riskLevelStr.toUpperCase() : 'UNKNOWN';

  // Parse advice sections from raw text
  const parseAdviceSections = (adviceText, level) => {
    const sections = [];
    if (!adviceText) return sections;

    const source = String(adviceText)
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<[^>]*>/g, '')
      .replace(/&nbsp;/gi, ' ')
      .replace(/\r/g, '');

    // Extract main message (first paragraph before "What To Do")
    const mainMatch = source.match(/✨.*?(!|💪)/s);
    if (mainMatch) {
      let mainContent = mainMatch[0];
      let supportiveIntro = "";

      if (level === 'LOW') {
          supportiveIntro = "We deeply appreciate the time and honesty you put into this reflection. Your proactive approach to wellness is a beautiful baseline. Keep up these wonderful everyday maintenance habits.\n\n";
      } else if (level === 'MODERATE') {
          supportiveIntro = "Thank you for sharing your current state so openly. It takes courage to pause and check in. You are doing a great job navigating this, and carving out a little extra gentleness for yourself right now can make a world of difference.\n\n";
      } else if (level === 'HIGH') {
          supportiveIntro = "Thank you for your honesty and for trusting us with your feelings today. We see how much you are holding right now, and it is entirely okay that things feel heavy. Please be gentle with yourself. You do not have to carry this completely alone.\n\n";
      }
      
      sections.push({
        id: 'main',
        title: '✨ Main Guidance',
        content: supportiveIntro + mainContent,
        mood: 'encouraging'
      });
    }

    // Extract "What To Do Right Now"
    const actionMatch = source.match(/📋 \*\*What To Do Right Now:\*\*.*?(?=\n\n|🛠️|$)/s);
    if (actionMatch) {
      sections.push({
        id: 'actions',
        title: '📋 What To Do Right Now',
        content: actionMatch[0],
        mood: 'thinking'
      });
    }

    // Extract Coping Techniques
    const copingMatch = source.match(/🛠️ \*\*Personalized Coping Techniques:\*\*.*?(?=📞|💪|$)/s);
    if (copingMatch) {
      sections.push({
        id: 'coping',
        title: '🛠️ Coping Techniques',
        content: copingMatch[0],
        mood: 'comforting'
      });
    }

    // Extract Resources
    const resourceMatch = source.match(/📞 \*\*Resources & Support:\*\*.*?(?=💪|$)/s);
    if (resourceMatch) {
      sections.push({
        id: 'resources',
        title: '📞 Resources & Support',
        content: resourceMatch[0],
        mood: 'greeting'
      });
    }

    // Extract Wellness Habits
    const wellnessMatch = source.match(/💪 \*\*Daily Wellness Habits.*?\*\*.*$/s);
    if (wellnessMatch) {
      sections.push({
        id: 'wellness',
        title: '💪 Daily Wellness Habits',
        content: wellnessMatch[0],
        mood: 'celebration'
      });
    }

    return sections;
  };
  
  const rawScore = data?.final_score ?? data?.overall_risk_score ?? data?.summary?.overall_risk_score ?? 0;
  const finalScoreNum = Number(rawScore);
  const finalScore = (Number.isFinite(finalScoreNum) && !Number.isNaN(finalScoreNum)) ? Math.round(finalScoreNum) : 0;
  
  const adviceDisplay = data?.advice_display || data?.advice_text || data?.advice?.primary_message || '';
  const summary = data?.summary || {};
  
  // Presentation logic
  let mood = 'greeting';
  let badgeClass = 'risk-low';
  let heroMessage = '';

  if (riskLevel === 'LOW') {
    mood = 'celebration';
    badgeClass = 'risk-low';
    heroMessage = `You are doing wonderfully, ${userName}!`;
  } else if (riskLevel === 'MODERATE') {
    mood = 'encouraging';
    badgeClass = 'risk-moderate';
    heroMessage = `You are handling things well, ${userName}.`;
  } else if (riskLevel === 'HIGH') {
    mood = 'comforting';
    badgeClass = 'risk-high';
    heroMessage = `I hear you, ${userName}. It's okay to not be okay.`;
  } else {
    mood = 'greeting';
    badgeClass = 'risk-low';
    heroMessage = `Here are your insights, ${userName}.`;
  }

  // Fallback advice composition
  const fallbackAdvice = summary?.interpretation_summary || 
                         (Array.isArray(summary?.advice) ? summary.advice.join('\n\n') : null) || 
                         'No specific advice available, but please remember to nurture your well-being and take care of yourself. Reach out to loved ones or professionals if you ever need support.';

  const formattedAdvice = adviceDisplay ? (
    <div dangerouslySetInnerHTML={{ __html: adviceDisplay }} />
  ) : (
    <div>{fallbackAdvice}</div>
  );

  const adviceSections = parseAdviceSections(adviceDisplay || fallbackAdvice, riskLevel);
  const hasSections = adviceSections.length > 0;

  return (
    <PageTransition>
      <div style={{ maxWidth: '900px', width: '100%', padding: '0 1rem', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        
        {/* Top Hero Section */}
        <div className="results-hero animate-fade-in">
          <Mascot mood={mood} size={160} />
          <h1 className="results-hero-title">Wellness Dashboard</h1>
          <p className="results-hero-subtitle">{heroMessage}</p>
        </div>

        {/* Metric Cards Grid */}
        <div className="results-grid animate-fade-in" style={{ width: '100%', animationDelay: '0.1s' }}>
          
          {/* Score Card */}
          <div className="metric-card">
            <div className="metric-label">Final Score</div>
            <div className="metric-value-large">{finalScore}</div>
            <div style={{ marginTop: '1rem', color: 'var(--color-text-light)', fontSize: '0.9rem' }}>
               Cumulative score across all modules
            </div>
          </div>

          {/* Risk Level Card */}
          <div className="metric-card">
            <div className="metric-label">Assessed State</div>
            <div className={`risk-badge ${badgeClass}`}>
              {riskLevel === 'UNKNOWN' ? 'Not Available' : riskLevel}
            </div>
            <div style={{ marginTop: '1.25rem', color: 'var(--color-text-light)', fontSize: '0.9rem' }}>
               A generalized measure of your current wellness
            </div>
          </div>
        </div>

        {/* Advice Sections as CardSwap Display */}
        {hasSections ? (
          <div className="advice-sections animate-fade-in" style={{ width: '100%', animationDelay: '0.2s', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <h2 style={{ fontSize: '1.4rem', fontWeight: 600, marginBottom: '2rem', color: 'var(--color-text)', textAlign: 'center' }}>
              💙 Click the cards for your personalized guidance
            </h2>
            <div style={{ padding: '2rem 0 4rem 0', display: 'flex', justifyContent: 'center', width: '100%' }}>
              <CardSwap width={450} height={400} cardDistance={40} verticalDistance={40} skewAmount={4}>
                {adviceSections.map((section) => (
                  <Card key={section.id} className="card" style={{ padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
                    <div style={{ 
                      padding: '1.5rem', 
                      background: 'var(--color-lavender)', 
                      borderBottom: '1px solid rgba(0,0,0,0.05)',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '1rem'
                    }}>
                      <Mascot mood={section.mood} size={50} style={{ margin: 0 }} />
                      <h3 style={{ fontSize: '1.25rem', margin: 0, fontWeight: 600 }}>{section.title}</h3>
                    </div>
                    <div style={{ flex: 1, padding: '1.5rem', overflowY: 'auto' }}>
                      <p style={{ 
                        fontSize: '1.05rem',
                        lineHeight: '1.7',
                        color: 'black',
                        fontWeight: 'bold',
                        whiteSpace: 'pre-wrap',
                        margin: 0
                      }}>
                        {section.content.trim()}
                      </p>
                    </div>
                  </Card>
                ))}
              </CardSwap>
            </div>
          </div>
        ) : (
          <div className="advice-panel animate-fade-in" style={{ width: '100%', animationDelay: '0.2s' }}>
            <h2 className="advice-title">
              <Info size={24} style={{ color: 'var(--color-lavender-dark)' }} />
              Personalized Insights & Strategies
            </h2>
            <div className="advice-content">
              {formattedAdvice}
            </div>
          </div>
        )}

        {/* Secondary Action Buttons */}
        <div className="action-buttons-group animate-fade-in" style={{ width: '100%', animationDelay: '0.3s', marginBottom: '2rem' }}>
          <button className="btn-primary btn-icon" onClick={() => window.print()} style={{ minWidth: '220px' }}>
            <Download size={20} /> Download Report
          </button>
          <button className="btn-secondary btn-icon" onClick={() => alert('Sharing functionality coming soon!')} style={{ minWidth: '220px' }}>
            <Share2 size={20} /> Share for Consultation
          </button>
        </div>

        {/* Start Over Action */}
        <div style={{ textAlign: 'center', marginTop: '1rem', width: '100%' }}>
          <button 
            onClick={handleRestart} 
            style={{ 
              background: 'none', border: 'none', color: 'var(--color-text-light)', 
              textDecoration: 'underline', fontSize: '1rem', cursor: 'pointer',
              opacity: 0.7, transition: 'var(--transition)'
            }}
            onMouseOver={(e) => e.target.style.opacity = 1}
            onMouseOut={(e) => e.target.style.opacity = 0.7}
          >
            Start Over
          </button>
        </div>

      </div>
    </PageTransition>
  );
};

export default Results;
