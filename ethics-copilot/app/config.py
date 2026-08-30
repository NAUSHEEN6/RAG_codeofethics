import os

from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

CHROMA_PATH = os.getenv(
    "CHROMA_PATH",
    "vectorstore"
)

CASE_API_URL = os.getenv(
    "CASE_API_URL",
    "http://127.0.0.1:8000"
)

OUTLOOK_ENABLED = (
    os.getenv(
        "OUTLOOK_ENABLED",
        "false"
    ).lower()
    == "true"
)