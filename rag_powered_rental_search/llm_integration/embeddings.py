import config
from openai import OpenAI
import json

client = OpenAI(api_key=config.OPENAI_API_KEY)

def get_embedding(text):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=config.EMBEDDING_MODEL).data[0].embedding

def compute_doc_embeddings(rows: list[str]) -> list[dict]:
    """
    Create an embedding for each row in the dataframe using the OpenAI Embeddings API.
    
    Return a dictionary that maps between each embedding vector and the index of the row that it corresponds to.
    """
    return [{"text": row, "embedding": get_embedding(row)} for row in rows]

def save_embeddings_to_json(embeddings: list[dict], filepath: str):
    """Save the embeddings to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(embeddings, f)

def load_embeddings_from_json(filepath: str) -> list[dict]:
    """Load the embeddings from a JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)

