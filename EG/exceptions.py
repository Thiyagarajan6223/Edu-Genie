class EduGenieError(Exception):
    """Base exception for EduGenie."""


class APIKeyError(EduGenieError):
    """Raised when Gemini API key is missing."""


class AIResponseError(EduGenieError):
    """Raised when AI response is invalid."""