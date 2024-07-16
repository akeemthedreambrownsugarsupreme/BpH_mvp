# RAG-Powered Commercial Search

This project implements a backend system for searching commercial properties using a Retrieval-Augmented Generation (RAG) based Large Language Model (LLM) integrated with FastAPI. The `index.html` file is used as a simple UI for testing purposes and should be modified for use in the desired production environment. The system leverages OpenAI's GPT-4 for generating responses and Pinecone for embedding storage and search.


### Install the dependencies:

```sh
pip install -r requirements.txt

### Running the Application

To start the FastAPI application:

```sh
python src/main.py


## API Endpoints

### `GET /`

Renders the HTML form for building and searching commercial property queries.

### `POST /build_query/`

Builds a query based on the user's input, creates an embedding, and stores it.

**Form data:**
- `building_type`: The type of building (e.g., "RESIDENTIAL", "COMMERCIAL", "INDUSTRIAL")
- `residential_type`: (Optional) Type of residential building
- `single_family_type`: (Optional) Type of single family building
- `apartment_type`: (Optional) Type of apartment building
- `location_type`: Location of the building (e.g., "CITY INFILL", "SUBURBS")

### `POST /search/`

Performs a semantic search based on the stored query embedding and returns the results.
