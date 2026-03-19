"""
Stage 1: Psycholinguistic Risk Analysis System (PRAS)
Backend Module for Mental Health Assessment System
Version: 1.0.0
"""

import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from datetime import datetime
from collections import Counter

# Load models globally
try:
    nlp = spacy.load('en_core_web_sm')
    SPACY_MODEL_LOADED = True
except Exception as e:
    import warnings
    warnings.warn(f"spaCy model en_core_web_sm not available: {e}. Falling back to blank English model.", UserWarning)
    nlp = spacy.blank('en')
    SPACY_MODEL_LOADED = False

vader = SentimentIntensityAnalyzer()



# Optional Transformers / BERT support (lazy)
try:
    from transformers import pipeline as _hf_pipeline
    TRANSFORMERS_AVAILABLE = True
except Exception:
    _hf_pipeline = None
    TRANSFORMERS_AVAILABLE = False

# ==========================================
# DICTIONARY
# ==========================================

MENTAL_HEALTH_DICTIONARY = {
    'positive_emotion': [
        'happy', 'joy', 'love', 'excellent', 'good', 'great', 'wonderful',
        'fantastic', 'amazing', 'excited', 'pleased', 'delighted', 'glad',
        'cheerful', 'content', 'satisfied', 'optimistic', 'hopeful', 'enjoy',
        'better', 'best', 'beautiful', 'perfect', 'awesome', 'brilliant'
    ],
    
    'negative_emotion': [
        'sad', 'depressed', 'awful', 'terrible', 'horrible', 'unhappy',
        'miserable', 'upset', 'angry', 'frustrated', 'disappointed',
        'hurt', 'pain', 'suffering', 'agony', 'distress', 'worried',
        'bad', 'worse', 'worst', 'difficult', 'hard', 'struggle'
    ],
    
    'anxiety': [
        'worried', 'anxious', 'nervous', 'afraid', 'scared', 'fearful',
        'tense', 'stress', 'stressed', 'panic', 'overwhelmed', 'uneasy',
        'apprehensive', 'dread', 'terror', 'frantic', 'restless'
    ],
    
    'sadness': [
        'sad', 'cry', 'crying', 'tears', 'grief', 'sorrow', 'depressed',
        'hopeless', 'lonely', 'miserable', 'blue', 'down', 'gloomy',
        'despair', 'heartbroken', 'dejected', 'melancholy', 'empty'
    ],
    
    'anger': [
        'angry', 'hate', 'mad', 'furious', 'rage', 'annoyed', 'irritated',
        'frustrated', 'hostile', 'resentful', 'bitter', 'outraged',
        'livid', 'enraged', 'infuriated', 'aggravated'
    ],
    
    'absolutist': [
        'always', 'never', 'nothing', 'everything', 'everyone', 'nobody',
        'completely', 'totally', 'absolutely', 'entirely', 'fully',
        'utterly', 'wholly', 'all', 'none', 'every', 'no one', 'forever'
    ],
    
    'cognitive_distortion': [
        'should', 'must', 'have to', 'supposed to', 'ought', 'need to',
        'worthless', 'useless', 'failure', 'stupid', 'idiot', 'loser',
        'pathetic', 'inadequate', 'incompetent', "can't", "won't", "don't"
    ],
    
    'death': [
        'die', 'died', 'dead', 'death', 'kill', 'killed', 'suicide',
        'funeral', 'grave', 'coffin', 'bury', 'buried', 'corpse',
        'end', 'ending', 'final', 'gone'
    ],
    
    'self_harm': [
        'cut', 'cutting', 'hurt myself', 'harm myself', 'burn', 'burning',
        'wound', 'injure', 'damage myself', 'destroy myself'
    ],
    
    'social': [
        'friend', 'friends', 'family', 'people', 'together', 'group',
        'team', 'community', 'social', 'relationship', 'partner',
        'spouse', 'parent', 'sibling', 'colleague', 'neighbor', 'us', 'we'
    ],
    
    'isolation': [
        'alone', 'lonely', 'isolated', 'nobody', 'by myself', 'solitary',
        'abandoned', 'rejected', 'excluded', 'outcast', 'withdrawn', 'empty'
    ],
    
    'past_focus': [
        'was', 'were', 'had', 'did', 'ago', 'before', 'yesterday',
        'last', 'previous', 'former', 'earlier', 'used to', 'back then'
    ],
    
    'future_focus': [
        'will', 'gonna', 'going to', 'shall', 'soon', 'later', 'tomorrow',
        'next', 'future', 'plan', 'planning', 'hope', 'hoping', 'intend',
        'expect', 'looking forward', 'upcoming', 'ahead'
    ],
    
    'i_pronoun': [
        'i', "i'm", "i've", "i'll", "i'd", 'me', 'my', 'mine', 'myself'
    ],
    
    'we_pronoun': [
        'we', "we're", "we've", "we'll", "we'd", 'us', 'our', 'ours', 'ourselves'
    ],
    
    'hopelessness': [
        'hopeless', 'pointless', 'meaningless', 'useless', 'futile',
        'worthless', 'helpless', 'powerless', 'defeated', 'give up',
        'giving up', 'no point', 'no use', 'why bother', 'no way out'
    ],
    
    'positive_coping': [
        'try', 'trying', 'cope', 'coping', 'manage', 'managing', 'handle',
        'handling', 'deal', 'dealing', 'work through', 'overcome',
        'solve', 'improve', 'better', 'help', 'support'
    ]
}

# ==========================================
# QUESTIONS
# ==========================================

STAGE1_QUESTIONS = [
    {
        'id': 'q1',
        'question': 'How have you been feeling lately? Describe your mood over the past few weeks.',
        'focus': 'emotional_state',
        'weight': 1.2
    },
    {
        'id': 'q2',
        'question': 'Describe a typical day in your life, from when you wake up to when you go to bed.',
        'focus': 'behavioral_activation',
        'weight': 1.0
    },
    {
        'id': 'q3',
        'question': 'When you think about the next few months, what comes to mind? What are you hoping for or planning?',
        'focus': 'future_orientation',
        'weight': 1.3
    },
    {
        'id': 'q4',
        'question': 'Tell me about the important people in your life and how you feel around them.',
        'focus': 'social_connections',
        'weight': 1.1
    },
    {
        'id': 'q5',
        'question': 'How do you handle stress and challenges? What helps you cope, and what makes things harder?',
        'focus': 'coping_mechanisms',
        'weight': 1.0
    },
    {
        'id': 'q6',
        'question': 'How would you describe yourself to someone who doesn\'t know you?',
        'focus': 'self_perception',
        'weight': 1.0
    }
]

# ==========================================
# CORE FUNCTIONS
# ==========================================

def preprocess_text(text):
    """Clean and prepare text for analysis"""
    if not text or len(text.strip()) == 0:
        return "", []
    
    text_lower = text.lower()
    text_clean = ' '.join(text_lower.split())
    doc = nlp(text_clean)
    tokens = [token.text for token in doc if not token.is_space]
    
    return text_clean, tokens


def analyze_with_liwc(tokens, dictionary=MENTAL_HEALTH_DICTIONARY):
    """Analyze tokens using custom LIWC-style dictionary"""
    if not tokens or len(tokens) == 0:
        return {}
    
    total_words = len([t for t in tokens if t.isalpha()])
    
    if total_words == 0:
        return {}
    
    category_counts = {category: 0 for category in dictionary.keys()}
    
    for token in tokens:
        clean_token = re.sub(r'[^\w]', '', token.lower())
        
        if not clean_token:
            continue
        
        for category, word_list in dictionary.items():
            if clean_token in word_list:
                category_counts[category] += 1
            elif clean_token.replace("'", "") in [w.replace("'", "") for w in word_list]:
                category_counts[category] += 1
    
    category_percentages = {
        category: round((count / total_words * 100), 2)
        for category, count in category_counts.items()
    }
    
    category_percentages['word_count'] = total_words
    
    return category_percentages


def analyze_sentiment(text):
    """Analyze sentiment using VADER"""
    if not text or len(text.strip()) == 0:
        return {
            'compound': 0,
            'positive': 0,
            'negative': 0,
            'neutral': 100
        }
    
    scores = vader.polarity_scores(text)
    
    sentiment_results = {
        'compound': round(scores['compound'], 3),
        'positive': round(scores['pos'] * 100, 2),
        'negative': round(scores['neg'] * 100, 2),
        'neutral': round(scores['neu'] * 100, 2)
    }
    
    return sentiment_results


# ==========================================
# Lightweight BERT classifier wrapper
# ==========================================

class BertClassifier:
    """Minimal wrapper that lazily loads a Hugging Face sentiment pipeline.
    Uses a distilBERT sentiment model as a placeholder; can be customized
    by passing a different model name to `BertClassifier(model_name=...)`.
    If `transformers` is not installed, classifier reports unavailable.
    """
    def __init__(self, model_name=None):
        self.model_name = model_name or 'distilbert-base-uncased-finetuned-sst-2-english'
        self._pipe = None

    def _ensure_loaded(self):
        if not TRANSFORMERS_AVAILABLE:
            return
        if self._pipe is None:
            try:
                self._pipe = _hf_pipeline('sentiment-analysis', model=self.model_name, tokenizer=self.model_name)
            except Exception:
                # Fallback to default pipeline if custom model download fails
                self._pipe = _hf_pipeline('sentiment-analysis')

    def predict(self, text):
        """Return a small dict: {'available': bool, 'label': str, 'score': float} or {'available': False}.
        """
        if not TRANSFORMERS_AVAILABLE:
            return {'available': False}

        try:
            self._ensure_loaded()
            if not self._pipe:
                return {'available': False}

            # Truncate long text to keep inference fast
            snippet = text if len(text) <= 1000 else text[:1000]
            out = self._pipe(snippet)
            if isinstance(out, list) and len(out) > 0:
                return {'available': True, 'label': out[0].get('label'), 'score': float(out[0].get('score', 0.0))}
            return {'available': True, 'error': 'empty_output'}
        except Exception as e:
            return {'available': False, 'error': str(e)}


# Global classifier instance (lazy)
bert_classifier = BertClassifier()


def analyze_pronouns(tokens, dictionary=MENTAL_HEALTH_DICTIONARY):
    """Analyze pronoun usage patterns"""
    if not tokens or len(tokens) == 0:
        return {
            'i_count': 0,
            'i_percentage': 0,
            'we_count': 0,
            'we_percentage': 0,
            'ratio': 0
        }
    
    total_words = len([t for t in tokens if t.isalpha()])
    
    if total_words == 0:
        return {
            'i_count': 0,
            'i_percentage': 0,
            'we_count': 0,
            'we_percentage': 0,
            'ratio': 0
        }
    
    i_pronouns_extended = [
        'i', 'me', 'my', 'mine', 'myself',
        "i'm", "i've", "i'll", "i'd",
        'im', 'ive', 'ill', 'id'
    ]
    
    we_pronouns_extended = [
        'we', 'us', 'our', 'ours', 'ourselves',
        "we're", "we've", "we'll", "we'd",
        'were', 'weve', 'well', 'wed'
    ]
    
    i_count = 0
    for token in tokens:
        clean_token = token.lower().strip("'\".,!?;:")
        if clean_token in i_pronouns_extended:
            i_count += 1
    
    we_count = 0
    for token in tokens:
        clean_token = token.lower().strip("'\".,!?;:")
        if clean_token in we_pronouns_extended:
            we_count += 1
    
    i_percentage = round((i_count / total_words * 100), 2)
    we_percentage = round((we_count / total_words * 100), 2)
    ratio = round(i_percentage / (we_percentage + 1), 2)
    
    return {
        'i_count': i_count,
        'i_percentage': i_percentage,
        'we_count': we_count,
        'we_percentage': we_percentage,
        'ratio': ratio
    }


def analyze_temporal_focus(tokens, text, dictionary=MENTAL_HEALTH_DICTIONARY):
    """Analyze past, present, future orientation with context awareness"""
    if not tokens or len(tokens) == 0:
        return {
            'past_count': 0,
            'future_count': 0,
            'positive_future_count': 0,
            'negative_future_count': 0,
            'has_future_orientation': False,
            'has_negative_future': False,
            'temporal_ratio': 0
        }
    
    text_lower = text.lower()
    
    past_count = sum(1 for token in tokens if token in dictionary['past_focus'])
    future_words_found = [token for token in tokens if token in dictionary['future_focus']]
    future_count = len(future_words_found)
    
    negative_future_phrases = [
        "can't see any future", "cannot see any future", "no future",
        "don't see a future", "don't have a future",
        "nothing to look forward", "nothing to hope for",
        "stopped making plans", "stopped planning", "gave up planning",
        "won't get better", "will never change", "will always be",
        "no point in planning", "why plan", "pointless to plan"
    ]
    
    positive_future_phrases = [
        "looking forward", "excited about", "can't wait",
        "planning to", "going to", "will be", "hope to",
        "expect to", "aiming to", "working toward"
    ]
    
    negative_future_detected = any(phrase in text_lower for phrase in negative_future_phrases)
    positive_future_detected = any(phrase in text_lower for phrase in positive_future_phrases)
    
    positive_future_count = sum(1 for phrase in positive_future_phrases if phrase in text_lower)
    negative_future_count = sum(1 for phrase in negative_future_phrases if phrase in text_lower)
    
    has_positive_future = (
        future_count > 0 and 
        (positive_future_detected or not negative_future_detected)
    )
    
    temporal_ratio = round(future_count / (past_count + 1), 2)
    
    return {
        'past_count': past_count,
        'future_count': future_count,
        'positive_future_count': positive_future_count,
        'negative_future_count': negative_future_count,
        'has_future_orientation': has_positive_future,
        'has_negative_future': negative_future_detected,
        'temporal_ratio': temporal_ratio
    }


def detect_red_flags(text, tokens, liwc_results):
    """Detect critical warning signs for immediate intervention"""
    red_flags = []
    text_lower = text.lower()
    
    # CRITICAL: Suicidal ideation
    suicide_keywords = [
        'kill myself', 'killing myself', 'killed myself',
        'end it all', 'end my life', 'ending my life',
        'suicide', 'suicidal', 'commit suicide',
        'want to die', 'wanting to die', 'wanna die',
        'wish i was dead', 'wish i were dead',
        'better off dead', "better off if i was dead",
        'no reason to live', 'nothing to live for',
        "can't go on", "cannot go on", "can not go on",
        'rather be dead', "rather die",
        'take my own life', 'taking my own life',
        'end everything', 'ending everything',
        "don't want to be here", "don't want to exist",
        "no point in living"
    ]
    
    for keyword in suicide_keywords:
        if keyword in text_lower:
            red_flags.append({
                'severity': 'CRITICAL',
                'type': 'suicidal_ideation',
                'trigger': keyword,
                'message': f'Explicit suicidal language detected: "{keyword}"'
            })
            break
    
    # CRITICAL: Death wishes
    death_wish_keywords = [
        "wish i was dead", "wish i were dead", "wish i could die",
        "hope i die", "hoping to die", "want death", "wish for death"
    ]
    
    for keyword in death_wish_keywords:
        if keyword in text_lower and not any(f['type'] == 'suicidal_ideation' for f in red_flags):
            red_flags.append({
                'severity': 'CRITICAL',
                'type': 'death_ideation',
                'trigger': keyword,
                'message': f'Death wish expressed: "{keyword}"'
            })
            break
    
    # CRITICAL: Severe Hopelessness
    hopeless_pct = liwc_results.get('hopelessness', 0)
    if hopeless_pct >= 8:
        red_flags.append({
            'severity': 'CRITICAL',
            'type': 'severe_hopelessness',
            'trigger': f'{hopeless_pct}% hopelessness words',
            'message': f'Severe hopelessness detected ({hopeless_pct}%) - major suicide risk factor'
        })
    
    # CRITICAL: Hopelessness + no future
    future_count = sum(1 for token in tokens if token in MENTAL_HEALTH_DICTIONARY['future_focus'])
    word_count = liwc_results.get('word_count', 0)
    
    if hopeless_pct >= 5 and future_count == 0 and word_count > 30:
        if not any(f['type'] == 'severe_hopelessness' for f in red_flags):
            red_flags.append({
                'severity': 'CRITICAL',
                'type': 'hopelessness_with_no_future',
                'trigger': f'{hopeless_pct}% hopelessness + zero future orientation',
                'message': 'Unable to envision future combined with severe hopelessness - extreme risk'
            })
    
    # WARNING: Moderate hopelessness
    if 5 <= hopeless_pct < 8:
        red_flags.append({
            'severity': 'WARNING',
            'type': 'moderate_hopelessness',
            'trigger': f'{hopeless_pct}% hopelessness words',
            'message': f'Elevated hopelessness language ({hopeless_pct}%) - monitor closely'
        })
    
    # WARNING: Self-harm
    self_harm_phrases = [
        'cut myself', 'cutting myself', 'cut themselves',
        'hurt myself', 'hurting myself', 
        'harm myself', 'harming myself',
        'burn myself', 'burning myself',
        'self harm', 'self-harm', 'injure myself'
    ]
    
    for phrase in self_harm_phrases:
        if phrase in text_lower:
            red_flags.append({
                'severity': 'WARNING',
                'type': 'self_harm',
                'trigger': phrase,
                'message': f'Self-harm mention: "{phrase}"'
            })
            break
    
    # WARNING: Death preoccupation
    death_pct = liwc_results.get('death', 0)
    if death_pct >= 4:
        red_flags.append({
            'severity': 'WARNING',
            'type': 'death_preoccupation',
            'trigger': f'{death_pct}% death references',
            'message': f'Preoccupation with death themes ({death_pct}%)'
        })
    
    # WARNING: Cognitive rigidity
    absolutist_pct = liwc_results.get('absolutist', 0)
    if absolutist_pct >= 12:
        red_flags.append({
            'severity': 'WARNING',
            'type': 'cognitive_rigidity',
            'trigger': f'{absolutist_pct}% absolutist words',
            'message': f'Extreme all-or-nothing thinking ({absolutist_pct}%)'
        })
    
    # WARNING: Social isolation
    social_pct = liwc_results.get('social', 0)
    isolation_pct = liwc_results.get('isolation', 0)
    
    if social_pct == 0 and word_count > 40 and isolation_pct > 0:
        red_flags.append({
            'severity': 'WARNING',
            'type': 'severe_isolation',
            'trigger': 'No social references + isolation language',
            'message': 'Complete social disconnection with active isolation themes'
        })
    
    # WARNING: Emotional depletion
    neg_emotion_pct = liwc_results.get('negative_emotion', 0)
    pos_emotion_pct = liwc_results.get('positive_emotion', 0)
    
    if neg_emotion_pct > 15 and pos_emotion_pct == 0 and word_count > 30:
        red_flags.append({
            'severity': 'WARNING',
            'type': 'emotional_depletion',
            'trigger': f'{neg_emotion_pct}% negative, 0% positive emotion',
            'message': 'Complete absence of positive emotion with high negativity'
        })
    
    return red_flags


def calculate_response_risk_score(analysis):
    """Calculate 0-100 risk score for a single response"""
    score = 0
    
    liwc = analysis.get('liwc', {})
    sentiment = analysis.get('sentiment', {})
    pronouns = analysis.get('pronouns', {})
    temporal = analysis.get('temporal', {})
    red_flags = analysis.get('red_flags', [])
    
    # Component 1: Emotion Ratio (0-25 points)
    pos_emotion = liwc.get('positive_emotion', 0)
    neg_emotion = liwc.get('negative_emotion', 0)
    emotion_ratio = (pos_emotion + 1) / (neg_emotion + 1)
    
    if emotion_ratio < 0.2:
        score += 25
    elif emotion_ratio < 0.5:
        score += 18
    elif emotion_ratio < 1.0:
        score += 10
    elif emotion_ratio < 2.0:
        score += 3
    
    # Component 2: Negative Emotion (0-15 points)
    if neg_emotion > 20:
        score += 15
    elif neg_emotion > 15:
        score += 12
    elif neg_emotion > 10:
        score += 8
    elif neg_emotion > 5:
        score += 4
    
    # Component 3: I-Pronoun Rumination (0-15 points)
    i_pct = pronouns.get('i_percentage', 0)
    if i_pct > 15:
        score += 15
    elif i_pct > 12:
        score += 12
    elif i_pct > 9:
        score += 8
    elif i_pct > 6:
        score += 4
    
    # Component 4: Social Isolation (0-15 points)
    social_words = liwc.get('social', 0)
    isolation_words = liwc.get('isolation', 0)
    social_score = isolation_words - social_words
    
    if social_score > 5:
        score += 15
    elif social_score > 3:
        score += 12
    elif social_score > 1:
        score += 8
    elif social_score > 0:
        score += 4
    
    # Component 5: Future Orientation (0-20 points)
    has_future = temporal.get('has_future_orientation', False)
    has_negative_future = temporal.get('has_negative_future', False)
    
    if has_negative_future:
        score += 20
    elif not has_future:
        score += 15
    elif temporal.get('future_count', 0) < 2:
        score += 8
    
    # Component 6: Hopelessness (0-15 points)
    hopelessness = liwc.get('hopelessness', 0)
    if hopelessness > 10:
        score += 15
    elif hopelessness > 7:
        score += 12
    elif hopelessness > 5:
        score += 8
    elif hopelessness > 2:
        score += 4
    
    # Component 7: Absolutist Thinking (0-10 points)
    absolutist = liwc.get('absolutist', 0)
    if absolutist > 15:
        score += 10
    elif absolutist > 10:
        score += 7
    elif absolutist > 5:
        score += 4
    
    # Component 8: Death References (0-10 points)
    death_refs = liwc.get('death', 0)
    if death_refs > 5:
        score += 10
    elif death_refs > 3:
        score += 7
    elif death_refs > 1:
        score += 4
    
    # Component 9: Sentiment Compound (0-10 points)
    compound = sentiment.get('compound', 0)
    if compound < -0.5:
        score += 10
    elif compound < -0.3:
        score += 7
    elif compound < -0.1:
        score += 4
    
    # Component 10: Red Flags Override
    critical_count = sum(1 for f in red_flags if f['severity'] == 'CRITICAL')
    warning_count = sum(1 for f in red_flags if f['severity'] == 'WARNING')
    
    score += critical_count * 30
    score += warning_count * 10
    
    return min(round(score, 1), 100)


def categorize_risk(score):
    """Categorize risk level based on score"""
    if score < 33:
        return 'LOW'
    elif score < 67:
        return 'MODERATE'
    else:
        return 'HIGH'


def analyze_single_response(question_id, question_text, response_text):
    """Complete analysis pipeline for a single question response"""
    analysis = {
        'question_id': question_id,
        'question': question_text,
        'response': response_text,
        'timestamp': datetime.now().isoformat(),
        'valid': True,
        'errors': []
    }
    
    if not response_text or len(response_text.strip()) == 0:
        analysis['valid'] = False
        analysis['errors'].append('Empty response')
        return analysis
    
    word_count_check = len(response_text.split())
    if word_count_check < 10:
        analysis['valid'] = False
        analysis['errors'].append(f'Response too short ({word_count_check} words, minimum 10 required)')
        return analysis
    
    try:
        clean_text, tokens = preprocess_text(response_text)
        analysis['preprocessed'] = {
            'clean_text': clean_text,
            'token_count': len(tokens)
        }
    except Exception as e:
        analysis['valid'] = False
        analysis['errors'].append(f'Preprocessing error: {str(e)}')
        return analysis
    
    try:
        liwc_results = analyze_with_liwc(tokens)
        analysis['liwc'] = liwc_results
    except Exception as e:
        analysis['errors'].append(f'LIWC analysis error: {str(e)}')
        analysis['liwc'] = {}
    
    try:
        sentiment_results = analyze_sentiment(response_text)
        analysis['sentiment'] = sentiment_results
    except Exception as e:
        analysis['errors'].append(f'Sentiment analysis error: {str(e)}')
        analysis['sentiment'] = {}

    # Optional BERT-based classification (adds `bert` to analysis)
    try:
        try:
            bert_results = bert_classifier.predict(response_text)
        except Exception as _e:
            bert_results = {'available': False, 'error': str(_e)}
        analysis['bert'] = bert_results
    except Exception as e:
        analysis['errors'].append(f'BERT analysis error: {str(e)}')
        analysis['bert'] = {'available': False}
    
    try:
        pronoun_results = analyze_pronouns(tokens)
        analysis['pronouns'] = pronoun_results
    except Exception as e:
        analysis['errors'].append(f'Pronoun analysis error: {str(e)}')
        analysis['pronouns'] = {}
    
    try:
        temporal_results = analyze_temporal_focus(tokens, response_text)
        analysis['temporal'] = temporal_results
    except Exception as e:
        analysis['errors'].append(f'Temporal analysis error: {str(e)}')
        analysis['temporal'] = {}
    
    try:
        red_flags = detect_red_flags(response_text, tokens, liwc_results)
        analysis['red_flags'] = red_flags
        analysis['critical_flags_count'] = sum(1 for f in red_flags if f['severity'] == 'CRITICAL')
        analysis['warning_flags_count'] = sum(1 for f in red_flags if f['severity'] == 'WARNING')
    except Exception as e:
        analysis['errors'].append(f'Red flag detection error: {str(e)}')
        analysis['red_flags'] = []
        analysis['critical_flags_count'] = 0
        analysis['warning_flags_count'] = 0
    
    try:
        risk_score = calculate_response_risk_score(analysis)
        analysis['risk_score'] = risk_score
        analysis['risk_level'] = categorize_risk(risk_score)
    except Exception as e:
        analysis['errors'].append(f'Risk scoring error: {str(e)}')
        analysis['risk_score'] = 0
        analysis['risk_level'] = 'UNKNOWN'
    
    return analysis


def calculate_aggregated_metrics(individual_analyses):
    """Calculate average metrics across all valid responses"""
    valid_analyses = [a for a in individual_analyses.values() if a['valid']]
    
    if not valid_analyses:
        return {}
    
    liwc_aggregated = {}
    liwc_categories = valid_analyses[0]['liwc'].keys()
    
    for category in liwc_categories:
        values = [a['liwc'].get(category, 0) for a in valid_analyses]
        liwc_aggregated[category] = round(sum(values) / len(values), 2)
    
    sentiment_aggregated = {
        'compound': round(sum(a['sentiment'].get('compound', 0) for a in valid_analyses) / len(valid_analyses), 3),
        'positive': round(sum(a['sentiment'].get('positive', 0) for a in valid_analyses) / len(valid_analyses), 2),
        'negative': round(sum(a['sentiment'].get('negative', 0) for a in valid_analyses) / len(valid_analyses), 2),
        'neutral': round(sum(a['sentiment'].get('neutral', 0) for a in valid_analyses) / len(valid_analyses), 2)
    }
    
    pronouns_aggregated = {
        'i_percentage': round(sum(a['pronouns'].get('i_percentage', 0) for a in valid_analyses) / len(valid_analyses), 2),
        'we_percentage': round(sum(a['pronouns'].get('we_percentage', 0) for a in valid_analyses) / len(valid_analyses), 2),
        'ratio': round(sum(a['pronouns'].get('ratio', 0) for a in valid_analyses) / len(valid_analyses), 2)
    }
    
    future_count = sum(1 for a in valid_analyses if a['temporal'].get('has_future_orientation', False))
    temporal_aggregated = {
        'responses_with_future': future_count,
        'percentage_with_future': round((future_count / len(valid_analyses) * 100), 2)
    }
    
    return {
        'liwc': liwc_aggregated,
        'sentiment': sentiment_aggregated,
        'pronouns': pronouns_aggregated,
        'temporal': temporal_aggregated,
        'total_responses': len(valid_analyses)
    }


def calculate_weighted_overall_score(individual_analyses):
    """Calculate weighted average risk score across all questions"""
    valid_analyses = [a for a in individual_analyses.values() if a['valid']]
    
    if not valid_analyses:
        return 0
    
    total_weight = sum(a['weight'] for a in valid_analyses)
    weighted_sum = sum(a['risk_score'] * a['weight'] for a in valid_analyses)
    
    overall_score = round(weighted_sum / total_weight, 1)
    
    return overall_score


def calculate_confidence(stage1_results):
    """Calculate confidence in the assessment"""
    total_questions = len(STAGE1_QUESTIONS)
    valid_responses = stage1_results['valid_responses']
    
    completion_rate = valid_responses / total_questions
    
    if completion_rate == 1.0:
        confidence = 'HIGH'
    elif completion_rate >= 0.8:
        confidence = 'MODERATE'
    else:
        confidence = 'LOW'
    
    return confidence


def analyze_all_stage1_responses(user_responses):
    """Analyze all 6 Stage 1 question responses"""
    
    stage1_results = {
        'timestamp': datetime.now().isoformat(),
        'questions_analyzed': 0,
        'valid_responses': 0,
        'invalid_responses': 0,
        'individual_analyses': {},
        'aggregated_metrics': {},
        'red_flags_summary': {
            'total_critical': 0,
            'total_warning': 0,
            'all_flags': []
        },
        'overall_risk_score': 0,
        'overall_risk_level': 'UNKNOWN',
        'crisis_detected': False,
        'stage1_signal': {}
    }
    
    for question_data in STAGE1_QUESTIONS:
        q_id = question_data['id']
        q_text = question_data['question']
        q_weight = question_data.get('weight', 1.0)
        
        response_text = user_responses.get(q_id, '')
        
        analysis = analyze_single_response(q_id, q_text, response_text)
        analysis['weight'] = q_weight
        
        stage1_results['individual_analyses'][q_id] = analysis
        stage1_results['questions_analyzed'] += 1
        
        if analysis['valid']:
            stage1_results['valid_responses'] += 1
            
            if analysis['red_flags']:
                stage1_results['red_flags_summary']['total_critical'] += analysis['critical_flags_count']
                stage1_results['red_flags_summary']['total_warning'] += analysis['warning_flags_count']
                stage1_results['red_flags_summary']['all_flags'].extend([
                    {**flag, 'question_id': q_id} for flag in analysis['red_flags']
                ])
                
                if analysis['critical_flags_count'] > 0:
                    stage1_results['crisis_detected'] = True
        else:
            stage1_results['invalid_responses'] += 1
    
    stage1_results['aggregated_metrics'] = calculate_aggregated_metrics(
        stage1_results['individual_analyses']
    )
    
    stage1_results['overall_risk_score'] = calculate_weighted_overall_score(
        stage1_results['individual_analyses']
    )
    
    stage1_results['overall_risk_level'] = categorize_risk(
        stage1_results['overall_risk_score']
    )
    
    stage1_results['stage1_signal'] = {
        'score': stage1_results['overall_risk_score'],
        'level': stage1_results['overall_risk_level'],
        'crisis_detected': stage1_results['crisis_detected'],
        'critical_flags': stage1_results['red_flags_summary']['total_critical'],
        'warning_flags': stage1_results['red_flags_summary']['total_warning'],
        'valid_responses': stage1_results['valid_responses'],
        'confidence': calculate_confidence(stage1_results)
    }
    
    return stage1_results


# ==========================================
# API-READY FUNCTIONS
# ==========================================

# ==========================================
# ADVICE ENGINE (EMOJI-ENHANCED)
# ==========================================

ADVICE_ENGINE = {
    
    # Risk Level Advice (Primary)
    'risk_level': {
        'LOW': {
            'message': '✨ Great news! Your responses suggest you are managing well overall. Keep up the good work! 💪',
            'advice': [
                '🌱 Continue engaging in activities that bring you fulfillment and joy',
                '👥 Maintain your social connections and support network',
                '💆 Practice regular self-care (sleep, nutrition, exercise)',
                '📝 Consider keeping a gratitude journal to reinforce positive patterns',
                '🎨 Set aside time for hobbies and interests you enjoy',
                '🧘 Keep nurturing your mental wellness with mindfulness practices'
            ],
            'resources': [
                '📱 Wellness apps: Headspace, Calm, Insight Timer',
                '📋 Self-care planning tools',
                '📚 Positive psychology resources',
                '🎧 Meditation and relaxation podcasts'
            ]
        },
        
        'MODERATE': {
            'message': '⚠️ Your responses indicate you may be experiencing some challenges. Additional support could be helpful. You don\'t have to manage this alone! 🤝',
            'advice': [
                '👨‍⚕️ Consider scheduling an appointment with a counselor or therapist',
                '💬 Talk to someone you trust about what you\'re experiencing',
                '🛠️ Practice structured coping techniques daily (see below)',
                '📊 Monitor your symptoms - keep a mood journal',
                '😴 Prioritize sleep hygiene and regular physical activity',
                '🚫 Limit alcohol and avoid substance use as coping mechanisms',
                '📅 Create a daily routine with small, achievable goals'
            ],
            'resources': [
                '🔍 Find a therapist: PsychologyToday.com, BetterHelp, Talkspace',
                '💼 Employee Assistance Program (EAP) if available through work',
                '🏥 Community mental health centers',
                '💻 Online support groups and communities',
                '📞 Mental health warmlines for non-crisis support'
            ]
        },
        
        'HIGH': {
            'message': '🔴 Your responses suggest you may be experiencing significant distress. Professional support is strongly recommended. Please know that help is available and you deserve support. 💙',
            'advice': [
                '🚨 PRIORITY: Contact a mental health professional within 24-48 hours',
                '🤝 Reach out to a trusted friend or family member today - don\'t isolate',
                '☎️ If you have suicidal thoughts, call a crisis hotline immediately',
                '🔒 Remove any means of self-harm from your environment',
                '📋 Create a safety plan with specific contacts and coping strategies',
                '👥 Avoid being alone for extended periods',
                '⏸️ Do NOT make major life decisions while in crisis',
                '💊 Continue any prescribed medications - consult doctor before changes'
            ],
            'resources': [
                '🆘 **CRISIS: National Suicide Prevention Lifeline: 988** (24/7, free)',
                '📱 **Crisis Text Line: Text HOME to 741741**',
                '🚑 **Emergency: Call 911 or go to nearest ER**',
                '🇺🇸 SAMHSA National Helpline: 1-800-662-4357 (24/7)',
                '🎖️ Veterans Crisis Line: 1-800-273-8255, Press 1',
                '🏥 Local crisis intervention centers',
                '👨‍⚕️ Your primary care doctor (emergency appointment)'
            ]
        }
    },
    
    # Category-Specific Advice (Secondary)
    'categories': {
        
        'negative_emotion': {
            'title': '😔 Managing Negative Emotions',
            'intro': 'Feeling down is part of being human. Here are some ways to work through difficult emotions:',
            'techniques': [
                '🏷️ **Naming emotions**: Say "I feel [emotion]" rather than "I am [emotion]" - you are not your feelings',
                '⏸️ **STOP technique**: Stop, Take a breath, Observe what\'s happening, Proceed mindfully',
                '🚶 **Physical release**: Take a walk, do jumping jacks, stretch, or dance it out',
                '🎯 **Healthy distraction**: Puzzle, cooking, art, cleaning - engage your focus',
                '💚 **Self-compassion**: Speak to yourself as you would to a dear friend',
                '📞 **Reach out**: Share with someone who cares - connection heals'
            ]
        },
        
        'anxiety': {
            'title': '😰 Anxiety Management Techniques',
            'intro': 'Anxiety is uncomfortable but manageable. These tools can help calm your nervous system:',
            'techniques': [
                '🌬️ **4-7-8 Breathing**: Inhale 4 sec, hold 7 sec, exhale 8 sec - repeat 4 times',
                '🔢 **5-4-3-2-1 Grounding**: Name 5 things you see, 4 you hear, 3 you feel, 2 you smell, 1 you taste',
                '💪 **Progressive muscle relaxation**: Tense each muscle group 5 sec, then release',
                '🤔 **Thought challenging**: "What evidence supports this worry? What doesn\'t?"',
                '⏰ **Scheduled worry time**: Dedicate 15 min daily for worries, then mentally close the door',
                '📱 **Grounding apps**: Try Rootd, MindShift, or Dare for in-the-moment support',
                '🧘 **Body scan meditation**: Notice tension without judgment, breathe into tight areas'
            ]
        },
        
        'hopelessness': {
            'title': '🌧️ Building Hope and Future Perspective',
            'intro': 'When hope feels distant, start with the smallest step forward. Progress isn\'t always visible immediately.',
            'techniques': [
                '🎯 **Micro-goals**: Focus on one achievable task today - brush teeth, drink water, step outside',
                '🏆 **Past victories**: List 3 challenges you\'ve overcome before - you\'re stronger than you think',
                '📅 **Small anticipation**: Identify ONE small thing to look forward to this week',
                '🎬 **Behavioral activation**: Do one activity you used to enjoy, even without motivation',
                '💎 **Values connection**: What matters most? Take one tiny action aligned with that value',
                '🌱 **Plant seeds**: Do something today your future self will thank you for',
                '🌅 **Morning routine**: Create one pleasant morning ritual to start days with intention'
            ],
            'warning': '⚠️ Severe hopelessness is a significant risk factor. Please reach out for professional help - you deserve support. 💙'
        },
        
        'cognitive_distortion': {
            'title': '🧠 Challenging Distorted Thinking',
            'intro': 'Our minds sometimes play tricks on us. Here\'s how to think more flexibly:',
            'techniques': [
                '⚖️ **All-or-nothing**: Replace "always/never" with "sometimes" - what\'s the gray area?',
                '🔄 **Should statements**: Replace "I should" with "I would prefer" or "It would be helpful if"',
                '🏷️ **Anti-labeling**: "I made a mistake" ≠ "I am a failure" - you are more than one moment',
                '🔍 **Evidence court**: What facts support this? What contradicts it? What would a friend say?',
                '🎨 **Reframing magic**: "This is challenging" instead of "This is impossible"',
                '📝 **Thought records**: Write the thought, rate belief 0-100, find alternatives, re-rate',
                '🤝 **Friend perspective**: Would you say this to someone you care about? Probably not!'
            ]
        },
        
        'isolation': {
            'title': '🤗 Rebuilding Social Connection',
            'intro': 'Reconnecting can feel scary, but humans need connection. Start small and be patient with yourself:',
            'techniques': [
                '💬 **Micro-connection**: Send a text, meme, or emoji to one person today',
                '💻 **Online communities**: Join Reddit, Discord, or forums about your interests - low pressure',
                '📅 **Weekly ritual**: Schedule ONE social activity per week (coffee, walk, video call)',
                '🤝 **Reciprocal outreach**: Reach out to others who might also feel lonely - you\'re not alone',
                '🎯 **Group activities**: Join a class, club, book group, or volunteer - shared purpose helps',
                '🐕 **Pet connections**: Volunteer at animal shelter - animals are non-judgmental connection',
                '☕ **Parallel play**: Work in a coffee shop, library - being around people counts',
                '🎮 **Gaming communities**: Online games with voice chat can ease back into socializing'
            ]
        },
        
        'low_self_worth': {
            'title': '💪 Building Self-Compassion & Worth',
            'intro': 'You are worthy simply because you exist. Let\'s work on believing that:',
            'techniques': [
                '✨ **Daily wins journal**: Write 3 things you did well each day, no matter how tiny',
                '🌟 **Strengths inventory**: List 5 strengths or positive qualities - ask a friend to help',
                '🫂 **Self-compassion break**: "This is hard. Others struggle too. May I be kind to myself."',
                '🗣️ **Inner critic challenge**: Would you say this to a friend? If not, don\'t say it to yourself',
                '🎯 **Values-based living**: Define what matters to you, take actions aligned with those values',
                '📸 **Evidence collection**: Take photos of accomplishments, kind notes, achievements',
                '🏆 **Past successes**: Create a "win jar" - add notes about things you\'re proud of',
                '💌 **Future self letter**: Write to yourself with compassion - read it when struggling'
            ]
        },
        
        'no_future_orientation': {
            'title': '🔮 Cultivating Future Perspective',
            'intro': 'When the future feels blank or scary, focus on the very next small step:',
            'techniques': [
                '📅 **Tomorrow only**: Don\'t plan the year - just plan tomorrow\'s one nice thing',
                '🎉 **Micro-anticipation**: Schedule ONE enjoyable activity this week (movie, meal, walk)',
                '✍️ **Future self letter**: Write to yourself 6 months from now - what do you hope for?',
                '🧩 **Goal decomposition**: Break big goals into the tiniest possible next step',
                '🌅 **Daily anchor**: Identify one small thing to look forward to each morning',
                '📖 **Story continuation**: "And then what happened?" - practice envisioning next chapters',
                '🎁 **Future gifts**: Do something today that future you will appreciate'
            ],
            'warning': '⚠️ Loss of future perspective is associated with increased risk. Please consider professional evaluation. 💙'
        },
        
        'high_rumination': {
            'title': '🔄 Breaking Rumination Cycles',
            'intro': 'Rumination is like a mental hamster wheel. Here\'s how to step off:',
            'techniques': [
                '⏱️ **Time-boxing**: Allow 15 min of focused thinking, then actively shift attention',
                '🎯 **Distraction menu**: Keep list of engaging activities that require focus (puzzles, crafts, games)',
                '🧘 **Mindful noticing**: "I\'m having the thought that..." - observe without engaging',
                '📝 **Problem-solving mode**: If it\'s solvable, write 3 action steps. If not, practice acceptance.',
                '🚶 **Physical interrupt**: Stand, move to different room, do 10 jumping jacks',
                '🎵 **Music shift**: Change your mental channel with upbeat or calming music',
                '🤝 **Talk it out**: Sometimes verbalizing breaks the loop - call a friend or hotline',
                '📵 **Screen break**: Rumination often worsens with passive scrolling - engage actively instead'
            ]
        },
        
        'behavioral_shutdown': {
            'title': '🔋 Behavioral Activation Strategies',
            'intro': 'When everything feels too hard, start impossibly small. Momentum builds on itself:',
            'techniques': [
                '🪥 **Microscopic start**: Can\'t shower? Just brush teeth. Can\'t exercise? Just stand up.',
                '✅ **One win daily**: Complete ONE small task, then celebrate it genuinely',
                '⏰ **Time anchors**: Set 2-3 daily routines (wake time, one meal, one activity)',
                '⏱️ **5-minute rule**: Commit to 5 min of any activity - movement creates momentum',
                '🤝 **Accountability buddy**: Tell one person your daily micro-goal, check in',
                '🎯 **Task ladder**: Rate tasks 1-10 difficulty, start with 1-2 level tasks',
                '🏆 **Reward immediately**: After task, do something pleasant right away (music, snack, rest)',
                '📱 **Activation apps**: Try Habitica, Streaks, or Forest to gamify basic tasks'
            ]
        },
        
        'suicidal_ideation': {
            'title': '🆘 Immediate Safety Strategies',
            'intro': '🚨 **If you\'re having thoughts of suicide, please reach out for help right now.** You deserve to live and feel better.',
            'techniques': [
                '☎️ **Call 988** (Suicide & Crisis Lifeline) - 24/7, free, confidential',
                '📱 **Text HOME to 741741** - Crisis Text Line for text-based support',
                '🤝 **Tell someone NOW** - Friend, family, therapist, doctor, anyone safe',
                '🔒 **Safety plan**: Remove access to means, create list of reasons to live',
                '🏥 **Go to ER** if you have a plan or can\'t stay safe',
                '⏸️ **Delay action**: Promise yourself to wait 24 hours - feelings change',
                '🧊 **Sensory grounding**: Hold ice, take cold shower, splash face - interrupt the crisis',
                '📝 **Reasons to live**: Write even small reasons - your pet, unfinished book, someone who cares'
            ],
            'warning': '🚨 **This is a mental health emergency. Please get help immediately. You are not a burden. You matter.** 💙'
        }
    },
    
    # Crisis Resources
    'crisis_resources': {
        'immediate_danger': [
            '🆘 **Call 988** - National Suicide Prevention Lifeline (24/7, free, confidential)',
            '📱 **Text HOME to 741741** - Crisis Text Line',
            '🚑 **Call 911** or go to nearest Emergency Room',
            '🎖️ **Veterans: 1-800-273-8255, Press 1** - Veterans Crisis Line',
            '🇺🇸 **1-800-662-4357** - SAMHSA Mental Health/Substance Abuse Helpline (24/7)',
            '🌈 **Trevor Project: 1-866-488-7386** - LGBTQ+ youth support',
            '👨‍👩‍👧 **Domestic Violence: 1-800-799-7233** - National Hotline'
        ],
        'international': [
            '🌍 **International Association for Suicide Prevention**: iasp.info/resources/Crisis_Centres',
            '🌍 **Befrienders Worldwide**: befrienders.org',
            '🌍 **Find a Helpline**: findahelpline.com'
        ]
    },
    
    # General Wellness Practices
    'wellness_practices': {
        'title': '💪 Daily Mental Health Maintenance',
        'intro': 'Small consistent actions add up to big changes over time:',
        'practices': [
            '😴 **Sleep hygiene**: 7-9 hours, consistent schedule, dark room, no screens 1hr before bed',
            '🏃 **Move your body**: 20-30 min daily (walk, dance, yoga, stretch, anything!)',
            '🍎 **Nourish yourself**: Regular meals, lots of water, limit caffeine after 2pm',
            '☀️ **Sunlight exposure**: 15-30 min outside daily - helps mood and sleep',
            '👥 **Social vitamin**: Connect with at least one person daily, even briefly',
            '🧘 **Mindful moments**: 5-10 min breathing, meditation, or just noticing',
            '🎯 **Purpose & meaning**: Do something aligned with your values each day',
            '📝 **Gratitude practice**: Write 3 things you\'re grateful for before bed',
            '🎨 **Creative outlet**: Draw, write, music, crafts - express yourself',
            '📵 **Digital boundaries**: Take breaks from news/social media doom-scrolling'
        ]
    },
    
    # Encouragement Messages
    'encouragement': {
        'general': [
            '💙 Remember: Seeking help is a sign of strength, not weakness.',
            '🌱 Healing isn\'t linear - ups and downs are normal.',
            '🤝 You don\'t have to go through this alone.',
            '⏰ Give yourself time - progress takes patience.',
            '✨ Small steps forward are still forward.',
            '💪 You\'ve survived 100% of your worst days so far.',
            '🌈 Things can get better, even when it doesn\'t feel that way right now.',
            '🫂 Your feelings are valid, and you deserve support.'
        ],
        'crisis': [
            '💙 **You matter. Your life has value.**',
            '🤝 **You are not alone, even when it feels that way.**',
            '⏰ **These feelings won\'t last forever, even though they feel permanent now.**',
            '📞 **Reaching out for help is brave and important.**',
            '🌅 **Tomorrow could feel different - please stay to find out.**'
        ]
    }
}


# ==========================================
# ENHANCED ADVICE GENERATION FUNCTION
# ==========================================

def generate_personalized_advice(analysis_results):
    """
    Generate emoji-enhanced personalized advice based on Stage 1 analysis
    """
    
    advice_package = {
        'risk_level': analysis_results.get('overall_risk_level', analysis_results.get('risk_level', 'LOW')),
        'crisis_detected': analysis_results.get('crisis_detected', False),
        'primary_message': '',
        'immediate_actions': [],
        'coping_techniques': [],
        'resources': [],
        'wellness_tips': [],
        'encouragement': ''
    }
    
    # 1. PRIMARY RISK-BASED ADVICE
    risk_key = advice_package['risk_level'] if advice_package['risk_level'] in ADVICE_ENGINE['risk_level'] else 'LOW'
    risk_advice = ADVICE_ENGINE['risk_level'][risk_key]
    advice_package['primary_message'] = risk_advice['message']
    advice_package['immediate_actions'] = risk_advice['advice']
    advice_package['resources'] = risk_advice['resources']
    
    # 2. CRISIS OVERRIDE
    if advice_package['crisis_detected']:
        advice_package['primary_message'] = '🚨 **CRISIS DETECTED**: Your responses indicate you may be in immediate distress. Please reach out for help right now. 💙'
        if ADVICE_ENGINE['categories'].get('suicidal_ideation'):
            advice_package['coping_techniques'].append(ADVICE_ENGINE['categories']['suicidal_ideation'])
        advice_package['immediate_actions'] = ADVICE_ENGINE['risk_level']['HIGH']['advice']
        advice_package['resources'] = ADVICE_ENGINE['crisis_resources']['immediate_danger']
        advice_package['encouragement'] = '\n\n'.join(ADVICE_ENGINE['encouragement']['crisis'])
        advice_package['crisis_alert'] = True
        return advice_package
    
    # 3. CATEGORY-SPECIFIC TECHNIQUES
    liwc = analysis_results.get('aggregated_metrics', {}).get('liwc', {}) if isinstance(analysis_results.get('aggregated_metrics', {}), dict) else analysis_results.get('liwc', {})
    if not liwc:
        liwc = analysis_results.get('liwc', {})
    
    if liwc.get('negative_emotion', 0) > 10:
        advice_package['coping_techniques'].append(ADVICE_ENGINE['categories']['negative_emotion'])
    
    if liwc.get('anxiety', 0) > 5:
        advice_package['coping_techniques'].append(ADVICE_ENGINE['categories']['anxiety'])
    
    if liwc.get('hopelessness', 0) > 3:
        advice_package['coping_techniques'].append(ADVICE_ENGINE['categories']['hopelessness'])
    
    if liwc.get('absolutist', 0) > 10 or liwc.get('cognitive_distortion', 0) > 5:
        advice_package['coping_techniques'].append(ADVICE_ENGINE['categories']['cognitive_distortion'])
    
    if liwc.get('isolation', 0) > 3 or liwc.get('social', 0) == 0:
        advice_package['coping_techniques'].append(ADVICE_ENGINE['categories']['isolation'])
    
    if liwc.get('low_self_worth', 0) > 0:
        advice_package['coping_techniques'].append(ADVICE_ENGINE['categories']['low_self_worth'])
    
    if liwc.get('i_pronoun', 0) > 12:
        advice_package['coping_techniques'].append(ADVICE_ENGINE['categories']['high_rumination'])
    
    temporal = analysis_results.get('aggregated_metrics', {}).get('temporal', {}) if isinstance(analysis_results.get('aggregated_metrics', {}), dict) else analysis_results.get('temporal', {})
    if not temporal:
        temporal = analysis_results.get('temporal', {})
    if not temporal.get('has_future_orientation', False):
        advice_package['coping_techniques'].append(ADVICE_ENGINE['categories']['no_future_orientation'])
    
    # Check for behavioral shutdown indicators
    if (liwc.get('positive_emotion', 0) == 0 and 
        liwc.get('negative_emotion', 0) > 15):
        advice_package['coping_techniques'].append(ADVICE_ENGINE['categories']['behavioral_shutdown'])
    
    # 4. WELLNESS TIPS
    if advice_package['risk_level'] in ['LOW', 'MODERATE']:
        advice_package['wellness_tips'] = ADVICE_ENGINE['wellness_practices']['practices']
    
    # 5. ENCOURAGEMENT
    import random
    advice_package['encouragement'] = random.choice(ADVICE_ENGINE['encouragement']['general'])
    
    return advice_package


# ==========================================
# ENHANCED FORMATTING FOR DISPLAY
# ==========================================

def format_advice_for_display(advice_package):
    """Format emoji-enhanced advice for frontend display"""
    output = []
    risk_emoji = {'LOW': '✅', 'MODERATE': '⚠️', 'HIGH': '🔴'}
    output.append(f"\n{risk_emoji.get(advice_package.get('risk_level','LOW'))} **ASSESSMENT RESULT: {advice_package.get('risk_level','LOW')} RISK**\n")
    output.append("="*60 + "\n")
    output.append(f"{advice_package.get('primary_message','')}\n\n")
    if advice_package.get('crisis_alert'):
        output.append("🚨 " + "="*58 + " 🚨\n")
        output.append("**IMMEDIATE ACTION REQUIRED**\n")
        output.append("🚨 " + "="*58 + " 🚨\n\n")
    output.append("📋 **What To Do Right Now:**\n")
    output.append("-"*60 + "\n")
    for action in advice_package.get('immediate_actions', []):
        output.append(f"{action}\n")
    output.append("\n")
    if advice_package.get('coping_techniques'):
        output.append("🛠️ **Personalized Coping Techniques:**\n")
        output.append("="*60 + "\n\n")
        for technique_set in advice_package.get('coping_techniques', []):
            output.append(f"**{technique_set.get('title','')}**\n")
            if 'intro' in technique_set:
                output.append(f"_{technique_set.get('intro')}_\n\n")
            for technique in technique_set.get('techniques', []):
                output.append(f"  {technique}\n")
            if 'warning' in technique_set:
                output.append(f"\n{technique_set.get('warning')}\n")
            output.append("\n")
    output.append("📞 **Resources & Support:**\n")
    output.append("="*60 + "\n")
    for resource in advice_package.get('resources', []):
        output.append(f"{resource}\n")
    output.append("\n")
    if advice_package.get('wellness_tips'):
        output.append("💪 **Daily Wellness Habits to Build:**\n")
        output.append("="*60 + "\n")
        if 'intro' in ADVICE_ENGINE['wellness_practices']:
            output.append(f"_{ADVICE_ENGINE['wellness_practices'].get('intro','')}_\n\n")
        for tip in advice_package.get('wellness_tips', []):
            output.append(f"{tip}\n")
        output.append("\n")
    if advice_package.get('encouragement'):
        output.append("-"*60 + "\n")
        output.append(f"💙 {advice_package.get('encouragement')}\n")
        output.append("-"*60 + "\n")
    return ''.join(output)

def run_stage1_assessment(user_responses):
    """
    Main API function - Call this from Flask/FastAPI endpoint
    
    Args:
        user_responses: Dictionary with format:
            {
                'q1': 'user response text',
                'q2': 'user response text',
                ...
                'q6': 'user response text'
            }
    
    Returns:
        Dictionary with Stage 1 results ready for frontend
    """
    results = analyze_all_stage1_responses(user_responses)

    # Generate personalized advice package (emoji-enhanced)
    try:
        advice_package = generate_personalized_advice(results)
        advice_text = format_advice_for_display(advice_package)
    except Exception:
        advice_package = {}
        advice_text = ''

    api_response = {
        'status': 'success',
        'stage': 'stage1_pras',
        'timestamp': results['timestamp'],
        'summary': {
            'overall_risk_score': results['overall_risk_score'],
            'risk_level': results['overall_risk_level'],
            'crisis_detected': results['crisis_detected'],
            'confidence': results['stage1_signal']['confidence']
        },
        'metrics': {
            'questions_analyzed': results['questions_analyzed'],
            'valid_responses': results['valid_responses'],
            'average_positive_emotion': results['aggregated_metrics']['liwc'].get('positive_emotion', 0) if results['aggregated_metrics'] else 0,
            'average_negative_emotion': results['aggregated_metrics']['liwc'].get('negative_emotion', 0) if results['aggregated_metrics'] else 0,
            'average_hopelessness': results['aggregated_metrics']['liwc'].get('hopelessness', 0) if results['aggregated_metrics'] else 0,
            'average_i_pronoun': results['aggregated_metrics']['pronouns']['i_percentage'] if results['aggregated_metrics'] else 0,
            'future_orientation_percentage': results['aggregated_metrics']['temporal']['percentage_with_future'] if results['aggregated_metrics'] else 0,
            'average_sentiment': results['aggregated_metrics']['sentiment']['compound'] if results['aggregated_metrics'] else 0
        },
        'red_flags': {
            'total_critical': results['red_flags_summary']['total_critical'],
            'total_warning': results['red_flags_summary']['total_warning'],
            'details': results['red_flags_summary']['all_flags']
        },
        'per_question_scores': {
            q_id: {
                'risk_score': analysis['risk_score'],
                'risk_level': analysis['risk_level'],
                'valid': analysis['valid']
            }
            for q_id, analysis in results['individual_analyses'].items()
        },
        'stage1_signal': results['stage1_signal'],
        'next_action': determine_next_action(results),
        'advice': advice_package,
        'advice_text': advice_text
    }
    
    return api_response


def determine_next_action(results):
    """Determine what should happen next based on results"""
    if results['crisis_detected']:
        return {
            'action': 'CRISIS_INTERVENTION',
            'message': 'Immediate crisis detected. Display emergency resources.',
            'skip_remaining_stages': False,
            'resources': [
                'National Suicide Prevention Lifeline: 9152987821',
                'Crisis Text Line: Text HOME to 14416',
                'Emergency Services: 100 '
            ]
        }
    elif results['overall_risk_level'] == 'HIGH':
        return {
            'action': 'HIGH_RISK_PROTOCOL',
            'message': 'High risk detected. Recommend professional evaluation within 24-48 hours.',
            'continue_to_stage2': True
        }
    elif results['overall_risk_level'] == 'MODERATE':
        return {
            'action': 'CONTINUE_ASSESSMENT',
            'message': 'Moderate risk detected. Continue to Stage 2 for comprehensive evaluation.',
            'continue_to_stage2': True
        }
    else:
        return {
            'action': 'CONTINUE_ASSESSMENT',
            'message': 'Low risk detected. Continue to Stage 2.',
            'continue_to_stage2': True
        }


# ==========================================
# TEST FUNCTION
# ==========================================

if __name__ == "__main__":
    import json
    
    print("Testing Stage 1 PRAS Module...")
    print("="*60)
    
    test_responses = {
        'q1': 'I have been feeling okay, some stress but managing with support.',
        'q2': 'My typical day involves work, exercise, and spending time with family.',
        'q3': 'Looking forward to vacation next month and starting a new project.',
        'q4': 'My family and friends are supportive. I feel connected to them.',
        'q5': 'I cope by talking to friends, exercising, and taking breaks when needed.',
        'q6': 'I would describe myself as hardworking, caring, and resilient.'
    }
    
    result = run_stage1_assessment(test_responses)
    
    print("\nRESULTS:")
    print(json.dumps(result['summary'], indent=2))
    print("\nTest complete! Module is working.")
