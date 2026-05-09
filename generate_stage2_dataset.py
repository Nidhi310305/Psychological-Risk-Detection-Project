"""Generate a synthetic Stage 2 dataset with computed model features.

This script creates a CSV that includes:
- Stage 2 free-text responses
- Flattened LIWC/sentiment/pronoun/temporal features
- Red flag metadata
- Risk score and risk level from the current model pipeline
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

from my_model import STAGE2_IMAGE_POOL, STAGE2_QUESTIONS, analyze_single_response

RANDOM_SEED = 42
SAMPLES_PER_PROFILE = {
    "low": 40,
    "moderate": 40,
    "high": 40,
}

LOW_OPENERS = [
    "When I look at this image, I feel calm and connected",
    "This picture makes me think about growth and support",
    "I notice balance in the image and feel mostly hopeful",
    "The image feels meaningful, and I can see positive direction",
]

LOW_MIDDLES = [
    "I have stress sometimes, but I usually manage by talking with friends and family.",
    "I try to stay active, keep a routine, and focus on what I can improve.",
    "I still face challenges, but I can plan ahead and stay motivated most days.",
    "I use coping skills like breathing, journaling, and asking for support when needed.",
]

LOW_ENDINGS = [
    "I am looking forward to future goals and better days.",
    "I feel optimistic about upcoming plans and personal growth.",
    "I think things can improve with steady effort and support.",
]

MOD_OPENERS = [
    "This image feels heavy, and I relate to some tension in it",
    "I see conflict and pressure in this picture",
    "The image makes me think of uncertainty and emotional strain",
    "I notice both hope and distress in the scene",
]

MOD_MIDDLES = [
    "Lately I feel worried and stressed, and some days feel difficult to manage.",
    "I feel lonely at times and overthink things, even when support is available.",
    "My mood changes often, and I struggle with confidence and motivation.",
    "I get anxious about the future and sometimes feel stuck in negative thoughts.",
]

MOD_ENDINGS = [
    "I am trying to cope and I hope things will get better.",
    "I want support and I plan to work through this gradually.",
    "I still have some hope, but it takes effort every day.",
]

HIGH_OPENERS = [
    "This image feels dark and overwhelming to me",
    "I see collapse and emotional pain in this picture",
    "The scene feels empty and hopeless from my perspective",
    "I relate to isolation and fear in this image",
]

HIGH_MIDDLES = [
    "I feel hopeless, powerless, and exhausted, and nothing seems to improve.",
    "I feel alone, anxious, and defeated, and I cannot see any future.",
    "I keep thinking I am a failure, and I feel trapped by constant distress.",
    "I feel severe emotional pain, and I struggle to find meaning in life.",
]

HIGH_ENDINGS = [
    "Some days I feel there is no point and I have no way out.",
    "I do not feel connected to people, and I feel completely isolated.",
    "I am overwhelmed and afraid things will never change.",
]


def _build_response(profile: str) -> str:
    if profile == "low":
        parts = [
            random.choice(LOW_OPENERS),
            random.choice(LOW_MIDDLES),
            random.choice(LOW_ENDINGS),
        ]
    elif profile == "moderate":
        parts = [
            random.choice(MOD_OPENERS),
            random.choice(MOD_MIDDLES),
            random.choice(MOD_ENDINGS),
        ]
    else:
        parts = [
            random.choice(HIGH_OPENERS),
            random.choice(HIGH_MIDDLES),
            random.choice(HIGH_ENDINGS),
        ]

    text = ". ".join(parts).strip()
    if not text.endswith("."):
        text += "."
    return text


def _flatten_row(sample_id: str, image_meta: dict, response_text: str, analysis: dict, profile: str) -> dict:
    liwc = analysis.get("liwc", {})
    sentiment = analysis.get("sentiment", {})
    pronouns = analysis.get("pronouns", {})
    temporal = analysis.get("temporal", {})
    red_flags = analysis.get("red_flags", [])

    return {
        "sample_id": sample_id,
        "source_profile": profile,
        "image_id": image_meta.get("id", ""),
        "image_title": image_meta.get("title", ""),
        "image_file": image_meta.get("file", ""),
        "image_prompt": image_meta.get("prompt", ""),
        "question_id": STAGE2_QUESTIONS[0]["id"],
        "question": STAGE2_QUESTIONS[0]["question"],
        "response_text": response_text,
        "valid": analysis.get("valid", False),
        "errors": " | ".join(analysis.get("errors", [])),
        "token_count": analysis.get("preprocessed", {}).get("token_count", 0),
        "word_count": liwc.get("word_count", 0),
        "sentiment_compound": sentiment.get("compound", 0),
        "sentiment_positive": sentiment.get("positive", 0),
        "sentiment_negative": sentiment.get("negative", 0),
        "sentiment_neutral": sentiment.get("neutral", 0),
        "liwc_positive_emotion": liwc.get("positive_emotion", 0),
        "liwc_negative_emotion": liwc.get("negative_emotion", 0),
        "liwc_anxiety": liwc.get("anxiety", 0),
        "liwc_sadness": liwc.get("sadness", 0),
        "liwc_anger": liwc.get("anger", 0),
        "liwc_absolutist": liwc.get("absolutist", 0),
        "liwc_cognitive_distortion": liwc.get("cognitive_distortion", 0),
        "liwc_death": liwc.get("death", 0),
        "liwc_self_harm": liwc.get("self_harm", 0),
        "liwc_social": liwc.get("social", 0),
        "liwc_isolation": liwc.get("isolation", 0),
        "liwc_past_focus": liwc.get("past_focus", 0),
        "liwc_future_focus": liwc.get("future_focus", 0),
        "liwc_hopelessness": liwc.get("hopelessness", 0),
        "liwc_positive_coping": liwc.get("positive_coping", 0),
        "pronoun_i_percentage": pronouns.get("i_percentage", 0),
        "pronoun_we_percentage": pronouns.get("we_percentage", 0),
        "pronoun_ratio": pronouns.get("ratio", 0),
        "temporal_past_count": temporal.get("past_count", 0),
        "temporal_future_count": temporal.get("future_count", 0),
        "temporal_has_future_orientation": temporal.get("has_future_orientation", False),
        "temporal_has_negative_future": temporal.get("has_negative_future", False),
        "critical_flags_count": analysis.get("critical_flags_count", 0),
        "warning_flags_count": analysis.get("warning_flags_count", 0),
        "red_flag_types": "|".join(sorted({flag.get("type", "") for flag in red_flags if flag.get("type")})),
        "risk_score": analysis.get("risk_score", 0),
        "risk_level": analysis.get("risk_level", "UNKNOWN"),
    }


def main() -> None:
    random.seed(RANDOM_SEED)

    output_dir = Path("data")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "stage2_synthetic_dataset.csv"

    rows = []
    index = 1
    for profile, count in SAMPLES_PER_PROFILE.items():
        for _ in range(count):
            image_meta = random.choice(STAGE2_IMAGE_POOL)
            response_text = _build_response(profile)
            analysis = analyze_single_response(
                STAGE2_QUESTIONS[0]["id"],
                image_meta.get("prompt", STAGE2_QUESTIONS[0]["question"]),
                response_text,
            )
            rows.append(_flatten_row(f"s2_{index:04d}", image_meta, response_text, analysis, profile))
            index += 1

    # Keep column ordering stable for reproducibility.
    fieldnames = list(rows[0].keys()) if rows else []
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    risk_counts = {}
    for row in rows:
        risk_counts[row["risk_level"]] = risk_counts.get(row["risk_level"], 0) + 1

    print(f"Created dataset: {output_path}")
    print(f"Total rows: {len(rows)}")
    print(f"Risk distribution: {risk_counts}")


if __name__ == "__main__":
    main()
