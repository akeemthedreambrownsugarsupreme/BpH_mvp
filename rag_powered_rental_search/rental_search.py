import sys
import os
import config
from config import logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_powered_rental_search.data_processing.data_collection import collect_data
from rag_powered_rental_search.data_processing.data_preprocessing import preprocess_data
from rag_powered_rental_search.llm_integration.contexts import upsert_embeddings, get_similar_contexts_pinecone
from rag_powered_rental_search.llm_integration.query import construct_prompt, answer_with_gpt_4
from rag_powered_rental_search.llm_integration.embeddings import compute_doc_embeddings, load_embeddings_from_json, save_embeddings_to_json

def main():
    # collect_data()
    # preprocess_data()
    # contexts_data_path = "data/realtor_ca_data/residential_listings.csv"
    
    embeddings_path = "data/realtor_ca_data/residential_listings_embeddings.json"
    # contexts = get_contents(contexts_data_path)
    # doc_embeddings = compute_doc_embeddings(contexts)
    
    # save_embeddings_to_json(doc_embeddings, embeddings_path)
    doc_embeddings = load_embeddings_from_json(embeddings_path)
    
    # add documents to Pinecone index
    # upsert_embeddings(doc_embeddings)
    
    prompt = '"Type": "Single Family", "Listing_type": "Residential", "Bedrooms": 2'
    similar_contexts = get_similar_contexts_pinecone(prompt, top_n=5)

    response, context_length = answer_with_gpt_4(prompt, similar_contexts, show_prompt=False)
    logger.info("Response generated suppoccessfully!")
    

def search(query: str):
    similar_contexts = get_similar_contexts_pinecone(query, top_n=5)
    response, context_length = answer_with_gpt_4(query, similar_contexts, show_prompt=False)
    return response

if __name__ == "__main__":
    main()
