import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pinecone = Pinecone(api_key=PINECONE_API_KEY)
index_name = os.getenv("PINECONE_COMMERCIAL_INDEX_NAME")
index = pinecone.Index(index_name)


def validate_metadata(metadata):
    """Ensure the metadata is JSON serializable and valid for Pinecone."""
    for key, value in metadata.items():
        if pd.isna(value):
            metadata[key] = ""
        elif isinstance(value, list):
            metadata[key] = [str(v) for v in value]
        else:
            metadata[key] = str(value)
    return metadata


def upsert_embeddings(embedding_file, max_batch_size):
    data = pd.read_csv(embedding_file)

    # Ensure embeddings column is converted from string to list of floats
    data["embeddings"] = data["embeddings"].apply(eval)

    data_to_upsert = []
    for i, row in data.iterrows():
        metadata = validate_metadata(
            row.drop(["combined_text", "embeddings"]).to_dict()
        )
        data_to_upsert.append((str(i), row["embeddings"], metadata))

    # Split data into batches and upsert each batch
    for start in range(0, len(data_to_upsert), max_batch_size):
        end = start + max_batch_size
        batch = data_to_upsert[start:end]
        index.upsert(vectors=batch)
    print("Embeddings have been upserted to Pinecone successfully.")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    embedding_file_path = os.path.join(
        current_dir, "../data/commercial_data_with_embeddings.csv"
    )

    upsert_embeddings(embedding_file_path, max_batch_size=100)
