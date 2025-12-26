import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # OpenRouter
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    DEFAULT_MODEL = os.getenv(
        "OPENROUTER_MODEL",
        "meta-llama/llama-3-8b-instruct"
    )
    FALLBACK_MODEL = os.getenv(
        "OPENROUTER_FALLBACK_MODEL",
        "mistralai/mixtral-8x7b-instruct"
    )

    TEMPERATURE = 0.0

    # Search
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")

    # RAG
    VECTOR_STORE_PATH = "data/faiss_index"

settings = Settings()
