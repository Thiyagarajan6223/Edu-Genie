import os

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pydantic import BaseModel

from dotenv import load_dotenv

from openai import OpenAI


# ============================================
# LOAD ENVIRONMENT VARIABLES
# ============================================

load_dotenv()


# ============================================
# API KEY
# ============================================

API_KEY = os.getenv("OPENAI_API_KEY")


if not API_KEY:

    raise RuntimeError(
        "OPENAI_API_KEY is missing from .env"
    )


# ============================================
# OPENAI CLIENT
# ============================================

client = OpenAI(
    api_key=API_KEY
)


# ============================================
# FASTAPI
# ============================================

app = FastAPI(
    title="EduGenie API"
)


# ============================================
# REQUEST MODEL
# ============================================

class AskRequest(BaseModel):

    question: str

    type: str


# ============================================
# PROMPTS
# ============================================

PROMPTS = {

    "question_ask": """
You are EduGenie, an AI learning assistant.

Answer the student's question clearly and directly.

Give an immediate answer first.

Then explain the answer in simple language.

Use examples when useful.

Student question:
""",


    "learning_path": """
You are EduGenie, an educational learning-path generator.

Create a structured learning path for the student's requested subject.

Include:

1. Beginner concepts
2. Intermediate concepts
3. Advanced concepts
4. Practice activities
5. Suggested project ideas
6. A reasonable learning order

Make it practical and easy to follow.

Student request:
""",


    "quiz": """
You are EduGenie, an educational quiz generator.

Create a useful quiz based on the student's topic.

Use multiple-choice questions.

Give four options for each question.

At the end, provide the answer key.

Keep the questions appropriate for learning.

Student request:
""",


    "topic_explain": """
You are EduGenie, an AI tutor.

Explain the requested topic clearly.

Start with a simple definition.

Then explain:

1. What it is
2. How it works
3. Why it is important
4. A simple example
5. A real-world example if useful

Use beginner-friendly language.

Student topic:
""",


    "summarize": """
You are EduGenie, an AI summarization assistant.

Summarize the student's provided text.

Keep the important ideas.

Remove unnecessary repetition.

Use clear bullet points when appropriate.

Do not add information that is not present in the supplied text.

Text to summarize:
"""

}


# ============================================
# HOME PAGE
# ============================================

@app.get("/")
async def home():

    return FileResponse(
        "static/index.html"
    )


# ============================================
# ASK API
# ============================================

@app.post("/ask")
async def ask(request: AskRequest):

    question =
        request.question.strip()


    selected_type =
        request.type.strip()


    # ========================================
    # VALIDATE
    # ========================================

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )


    if selected_type not in PROMPTS:

        raise HTTPException(
            status_code=400,
            detail="Invalid learning type."
        )


    # ========================================
    # CREATE PROMPT
    # ========================================

    system_prompt =
        PROMPTS[selected_type]


    user_prompt =
        system_prompt +
        "\n\n" +
        question


    try:

        # ====================================
        # AI REQUEST
        # ====================================

        response = client.responses.create(

            model="gpt-5.6",

            input=[
                {
                    "role": "system",
                    "content": (
                        "You are EduGenie. "
                        "Help students learn clearly."
                    )
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]

        )


        # ====================================
        # GET ANSWER
        # ====================================

        answer =
            response.output_text


        return {

            "success": True,

            "type": selected_type,

            "answer": answer

        }


    except Exception as error:

        print(
            "AI ERROR:",
            str(error)
        )


        raise HTTPException(

            status_code=500,

            detail=
                "Unable to generate an answer."
        )


# ============================================
# STATIC FILES
# ============================================

app.mount(

    "/static",

    StaticFiles(
        directory="static"
    ),

    name="static"

)
