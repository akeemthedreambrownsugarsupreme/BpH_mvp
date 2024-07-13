import pandas as pd
from .tokenization import count_tokens
from .embeddings import compute_doc_embeddings
from .similarity import order_by_similarity
from config import logging

def load_data(filepath: str) -> pd.DataFrame:
    """Load data from a CSV file and return it as a DataFrame."""
    data = pd.read_csv(filepath)
    return data

def print_token_statistics(tokens: dict):
    """Print the statistics of the token counts."""
    logging.info("Max number of tokens in a row:", max(tokens["tokens_per_row"]))

def print_embedding_statistics(document_embeddings: list):
    """Print the statistics of the document embeddings."""
    logging.info("Length of document embeddings:", len(document_embeddings))
    logging.info("Length of each document embedding:", len(document_embeddings[0]))

def print_similarities(similarities: list, data: list[str]):
    """Print the similarities and corresponding data entries."""
    for similarity, idx in similarities:
        logging.info(f"Similarity: {similarity}, Index: {idx}")
        logging.info(data[idx])
        logging.info("\n")

def get_similar_contexts(query: str, document_embeddings: list[dict], top_n: int = 5) -> list:
    """Get the most similar contexts for a given query."""
    similarities = order_by_similarity(query, document_embeddings)
    top_similarities = similarities[:top_n]
    similar_contexts = [document_embeddings[idx]["text"] for _, idx in top_similarities]
    return similar_contexts

def convert_to_str_data(df: pd.DataFrame) -> list[str]:
    """Convert a row dictionary to a string."""
    return [" ".join([f"{key}: {value}" for key, value in row.items()]) for _, row in df.iterrows()]

def get_contents(filepath: str) -> list[str]:
    data = load_data(filepath)
    # convert into str
    str_data = convert_to_str_data(data)
    # tokens = count_tokens(data.to_dict(orient="records"))
    # print_token_statistics(tokens)
    return str_data

# def process_and_find_similarities(filepath: str, query: str, top_n: int = 5):
#     """Tokenize the data, compute embeddings, and print statistics and similarities."""
#     data = load_data(filepath)
#     # convert into str
#     str_data = convert_to_str_data(data)
#     # tokens = count_tokens(data.to_dict(orient="records"))
#     # print_token_statistics(tokens)
#     document_embeddings = compute_doc_embeddings(str_data)
#     # save the document embeddings as vector data
#     # print_embedding_statistics(document_embeddings)
#     document_similarities = order_by_similarity(query, document_embeddings)
#     # print_similarities(document_similarities, str_data)
#     similar_contexts = get_similar_contexts(query, document_embeddings, str_data, top_n)
#     return similar_contexts