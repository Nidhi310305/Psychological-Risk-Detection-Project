"""Standalone Stage 2 synthetic dataset builder.

Generates a CSV with:
- Stage 2 response text
- Computed features from the current model
- Risk score and risk level

Usage:
  python stage2_dataset_builder.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

from my_model import STAGE2_IMAGE_POOL, STAGE2_QUESTIONS, analyze_single_response

SEED = 123
TOTAL_ROWS = 150
OUTPUT_FILE = Path("data/stage2_dataset_synthetic_v2.csv")

LOW_TEXT = [
    "I feel connected and calm when I look at this image, and I think things can improve with support.",
    "This picture reminds me of balance, and I can manage stress by talking with family and staying active.",
    "I notice hopeful elements in this image and I am planning small goals for the next few months.",
]

MOD_TEXT = [
    "The image feels heavy and uncertain, and I have been worried and stressed with changing mood lately.",
    "I see conflict in this picture, and I feel lonely sometimes though I am trying to cope and improve.",
    "This scene feels tense, and I overthink the future, but I still hope to get better with help.",
]

HIGH_TEXT = [
    "This image feels overwhelming and dark, and I feel hopeless, isolated, and unable to see any future.",
    "I relate to fear and emotional pain here, and I feel powerless, defeated, and stuck every day.",
    "The picture feels empty and distressing, and I feel there is no point and no way out right now.",
]


def build_text(profile: str) -> str:
    if profile == "LOW":
        return random.choice(LOW_TEXT)
    if profile == "MODERATE":
        return random.choice(MOD_TEXT)
    return random.choice(HIGH_TEXT)


def flatten(sample_id: str, profile_hint: str, image_meta: dict, response: str, analysis: dict) -> dict:
    liwc = analysis.get("liwc", {})
    sentiment = analysis.get("sentiment", {})
    pronouns = analysis.get("pronouns", {})
    temporal = analysis.get("temporal", {})
    red_flags = analysis.get("red_flags", [])

    return {
        "sample_id": sample_id,
        "profile_hint": profile_hint,
        "image_id": image_meta.get("id", ""),
        "image_title": image_meta.get("title", ""),
        "response_text": response,
        "valid": analysis.get("valid", False),
        "risk_score": analysis.get("risk_score", 0),
        "risk_level": analysis.get("risk_level", "UNKNOWN"),
        "critical_flags_count": analysis.get("critical_flags_count", 0),
        "warning_flags_count": analysis.get("warning_flags_count", 0),
        "red_flag_types": "|".join(sorted({f.get("type", "") for f in red_flags if f.get("type")})),
        "word_count": liwc.get("word_count", 0),
        "sentiment_compound": sentiment.get("compound", 0),
        "sentiment_positive": sentiment.get("positive", 0),
        "sentiment_negative": sentiment.get("negative", 0),
        "liwc_positive_emotion": liwc.get("positive_emotion", 0),
        "liwc_negative_emotion": liwc.get("negative_emotion", 0),
        "liwc_anxiety": liwc.get("anxiety", 0),
        "liwc_hopelessness": liwc.get("hopelessness", 0),
        "liwc_death": liwc.get("death", 0),
        "liwc_isolation": liwc.get("isolation", 0),
        "liwc_social": liwc.get("social", 0),
        "pronoun_i_percentage": pronouns.get("i_percentage", 0),
        "pronoun_we_percentage": pronouns.get("we_percentage", 0),
        "temporal_future_count": temporal.get("future_count", 0),
        "temporal_has_future_orientation": temporal.get("has_future_orientation", False),
        "temporal_has_negative_future": temporal.get("has_negative_future", False),
    }


def main() -> None:
    random.seed(SEED)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    profiles = ["LOW", "MODERATE", "HIGH"]
    rows = []

    for idx in range(1, TOTAL_ROWS + 1):
        profile = profiles[(idx - 1) % len(profiles)]
        image_meta = random.choice(STAGE2_IMAGE_POOL)
        response = build_text(profile)

        analysis = analyze_single_response(
            question_id=STAGE2_QUESTIONS[0]["id"],
            question_text=image_meta.get("prompt", STAGE2_QUESTIONS[0]["question"]),
            response_text=response,
        )

        rows.append(flatten(f"s2v2_{idx:04d}", profile, image_meta, response, analysis))

    fieldnames = list(rows[0].keys())
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    by_level = {}
    for r in rows:
        by_level[r["risk_level"]] = by_level.get(r["risk_level"], 0) + 1

    print(f"Saved: {OUTPUT_FILE}")
    print(f"Rows: {len(rows)}")
    print(f"Risk distribution: {by_level}")


if __name__ == "__main__":
    main()
