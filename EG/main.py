from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import recommend_learning_path


# --------------------------------
# Project directory
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent


# --------------------------------
# FastAPI application
# --------------------------------

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="3.8"
)


# --------------------------------
# Static files
# --------------------------------

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)


# --------------------------------
# Request Models
# --------------------------------

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1)


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    num_questions: int = Field(
        default=5,
        ge=1,
        le=10
    )


# --------------------------------
# Home Page
# --------------------------------

@app.get("/", response_class=HTMLResponse)
async def home():

    html_file = BASE_DIR / "templates" / "index.html"

    if not html_file.exists():
        return HTMLResponse(
            "<h1>Error: index.html not found</h1>",
            status_code=500
        )

    html_content = html_file.read_text(
        encoding="utf-8"
    )

    return HTMLResponse(
        content=html_content
    )


# --------------------------------
# Health Check
# --------------------------------

@app.get("/health")
async def health():

    return {
        "status": "OK",
        "message": "EduGenie is running"
    }


# --------------------------------
# Q&A
# --------------------------------

@app.post("/qa")
async def qa(request: TextRequest):

    try:

        result = answer_question(
            request.text
        )

        return {
            "success": True,
            "answer": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------
# Explanation
# --------------------------------

@app.post("/explain/")
async def explain(request: TextRequest):

    try:

        result = explain_topic(
            request.text
        )

        return {
            "success": True,
            "explanation": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------
# Quiz
# --------------------------------

@app.post("/quiz")
async def quiz(request: QuizRequest):

    try:

        result = generate_quiz(
            request.topic,
            request.num_questions
        )

        return {
            "success": True,
            "quiz": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------
# Summary
# --------------------------------

@app.post("/summarize")
async def summarize(request: TextRequest):

    try:

        result = summarize_text(
            request.text
        )

        return {
            "success": True,
            "summary": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------
# Learning Path
# --------------------------------

@app.post("/learn/recommendations")
async def learning_path(request: TextRequest):

    try:

        result = recommend_learning_path(
            request.text
        )

        return {
            "success": True,
            "recommendations": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------
# Run
# --------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )