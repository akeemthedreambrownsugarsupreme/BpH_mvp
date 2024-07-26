import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from pinecone import Pinecone
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
Pinecone = Pinecone(os.getenv("PINECONE_API_KEY"))
index = Pinecone.Index(os.getenv("PINECONE_COMMERCIAL_INDEX_NAME"))


def load_query_and_embedding(file_path):
    data = np.load(file_path)
    query = data["query"].item()
    query_embedding = data["embedding"]
    return query, query_embedding


def perform_semantic_search(query_embedding):
    response = index.query(
        vector=query_embedding, top_k=3, include_metadata=True
    )
    return response


def extract_contexts(response):
    contexts = []
    for match in response["matches"]:
        metadata = match["metadata"]
        context = (
            f"Address: {metadata['Address']}\n"
            f"Latitude: {metadata['Latitude']}\n"
            f"Longitude: {metadata['Longitude']}\n"
            f"Nearby Amenities: {metadata['Nearby Amenities']}\n"
            # f"Photo: {metadata['Photo']}\n"
            f"Postal Code: {metadata['Postal Code']}\n"
            f"Public Remark: {metadata['Public Remark']}\n"
            f"Services: {metadata['Services']}\n"
            f"Size of Property: {metadata['Size of Property']}\n"
            f"Zone: {metadata['Zone']}"
        )
        contexts.append(context)
    return contexts


def create_prompt(query, contexts):
    prompt_start = (
        "You are an AI tasked with finding the best lots for building residential apartments."
        "The user has provided the following requirements: \n\n"
        "Based on these requirements, return an available lot that meet the criteria. "
        "Provide a recommendation_summary in English explaining why this lot is recommended.\n\n"
        "Only answer questions using the provided context. Do not provide any information that is not in the context and remove duplicates in choices if the latitude and longitude are the same. "
        "Provide the information in the following JSON format:\n"
        "{\n"
        "  \"recommendation_summary\": \"...\",\n"
        "  \"type\": \"...\",\n"
        "  \"price\": \"...\",\n"
        "  \"address\": \"...\",\n"
        "  \"latitude\": \"...\",\n"
        "  \"longitude\": \"...\",\n"
        "  \"photos\": [\"...\", \"...\"]\n"
        "  \"utilities\": [\"...\", \"...\"]\n"
        "}\n"
    )
    prompt_end = f"\n\nQuery: {query}\nAnswer:"
    prompt = prompt_start + "\n\n---\n\n".join(contexts) + prompt_end
    return prompt


def get_gpt4_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=1500,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0,
    )
    json_responses = []
    for choice in response.choices:
        try:
            json_responses.append(json.loads(choice.message.content))
        except:
            pass
    return json_responses