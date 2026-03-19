# Compatibility wrapper to expose names expected by the Streamlit app
# This simply re-exports symbols from my_model.py

from my_model import (
    STAGE1_QUESTIONS,
    run_stage1_assessment,
    generate_personalized_advice,
    format_advice_for_display
)

__all__ = [
    'STAGE1_QUESTIONS',
    'run_stage1_assessment',
    'generate_personalized_advice',
    'format_advice_for_display'
]
