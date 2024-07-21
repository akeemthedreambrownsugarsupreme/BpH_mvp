import os
import numpy as np
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pinecone = Pinecone(os.getenv("PINECONE_API_CODE"))
index = pinecone.Index(os.getenv("INDEX_NAME"))


# Define the function to create embeddings
def create_embeddings(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding


def main(output_file_path):
    # Hierarchical user input
    # Define the mapping of user input to building types
    build_options = {"1": "RESIDENTIAL", "2": "COMMERCIAL", "3": "INDUSTRIAL"}

    # Prompt the user for the main building type
    user_input = input(
        "What do you want to build?\n1. RESIDENTIAL\n2. COMMERCIAL\n3. INDUSTRIAL\n"
    )

    # Check if the user input is valid and save the building type
    if user_input in build_options:
        building_type = build_options[user_input]

        if building_type == "RESIDENTIAL":
            # Prompt for the type of residential building
            residential_options = {
                "1": "Single Family (Attached or semi detached)",
                "2": "Apartments",
            }
            residential_input = input(
                "\tWHAT KIND OF RESIDENTIAL BUILDING?\n"
                "\t1. Single Family (Attached or semi detached)\n"
                "\t2. Apartments\n"
            )
            if residential_input in residential_options:
                residential_type = residential_options[residential_input]

                if residential_type == "Single Family (Attached or semi detached)":
                    # Prompt for the type of single family building
                    single_family_options = {"1": "Duplex", "2": "Row Houses"}
                    single_family_input = input(
                        "\t\tSingle Family (Attached or semi detached):\n"
                        "\t\t1. Duplex\n"
                        "\t\t2. Row Houses\n"
                    )
                    if single_family_input in single_family_options:
                        single_family_type = single_family_options[single_family_input]
                        final_choice = (
                            f"{building_type}, {residential_type}, {single_family_type}"
                        )

                elif residential_type == "Apartments":
                    # Prompt for the type of apartments
                    apartment_options = {"1": "Low", "2": "Medium", "3": "High"}
                    apartment_input = input(
                        "\t\tApartments:\n"
                        "\t\t1. Low\n"
                        "\t\t2. Medium\n"
                        "\t\t3. High\n"
                    )
                    if apartment_input in apartment_options:
                        apartment_type = apartment_options[apartment_input]
                        final_choice = f"{building_type}, {residential_type}, {apartment_type} Apartments"

    else:
        final_choice = "Invalid choice. Please select a valid option."

    # Asking for the location
    location_options = {"1": "CITY INFILL", "2": "SUBURBS"}

    location_input = input(
        "\tWHERE DO YOU WANT TO BUILD?\n\t1. CITY INFILL\n\t2. SUBURBS\n"
    )

    if location_input in location_options:
        location_type = location_options[location_input]
        final_choice += f", {location_type}"
    else:
        final_choice = "Invalid choice. Please select 1 or 2."

    # Create the embedding for the final choice
    embed = create_embeddings(final_choice)
    print("The embedding is completed!")

    # Save the original query and the embedding
    np.savez(output_file_path, query=final_choice, embedding=embed)
    print("Query and embedding saved!")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(current_dir, "../data/query_embedding.npz")
    main(output_file_path)
