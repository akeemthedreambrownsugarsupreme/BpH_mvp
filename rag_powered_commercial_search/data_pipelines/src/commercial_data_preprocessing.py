import pandas as pd
import os


def preprocess_commercial_data(input_file, output_file):
    df = pd.read_csv(input_file)
    
    # Preprocess to get the commercial data
    df_commercial = df[df["listing_type"] == "commercial"]
    print(len(df_commercial))

    # Extract and clean the required columns
    df_commercial["address"] = df_commercial["address"].apply(
        lambda x: x.split("|")[0]
    )  # Remove postal code from address

    # Create a new DataFrame with the required columns
    new_df_commercial = df_commercial[
        [
            "address",
            "postal_code",
            "latitude",
            "longitude",
            "zone",
            "photos",
            "size_interior",
            "amenities_nearby",
            "public_remarks",
        ]
    ]

    # Rename columns for clarity
    new_df_commercial.columns = [
        "Address",
        "Postal Code",
        "Latitude",
        "Longitude",
        "Zone",
        "Photo",
        "Size of Property",
        "Nearby Amenities",
        "Public Remark",
    ]

    # Assume "services" means checking for 'Playground' and 'Public Transit' in amenities_nearby (as an example)
    new_df_commercial["Services"] = new_df_commercial["Nearby Amenities"].apply(
        lambda x: (
            "Water, Electricity" if "Playground" in x and "Public Transit" in x else ""
        )
    )

    # Save the cleaned data to a new CSV file
    new_df_commercial.to_csv(output_file, index=False)

    print("CSV file has been processed and saved successfully.")


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(current_dir, "../data/features.csv")
    output_file_path = os.path.join(current_dir, "../data/commercial_data.csv")
    preprocess_commercial_data(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
