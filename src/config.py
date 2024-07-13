import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Export variables
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
COMPLETIONS_MODEL = os.getenv("COMPLETIONS_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = os.getenv("RAPID_API_HOST")

# constants
listings_type = ["residential", "commercial"]
