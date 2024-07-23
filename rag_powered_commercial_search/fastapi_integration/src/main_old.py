import os
import logging
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from build_query_embedding import build_query_embedding, save_embedding
from perform_semantic_search import (
    load_query_and_embedding,
    perform_semantic_search,
    extract_contexts,
    create_prompt,
    get_gpt4_response,
)

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/build_query/", response_class=HTMLResponse)
def build_query(
    request: Request,
    building_type: str = Form(...),
    residential_type: str = Form(None),
    single_family_type: str = Form(None),
    apartment_type: str = Form(None),
    location_type: str = Form(...),
):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_file_path = os.path.join(current_dir, "../data/query_embedding.npz")

        final_choice, embed = build_query_embedding(
            building_type,
            residential_type,
            single_family_type,
            apartment_type,
            location_type,
        )
        
        save_embedding(output_file_path, final_choice, embed)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "message": "Query and embedding created successfully",
                "query": final_choice,
            },
        )

    except Exception as e:
        logger.error(f"Error in /build_query/: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search/", response_class=HTMLResponse)
def search(request: Request):
    try:
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")
        query_embedding_path = os.path.join(data_dir, "query_embedding.npz")

        query, query_embedding = load_query_and_embedding(query_embedding_path)
        response = perform_semantic_search(query_embedding)
        contexts = extract_contexts(response)
        prompt = create_prompt(query, contexts)
        gpt4_response = get_gpt4_response(prompt)

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "query": query, "response": gpt4_response},
        )

    except Exception as e:
        logger.error(f"Error in /search/: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
