import google.generativeai as genai

from app.config import GEMINI_API_KEY


if not GEMINI_API_KEY:

    raise RuntimeError(
        "GEMINI_API_KEY is missing from .env"
    )


genai.configure(
    api_key=GEMINI_API_KEY
)


MODEL_NAME = "gemini-2.5-flash"


def generate_response(
    prompt: str
):

    model = genai.GenerativeModel(
        MODEL_NAME
    )

    response = model.generate_content(
        prompt
    )

    return response.text