import os
from dotenv import load_dotenv
import pandas as pd
import openai

load_dotenv()


def create_embeddings(text, client):
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding


def main():
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    csv_file_path = os.path.join("rag_powered_commercial_search/data_pipelines/data", "commercial_data.csv")
    df = pd.read_csv(csv_file_path)

    # Combine all columns into one text string per row
    df["combined_text"] = df.astype(str).agg(" ".join, axis=1)

    # Generate embeddings for each combined text record
    df["embeddings"] = df["combined_text"].apply(lambda x: create_embeddings(x, client))

    # Save the DataFrame with embeddings to a new CSV file
    output_csv_file_path = os.path.join("rag_powered_commercial_search/data_pipelines/data", "commercial_data_with_embeddings.csv")
    df.to_csv(output_csv_file_path, index=False)

    print(f"Embeddings saved to {output_csv_file_path}")


if __name__ == "__main__":
    main()
