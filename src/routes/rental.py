from fastapi import APIRouter
from rag_powered_rental_search.llm_integration.embeddings import get_embedding as rental_get_embedding
import rag_powered_rental_search.rental_search as rental_search
import json

router = APIRouter()

@router.post("/search")
def perform_search(query: str):
    results = rental_search.search(query)
    # convert the result as a list of json objects
    if isinstance(results, str):
        results = json.loads(results)
    return {"results": results}