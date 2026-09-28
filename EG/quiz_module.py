from ai_client import generate_json


def generate_quiz(topic: str, number_of_questions: int = 5):

    prompt = f"""
Create {number_of_questions} multiple-choice questions
about the following topic:

{topic}

Return ONLY valid JSON.

Format:

[
    {{
        "question": "Question text",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "answer": "Correct option",
        "explanation": "Short explanation"
    }}
]

Rules:

- Exactly 4 options for every question.
- The answer must exactly match one option.
- Questions must be educational.
- Do not add Markdown.
- Do not add any text outside JSON.
"""

    result = generate_json(prompt)

    if not isinstance(result, list):
        raise ValueError("Quiz response must be a list.")

    return result