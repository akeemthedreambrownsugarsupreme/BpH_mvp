import sys
import os
import config

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data_collection import collect_data
from data.data_preprocessing import preprocess_data
from llm_integration.contexts import get_contents, get_similar_contexts
from llm_integration.query import construct_prompt, answer_with_gpt_4
from llm_integration.embeddings import compute_doc_embeddings, load_embeddings_from_json, save_embeddings_to_json

def main():
    collect_data()
    preprocess_data()
    contexts_data_path = "data/realtor_ca_data/residential_listings.csv"
    
    embeddings_path = "data/realtor_ca_data/residential_listings_embeddings.json"
    contexts = get_contents(contexts_data_path)
    doc_embeddings = compute_doc_embeddings(contexts)
    
    save_embeddings_to_json(doc_embeddings, embeddings_path)
    doc_embeddings = load_embeddings_from_json(embeddings_path)
    
    prompt = "What will be best rental apartment for a single mom of a todler in a good neighborhood with good schools?"
    similar_contexts = get_similar_contexts(prompt, doc_embeddings, top_n=10)

    response, context_length = answer_with_gpt_4(prompt, similar_contexts, show_prompt=False)
    print("Model response: ", response)

if __name__ == "__main__":
    main()
