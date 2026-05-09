import os
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import stage1_pras


class Stage1Request(BaseModel):
    responses: Dict[str, str] = Field(
        ...,
        description="Map of question IDs to free-text responses (e.g., q1..q6).",
    )


class Stage2Request(BaseModel):
    response: str = Field(..., min_length=1)
    image_id: Optional[str] = None
    image_prompt: Optional[str] = None
    user_id: Optional[str] = None
    image_title: Optional[str] = None
    image_path: Optional[str] = None


class Stage3Request(BaseModel):
    responses: Dict[str, int] = Field(
        ...,
        description="Map of DASS-21 IDs (dass_1..dass_21) to values 0..3.",
    )


class FinalAssessmentRequest(BaseModel):
    stage1_results: dict
    stage2_results: dict
    stage3_results: dict


class BatchAssessmentRequest(BaseModel):
    stage1: Stage1Request
    stage2: Stage2Request
    stage3: Stage3Request


def _parse_allowed_origins() -> List[str]:
    raw = os.getenv(
        "CORS_ALLOW_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173",
    )
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(
    title="Mental Wellness Assessment API",
    version="1.0.0",
    description="FastAPI wrapper for PRAS/ASNA/DASS-21 backend assessment functions.",
)

allowed_origins = _parse_allowed_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https?://(localhost|127\\.0\\.1)(:\\d+)?$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "mental-wellness-api",
        "cors_allowed_origins": allowed_origins,
    }


@app.post("/stage1/assess")
def assess_stage1(payload: Stage1Request):
    try:
        return stage1_pras.run_stage1_assessment(payload.responses)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Stage 1 assessment failed: {exc}")


@app.get("/stage2/image/{user_id}")
def get_stage2_image(user_id: str):
    import hashlib

    hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    pool = stage1_pras.STAGE2_IMAGE_POOL
    selected = pool[hash_val % len(pool)]
    return selected


@app.post("/stage2/assess")
def assess_stage2(payload: Stage2Request):
    try:
        return stage1_pras.run_stage2_assessment(
            payload.response,
            image_id=payload.image_id,
            image_prompt=payload.image_prompt,
            user_id=payload.user_id,
            image_title=payload.image_title,
            image_path=payload.image_path,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Stage 2 assessment failed: {exc}")


@app.post("/stage3/assess")
def assess_stage3(payload: Stage3Request):
    try:
        invalid_values = [
            key for key, value in payload.responses.items() if not isinstance(value, int) or value < 0 or value > 3
        ]
        if invalid_values:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid DASS-21 values for: {', '.join(invalid_values)}. Expected integers 0-3.",
            )

        return stage1_pras.run_stage3_assessment(payload.responses)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Stage 3 assessment failed: {exc}")


@app.post("/assessment/final")
def final_assessment(payload: FinalAssessmentRequest):
    try:
        return stage1_pras.run_final_assessment(
            payload.stage1_results,
            payload.stage2_results,
            payload.stage3_results,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Final assessment failed: {exc}")


@app.post("/assessment/run-all")
def run_all_stages(payload: BatchAssessmentRequest):
    try:
        stage1_result = stage1_pras.run_stage1_assessment(payload.stage1.responses)
        stage2_result = stage1_pras.run_stage2_assessment(
            payload.stage2.response,
            image_id=payload.stage2.image_id,
            image_prompt=payload.stage2.image_prompt,
            user_id=payload.stage2.user_id,
            image_title=payload.stage2.image_title,
            image_path=payload.stage2.image_path,
        )

        invalid_values = [
            key
            for key, value in payload.stage3.responses.items()
            if not isinstance(value, int) or value < 0 or value > 3
        ]
        if invalid_values:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid DASS-21 values for: {', '.join(invalid_values)}. Expected integers 0-3.",
            )

        stage3_result = stage1_pras.run_stage3_assessment(payload.stage3.responses)
        final_result = stage1_pras.run_final_assessment(stage1_result, stage2_result, stage3_result)

        return {
            "stage1": stage1_result,
            "stage2": stage2_result,
            "stage3": stage3_result,
            "final": final_result,
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Batch assessment failed: {exc}")
