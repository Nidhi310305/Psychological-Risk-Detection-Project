import streamlit as st
import streamlit.components.v1 as components
import time
import streamlit as st
import streamlit.components.v1 as components
import time
from datetime import datetime
import random

# Import your Stage 1 backend
import stage1_pras

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Mental Wellness Check-In 🌱",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CUSTOM CSS - BEAUTIFUL THEME
# ==========================================

st.markdown("""
<style>
    /* Main Background - Soft Gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Content Container - Glassmorphism Effect */
    .main .block-container {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(6px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.6);
        color: #0b2545; /* Ensure high-contrast dark text inside container */
    }
    
    /* Headers - High contrast for readability inside white container */
    h1 {
        color: #0b2545;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        font-size: 3rem !important;
        margin-bottom: 1rem;
        text-shadow: 0 1px 0 rgba(255,255,255,0.6);
    }
    
    h2 {
        color: #0b2545;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-top: 2rem;
    }
    
    h3 {
        color: #0b2545;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Text Areas - Soft & Inviting */
    .stTextArea textarea {
        background: linear-gradient(135deg, #ffffff 0%, #fbfbfc 100%);
        border: 2px solid rgba(11,37,69,0.12);
        border-radius: 12px;
        padding: 13px;
        font-size: 1.05rem;
        transition: all 0.2s ease;
        color: #0b2545; /* dark input text for readability */
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.12);
        transform: none;
    }
    
    /* Buttons - Gradient & Animated */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 40px;
        font-size: 1.2rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Progress Bar - Colorful */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    }
    
    /* Info/Success/Warning Boxes */
    .stAlert {
        border-radius: 15px;
        border-left: 5px solid;
        padding: 1rem;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Celebration Animation */
    @keyframes celebrate {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .celebration {
        animation: celebrate 0.6s ease;
    }
    
    /* Emoji Styling */
    .big-emoji {
        font-size: 4rem;
        text-align: center;
        animation: bounce 1s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Card Style for Results */
    .result-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 5px solid;
        transition: transform 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateY(-5px);
    }
    
    .low-risk {
        border-left-color: #10b981;
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    }
    
    .moderate-risk {
        border-left-color: #f59e0b;
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
    }
    
    .high-risk {
        border-left-color: #ef4444;
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
    }
    
    /* Word Count Badge */
    .word-count {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# CONFETTI ANIMATION FUNCTION
# ==========================================

def show_confetti():
    """Display confetti animation"""
    components.html("""
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            confetti({
                particleCount: 100,
                spread: 70,
                origin: { y: 0.6 }
            });
        </script>
    """, height=0)

def show_celebration():
    """Display star celebration"""
    components.html("""
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            const defaults = {
                spread: 360,
                ticks: 50,
                gravity: 0,
                decay: 0.94,
                startVelocity: 30,
                shapes: ['star'],
                colors: ['FFE400', 'FFBD00', 'E89400', 'FFCA6C', 'FDFFB8']
            };

            function shoot() {
                confetti({
                    ...defaults,
                    particleCount: 40,
                    scalar: 1.2,
                    shapes: ['star']
                });

                confetti({
                    ...defaults,
                    particleCount: 10,
                    scalar: 0.75,
                    shapes: ['circle']
                });
            }

            setTimeout(shoot, 0);
            setTimeout(shoot, 100);
            setTimeout(shoot, 200);
        </script>
    """, height=0)

# ==========================================
# ENCOURAGING MESSAGES
# ==========================================

ENCOURAGEMENT_MESSAGES = [
    "🌟 You're doing great! Keep going!",
    "💪 One step closer! You've got this!",
    "✨ Amazing progress! Keep sharing!",
    "🎯 You're being so brave right now!",
    "🌈 Your honesty helps us help you better!",
    "💙 Thank you for taking this seriously!",
    "🌱 Every answer helps - you're doing wonderfully!",
    "🎨 Your thoughts matter - keep expressing!",
    "🚀 Halfway there! You're crushing it!",
    "🌸 Beautiful work! Almost done!",
]

COMPLETION_MESSAGES = [
    "🎉 Incredible! You completed the assessment!",
    "🏆 You did it! That took courage!",
    "💫 All done! We're so proud of you!",
    "🌟 Assessment complete! You're amazing!",
    "✨ Finished! That's real strength!",
]

# ==========================================
# WORD COUNT HELPER
# ==========================================

def count_words(text):
    """Count words in text"""
    if not text:
        return 0
    return len(text.split())

def get_word_count_message(count):
    """Get encouraging message based on word count"""
    if count == 0:
        return "✍️ Start sharing your thoughts..."
    elif count < 10:
        return f"📝 {count} words - Keep going! (10 min)"
    else:
        return f"✅ {count} words - Perfect! Thank you!"

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'assessment_complete' not in st.session_state:
    st.session_state.assessment_complete = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()

# ==========================================
# WELCOME SCREEN
# ==========================================

def show_welcome():
    st.markdown('<div class="big-emoji">🧠💙</div>', unsafe_allow_html=True)
    st.title("Mental Wellness Check-In")
    
    st.markdown("""
     <div style='text-align: center; font-size: 1.3rem; color: #f8f8ff; font-weight: 600; margin: 2rem 0;'>
      Welcome! We're here to support you. 🤗
     </div>
""", unsafe_allow_html=True)
    
    st.markdown("""
    ### 📋 What to Expect:
    - **6 questions** about how you've been feeling
    - **10-15 minutes** of your time
    - **Completely confidential** - your privacy matters
    - **Personalized insights** and helpful resources at the end
    
    ### 💙 Please know:
    - There are no "right" or "wrong" answers
    - Be as honest as possible - it helps us help you better
    - Take breaks if you need to
    - You can close this anytime and come back
    """, unsafe_allow_html=True)
    
    st.success("""
    🌟 **You're taking an important step** by checking in on your mental health. 
    That takes real courage! We're proud of you.
    """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Let's Begin!", key="start_button"):
            # mark that the assessment has started so we leave the welcome screen
            st.session_state.current_question = 0
            # add a small sentinel to responses so it's no longer empty
            if not st.session_state.get('responses'):
                st.session_state.responses = {'_started': True}
            show_confetti()
            st.rerun()

# ==========================================
# QUESTION SCREEN
# ==========================================

def show_question():
    questions = stage1_pras.STAGE1_QUESTIONS
    current_q = st.session_state.current_question
    question_data = questions[current_q]
    
    # Progress bar
    progress = (current_q) / len(questions)
    st.progress(progress)
    st.markdown(f"""
    <div style='text-align: center; color: #764ba2; font-size: 1.1rem; margin: 1rem 0;'>
    Question {current_q + 1} of {len(questions)} 
    {' '.join(['⭐' for _ in range(current_q + 1)])}
    {' '.join(['☆' for _ in range(len(questions) - current_q - 1)])}
    </div>
    """, unsafe_allow_html=True)
    
    # Question title with emoji
    focus_emojis = {
        'emotional_state': '😊',
        'behavioral_activation': '🌅',
        'future_orientation': '🔮',
        'social_connections': '👥',
        'coping_mechanisms': '🛠️',
        'self_perception': '🪞'
    }
    
    emoji = focus_emojis.get(question_data['focus'], '💭')
    st.markdown(f"## {emoji} {question_data['question']}")
    
    # Encouraging subtitle
    st.markdown(f"""
    <div style='color: #0b2545; font-style: italic; margin-bottom: 1rem; font-weight:500;'>
    Take your time and share what feels right. There's no pressure. 💙
    </div>
    """, unsafe_allow_html=True)
    
    # Text area with previous response if exists
    default_value = st.session_state.responses.get(question_data['id'], "")
    response = st.text_area(
        "Your thoughts:",
        value=default_value,
        height=200,
        placeholder="Share as much or as little as feels comfortable... We're listening. 🌸",
        key=f"response_{current_q}",
        label_visibility="collapsed"
    )

    # Word count feedback
    word_count = count_words(response)
    word_msg = get_word_count_message(word_count)

    if word_count < 10:
        st.markdown(f"""
        <div class='word-count' style='background: #f59e0b;'>
        {word_msg}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='word-count' style='background: #10b981;'>
        {word_msg}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if current_q > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.responses[question_data['id']] = response
                st.session_state.current_question -= 1
                st.rerun()

    with col2:
        # Encouraging message
        if response and word_count >= 10:
            encouragement = random.choice(ENCOURAGEMENT_MESSAGES)
            st.success(encouragement)

    with col3:
        if current_q < len(questions) - 1:
            # Next button
            if st.button("Next ➡️", use_container_width=True, disabled=(word_count < 10)):
                if word_count >= 10:
                    st.session_state.responses[question_data['id']] = response
                    st.session_state.current_question += 1
                    show_confetti()
                    st.rerun()
                else:
                    st.warning("Please write at least 10 words to continue. We need a bit more information to help you best! 💙")
        else:
            # Submit button
            if st.button("✨ Complete Assessment", use_container_width=True, disabled=(word_count < 10)):
                if word_count >= 10:
                    st.session_state.responses[question_data['id']] = response
                    st.session_state.assessment_complete = True
                    show_celebration()
                    st.rerun()
                else:
                    st.warning("Please write at least 10 words for this final question. You're almost there! 💪")

# ==========================================
# RESULTS SCREEN
# ==========================================

def show_results():
    # Celebration
    st.balloons()
    completion_msg = random.choice(COMPLETION_MESSAGES)
    st.markdown(f"<h1>{completion_msg}</h1>", unsafe_allow_html=True)
    
    # Processing message
    with st.spinner("🔍 Analyzing your responses with care..."):
        time.sleep(2)  # Dramatic pause
        results = stage1_pras.run_stage1_assessment(st.session_state.responses)
    
    st.success("✅ Analysis complete! Here are your personalized insights:")
    
    # ==========================================
    # RISK LEVEL DISPLAY - BIG & CLEAR
    # ==========================================
    
    risk_level = results['summary']['risk_level']
    risk_score = results['summary']['overall_risk_score']
    crisis = results['summary']['crisis_detected']
    
    # Risk level styling
    risk_colors = {
        'LOW': {'color': '#10b981', 'bg': '#ecfdf5', 'emoji': '✅', 'class': 'low-risk'},
        'MODERATE': {'color': '#f59e0b', 'bg': '#fffbeb', 'emoji': '⚠️', 'class': 'moderate-risk'},
        'HIGH': {'color': '#ef4444', 'bg': '#fef2f2', 'emoji': '🔴', 'class': 'high-risk'}
    }
    
    style = risk_colors[risk_level]
    
    # Big risk level card
    st.markdown(f"""
    <div class='result-card {style["class"]}' style='text-align: center; margin: 2rem 0;'>
        <div style='font-size: 5rem; margin-bottom: 1rem;'>{style['emoji']}</div>
        <h1 style='color: {style["color"]}; margin: 0; font-size: 3rem;'>{risk_level} RISK</h1>
        <h2 style='color: {style["color"]}; margin: 1rem 0;'>Score: {risk_score}/100</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Crisis alert if detected
    if crisis:
        st.error("""
        ### 🚨 IMMEDIATE ATTENTION NEEDED
        Your responses indicate you may be experiencing a crisis. 
        **Please reach out for help right now:**
        
        - 🆘 **Call 988** - Suicide & Crisis Lifeline (24/7)
        - 📱 **Text HOME to 741741** - Crisis Text Line
        - 🚑 **Call 911** or go to nearest Emergency Room
        
        **You are not alone. Help is available. You matter.** 💙
        """)
    
    # ==========================================
    # DETAILED METRICS
    # ==========================================
    
    st.markdown("## 📊 Your Assessment Breakdown")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🎭 Emotional Balance",
            value=f"{results['metrics']['average_positive_emotion']:.1f}% positive",
            delta=f"{results['metrics']['average_negative_emotion']:.1f}% negative",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="🔮 Future Outlook",
            value=f"{results['metrics']['future_orientation_percentage']:.0f}%",
            delta="Present" if results['metrics']['future_orientation_percentage'] > 50 else "Limited"
        )
    
    with col3:
        st.metric(
            label="💭 Overall Sentiment",
            value=f"{results['metrics']['average_sentiment']:.2f}",
            delta="Positive" if results['metrics']['average_sentiment'] > 0 else "Negative",
            delta_color="normal" if results['metrics']['average_sentiment'] > 0 else "inverse"
        )
    
    # Red flags summary
    if results['red_flags']['total_critical'] > 0 or results['red_flags']['total_warning'] > 0:
        st.markdown("### 🚩 Concerns Identified")
        
        if results['red_flags']['total_critical'] > 0:
            st.error(f"🔴 **{results['red_flags']['total_critical']} Critical Flag(s)** - Immediate attention recommended")
        
        if results['red_flags']['total_warning'] > 0:
            st.warning(f"⚠️ **{results['red_flags']['total_warning']} Warning Flag(s)** - Monitor closely")
        
        # Show details
        with st.expander("📋 View Detailed Flags"):
            for flag in results['red_flags']['details']:
                severity_icon = "🔴" if flag['severity'] == 'CRITICAL' else "⚠️"
                st.markdown(f"{severity_icon} **{flag['type']}**: {flag['message']}")
    
    # ==========================================
    # PERSONALIZED ADVICE
    # ==========================================
    
    st.markdown("## 💙 Your Personalized Action Plan")
    
    # Generate advice using your advice engine
    from stage1_pras import generate_personalized_advice, format_advice_for_display
    
    advice = generate_personalized_advice(results)
    formatted_advice = format_advice_for_display(advice)
    
    # Display advice in expandable sections
    st.markdown(advice['primary_message'])
    
    st.markdown("### 📋 Immediate Actions")
    for action in advice['immediate_actions']:
        st.markdown(f"- {action}")
    
    if advice['coping_techniques']:
        st.markdown("### 🛠️ Coping Techniques for You")
        for technique_set in advice['coping_techniques']:
            with st.expander(f"**{technique_set['title']}**"):
                if 'intro' in technique_set:
                    st.info(technique_set['intro'])
                for technique in technique_set['techniques']:
                    st.markdown(f"- {technique}")
                if 'warning' in technique_set:
                    st.warning(technique_set['warning'])
    
    st.markdown("### 📞 Resources & Support")
    for resource in advice['resources']:
        st.markdown(f"- {resource}")
    
    if advice.get('wellness_tips'):
        with st.expander("💪 Daily Wellness Practices"):
            for tip in advice['wellness_tips']:
                st.markdown(f"- {tip}")

    # ==========================================
    # DOWNLOAD REPORT BUTTON
    # ==========================================
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        report_text = f"""
MENTAL WELLNESS ASSESSMENT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

RISK LEVEL: {risk_level}
OVERALL SCORE: {risk_score}/100
CRISIS DETECTED: {'YES' if crisis else 'NO'}

{formatted_advice}

---
This assessment is for informational purposes only and does not replace 
professional medical advice, diagnosis, or treatment.
"""
        
        st.download_button(
            label="📄 Download Full Report",
            data=report_text,
            file_name=f"mental_wellness_report_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # ==========================================
    # NEXT STEPS
    # ==========================================
    
    st.markdown("---")
    st.markdown("## 🌟 What's Next?")
    
    next_steps_col1, next_steps_col2 = st.columns(2)
    
    with next_steps_col1:
        st.info("""
        ### 📋 Save Your Results
        - Download the report above
        - Share with a healthcare provider if comfortable
        - Use insights for self-reflection
        """)
    
    with next_steps_col2:
        st.success("""
        ### 🎯 Take Action
        - Try one coping technique today
        - Reach out to someone you trust
        - Schedule time for self-care
        """)
    
    # Restart button
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Take Assessment Again", use_container_width=True):
            # Reset session state
            st.session_state.current_question = 0
            st.session_state.responses = {}
            st.session_state.assessment_complete = False
            st.session_state.start_time = datetime.now()
            st.rerun()

# ==========================================
# MAIN APP LOGIC
# ==========================================

def main():
    # Show appropriate screen based on state
    if st.session_state.current_question == 0 and not st.session_state.responses:
        show_welcome()
    elif not st.session_state.assessment_complete:
        show_question()
    else:
        show_results()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #764ba2; padding: 2rem;'>
    <p><strong>Mental Wellness Check-In</strong> | Confidential & Secure</p>
    <p style='font-size: 0.9rem;'>💙 Your mental health matters. You deserve support.</p>
    <p style='font-size: 0.8rem;'>This tool is not a substitute for professional mental health care.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
