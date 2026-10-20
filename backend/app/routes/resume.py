
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.resume_parser import (
    MAX_FILE_SIZE,
    ResumeParsingError,
    extract_resume_text,
)

router = APIRouter(prefix="/api/v1/resume", tags=["Resume"])


@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="Please upload a PDF file.",
        )

    # Read at most 1 byte beyond the limit to detect oversized uploads.
    contents = await file.read(MAX_FILE_SIZE + 1)

    try:
        result = extract_resume_text(contents)
        return {
            "filename": file.filename,
            **result,
        }
    except ResumeParsingError as exc:
        message = str(exc)
        status_code = 413 if "5 MB" in message else 422
        raise HTTPException(
            status_code=status_code,
            detail=message,
        ) from exc
    finally:
        await file.close()
