# Data Pipelines

This folder contains scripts for processing and managing commercial property data using a Retrieval-Augmented Generation (RAG) based Large Language Model (LLM). Below are the descriptions and usage instructions for each script.


## Usage

Preprocess the commercial data:

```sh
python pipelines/commercial_data_preprocessing.py
```

Create embeddings for the processed data:

```sh
python pipelines/create_data_embeddings.py
```

Upsert the embeddings into Pinecone:

```sh
python pipelines/pinecone_upserting.py
```

Build a query and create an embedding for it:

```sh
python pipelines/build_query_embedding.py
```

Perform a semantic search based on the query embedding:

```sh
python pipelines/perform_semantic_search.py
```