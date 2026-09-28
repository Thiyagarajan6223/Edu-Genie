import json
import time

from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing in .env"
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


# Try the configured model first.
# If it is temporarily unavailable, try another model.
MODELS_TO_TRY = [
    GEMINI_MODEL,
    "gemini-3.8-flash"
]


def generate_text(prompt: str) -> str:

    last_error = None

    for model in MODELS_TO_TRY:

        if not model:
            continue

        # Don't try the same model twice
        if model in MODELS_TO_TRY[:MODELS_TO_TRY.index(model)]:
            continue

        for attempt in range(2):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if response.text:
                    return response.text.strip()

                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            except Exception as error:

                last_error = error

                error_text = str(error)

                # Retry only temporary availability/rate errors
                if (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "429" in error_text
                ):

                    if attempt == 0:
                        time.sleep(2)
                        continue

                # Move to next model
                break

    raise RuntimeError(
        f"Gemini is temporarily unavailable. "
        f"Please try again in a moment. "
        f"Details: {last_error}"
    )


def clean_json_block(text: str) -> str:

    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def generate_json(prompt: str):

    result = generate_text(prompt)

    result = clean_json_block(result)

    try:

        return json.loads(result)

    except json.JSONDecodeError as error:

        raise RuntimeError(
            f"Invalid JSON returned by Gemini: {error}"
        )