
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.skill_matcher import analyze_match

router = APIRouter(prefix="/api/v1", tags=["Analysis"])


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(min_length=1, max_length=100_000)
    job_description: str = Field(min_length=1, max_length=50_000)


class AnalyzeResponse(BaseModel):
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    resume_skills: list[str]
    required_skills: list[str]
    suggestions: list[str]
    preferred_skills: list[str]
    missing_required_skills: list[str]
    missing_preferred_skills: list[str]


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_resume(request: AnalyzeRequest):
    try:
        result = analyze_match(
            request.resume_text,
            request.job_description,
        )
        return result
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc
