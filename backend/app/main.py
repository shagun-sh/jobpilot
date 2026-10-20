
from fastapi import FastAPI

from app.routes.resume import router as resume_router
from app.routes.analyze import router as analyze_router

app = FastAPI(
    title="JobPilot API",
    description="Resume analysis and job matching platform",
    version="0.1.0",
)

app.include_router(resume_router)
app.include_router(analyze_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "jobpilot-api",
    }
