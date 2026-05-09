# Compatibility wrapper to expose names expected by the Streamlit app
# This simply re-exports symbols from my_model.py

from my_model import (
    STAGE1_QUESTIONS,
    STAGE2_QUESTIONS,
    STAGE3_QUESTIONS,
    DASS21_QUESTIONS,
    DASS21_RESPONSE_OPTIONS,
    DASS21_INSTRUCTIONS,
    STAGE2_IMAGE_POOL,
    STAGE_WEIGHTS,
    run_stage1_assessment,
    run_stage2_assessment,
    run_stage3_assessment,
    run_final_assessment,
    calculate_final_weighted_score,
    generate_personalized_advice,
    format_advice_for_display
)

__all__ = [
    'STAGE1_QUESTIONS',
    'STAGE2_QUESTIONS',
    'STAGE3_QUESTIONS',
    'DASS21_QUESTIONS',
    'DASS21_RESPONSE_OPTIONS',
    'DASS21_INSTRUCTIONS',
    'STAGE2_IMAGE_POOL',
    'STAGE_WEIGHTS',
    'run_stage1_assessment',
    'run_stage2_assessment',
    'run_stage3_assessment',
    'run_final_assessment',
    'calculate_final_weighted_score',
    'generate_personalized_advice',
    'format_advice_for_display'
]
