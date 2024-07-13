import config
import tiktoken
import pandas as pd
import numpy as np
from openai import OpenAI


client = OpenAI(api_key=config.OPENAI_API_KEY)

def get_embedding(text):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=config.EMBEDDING_MODEL).data[0].embedding

def compute_doc_embeddings(df: pd.DataFrame) -> dict[tuple[str, str], list[float]]:
    """
    Create an embedding for each row in the dataframe using the OpenAI Embeddings API.
    
    Return a dictionary that maps between each embedding vector and the index of the row that it corresponds to.
    """
    return {
        idx: get_embedding(" ".join([f"{key}: {value}" for key, value in row.items()])) for idx, row in df.iterrows()
    }

def count_tokens(rows: list[dict[str]]) -> dict[str, int]:
    """Count the number of tokens in each row."""
    encoder = tiktoken.encoding_for_model(config.COMPLETIONS_MODEL)
    tokens_per_row = []
    for row in rows:
        # whole dict to string including keys and values
        row_str = " ".join([f"{key}: {value}" for key, value in row.items()])
        tokens_per_row.append(len(encoder.encode(row_str)))    
    return {"tokens_per_row": tokens_per_row}

def vector_similarity(x: list[float], y: list[float]) -> float:
    """
    Returns the similarity between two vectors.
    
    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    return np.dot(np.array(x), np.array(y))

def order_by_similarity(query: str, contexts: dict[(str, str), np.array]) -> list[(float, (str, str))]:
    """
    Find the query embedding for the supplied query, and compare it against all of the pre-calculated document embeddings
    to find the most relevant sections. 
    
    Return the list of document sections, sorted by relevance in descending order.
    """
    query_embedding = get_embedding(query)
    
    document_similarities = sorted([
        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in contexts.items()
    ], reverse=True)
    
    return document_similarities


def data_tokenize():
    data = pd.read_csv("data/realtor_ca_data/residential_listings.csv")
    
    # make data is only the first 10 rows
    data = data.head(10)
    
    # print(data.head())
    # print(type(data.to_dict(orient="records")))
    tokens = count_tokens(data.to_dict(orient="records"))
    # find the max number of tokens in a row
    print("Max number of tokens in a row:", max(tokens["tokens_per_row"]))
    
    # print("Type of data:", type(data))
    
    document_embeddings = compute_doc_embeddings(data)
    
    # length of document embeddings
    print("Length of document embeddings:", len(document_embeddings))

    # An example embedding:
    example_entry = list(document_embeddings.items())[0]
    print(f"{example_entry[0]} : {example_entry[1][:5]}... ({len(example_entry[1])} entries)")
    
    document_similarities = order_by_similarity("Attached Garage", document_embeddings)
    
    for similarity, idx in document_similarities:
        print(f"Similarity: {similarity}, Index: {idx}")
        print(data.iloc[idx])
        print("\n")
        

if __name__ == "__main__":
    data_tokenize()



