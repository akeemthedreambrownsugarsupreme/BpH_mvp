import numpy as np
import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_embeddings(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding


def build_query_embedding(
    building_type, residential_type, single_family_type, apartment_type, location_type
):
    if building_type == "RESIDENTIAL":
        if residential_type == "Single Family (Attached or semi detached)":
            final_choice = f"{building_type}, {residential_type}, {single_family_type}"
        elif residential_type == "Apartments":
            final_choice = (
                f"{building_type}, {residential_type}, {apartment_type} Apartments"
            )
        else:
            final_choice = f"{building_type}"
    else:
        final_choice = f"{building_type}"

    final_choice += f", {location_type}"

    embed = create_embeddings(final_choice)
    return final_choice, embed


def save_embedding(output_file_path, final_choice, embed):
    np.savez(output_file_path, query=final_choice, embedding=embed)
