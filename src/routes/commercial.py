# from fastapi import APIRouter
# from rag_powered_commercial_search.data_pipelines.src.build_query_embedding import build_query_embedding as commercial_build_query_embedding
# from rag_powered_commercial_search.data_pipelines.src.perform_semantic_search import perform_semantic_search as commercial_perform_semantic_search

# router = APIRouter()

# @router.get("/embed")
# def embed_text(text: str):
#     embedding = commercial_build_query_embedding(text)
#     return {"embedding": embedding}

# @router.post("/search")
# def perform_search(query: str):
#     results = commercial_perform_semantic_search(query)
#     return {"results": results}