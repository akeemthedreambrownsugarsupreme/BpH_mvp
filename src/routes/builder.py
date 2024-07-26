from fastapi import APIRouter
import json
from config import logger
from rag_powered_commercial_search.fastapi_integration.src.build_query_embedding import build_query_embedding
from rag_powered_commercial_search.fastapi_integration.src.perform_semantic_search import (
    perform_semantic_search,
    extract_contexts,
    create_prompt,
    get_gpt4_response,
)

router = APIRouter()

@router.post("/search")
def perform_search(query: str):
    query_json = json.loads(query)
    building_type: str = query_json.get("building_type")
    residential_type: str = query_json.get("residential_type")
    single_family_type: str = query_json.get("single_family_type")
    apartment_type: str = query_json.get("apartment_type")
    location_type: str = query_json.get("location_type")
    try:
        query, query_embedding = build_query_embedding(
            building_type,
            residential_type,
            single_family_type,
            apartment_type,
            location_type,
        )
        response = perform_semantic_search(query_embedding)
        contexts = extract_contexts(response)
        prompt = create_prompt(query, contexts)
        gpt4_response = get_gpt4_response(prompt)
        return {"results": gpt4_response}

    except Exception as e:
        logger.error(f"Error in /search/: {e}")
        raise e
