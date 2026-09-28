from pydantic import BaseModel
from typing import List


class QuizQuestion(BaseModel):

    question: str

    options: List[str]

    answer: str

    explanation: str = ""