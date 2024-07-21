import os
from dotenv import load_dotenv
import logging

# Load .env file
load_dotenv()

# Export variables
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
COMPLETIONS_MODEL = os.getenv("COMPLETIONS_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = os.getenv("RAPID_API_HOST")
MAX_TOKEN_LENGTH = int(os.getenv("MAX_TOKEN_LENGTH"))
SEPERATOR = os.getenv("SEPERATOR")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")

# constants
listings_type = ["residential", "commercial"]
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)