import pandas as pd
import numpy as np
from shapely.geometry import MultiPolygon, Point
from shapely.wkt import loads as load_wkt
import json
import os
from config import logger

# Function to check if a point lies within a multipolygon
def is_point_in_multipolygon(zonal_data, lat, lon):
    point = Point(lon, lat)  # Note: Shapely uses (lon, lat) order
    for _, row in zonal_data.iterrows():
        multipolygon_wkt = row["geometry_multipolygon"]
        multipolygon = load_wkt(multipolygon_wkt)
        if multipolygon.contains(point):
            # return as row as json
            return row.to_dict()
    return {}


def update_zoning(zonal_data, listing_type):
    all_listings = []
    for file in os.listdir(f"data/realtor_ca_data/{listing_type}/"):
        with open(f"data/realtor_ca_data/{listing_type}/" + file) as f:
            data = json.load(f)
            listings = data["Results"]

            for listing in listings:
                lat = listing["Property"]["Address"]["Latitude"]
                lon = listing["Property"]["Address"]["Longitude"]

                # Find the zoning for the listing
                zone = is_point_in_multipolygon(zonal_data, lat, lon)
                listing["zone"] = zone
                listing["listing_type"] = listing_type
                extracted_info = extract_listing_info(listing, listing_type)
                all_listings.append(extracted_info)
    return pd.DataFrame(all_listings)


def extract_listing_info(listing, listing_type):
    # Extract the necessary fields from the listing, handling missing values
    if listing_type == "residential":
        return {
            "price": listing["Property"].get("Price", ""),
            "type": listing["Property"].get("Type", ""),
            "address": listing["Property"]["Address"].get("AddressText", ""),
            "latitude": listing["Property"]["Address"].get("Latitude", ""),
            "longitude": listing["Property"]["Address"].get("Longitude", ""),
            "zone": [
                {
                    "code": listing["zone"].get("zoning", "") if "zone" in listing else "",
                    "description": (
                        listing["zone"].get("description", "") if "zone" in listing else ""
                    ),
                }
            ],
            "photos": [
                photo.get("HighResPath", "")
                for photo in listing["Property"].get("Photo", [])
            ],
            "parking": [
                parking.get("Name", "")
                for parking in listing["Property"].get("Parking", [])
            ],
            "amenities_nearby": (
                listing["Property"].get("AmmenitiesNearBy", "").split(", ")
                if listing["Property"].get("AmmenitiesNearBy")
                else []
            ),
            "bedrooms": listing["Building"].get("Bedrooms", ""),
            "bathrooms": listing["Building"].get("BathroomTotal", ""),
            "size_interior": listing["Building"].get("SizeInterior", ""),
            "ownership_type": listing["Property"].get("OwnershipType", ""),
            "public_remarks": listing.get("PublicRemarks", ""),
            "postal_code": listing.get("PostalCode", ""),
            "additional_features": listing.get("AdditionalFeatures", []),
            "listing_type": listing_type,
        }
    elif listing_type == "commercial":
        return {
            "address": listing["Property"]["Address"].get("AddressText", ""),
            "latitude": listing["Property"]["Address"].get("Latitude", ""),
            "longitude": listing["Property"]["Address"].get("Longitude", ""),
            "zone": [
                {
                    "code": listing["zone"].get("zoning", "") if "zone" in listing else "",
                    "description": (
                        listing["zone"].get("description", "") if "zone" in listing else ""
                    ),
                }
            ],
            "photos": [
                photo.get("HighResPath", "")
                for photo in listing["Property"].get("Photo", [])
            ],
            "ownership_type": listing["Property"].get("OwnershipType", ""),
            "public_remarks": listing.get("PublicRemarks", ""),
            "land": listing["Land"].get("SizeTotal", ""),
            "services": listing["Business"].get("Services", ""),
            "amenities_nearby": (
                listing["Property"].get("AmmenitiesNearBy", "").split(", ")
                if listing["Property"].get("AmmenitiesNearBy")
                else []
            ),
            "listing_type": listing_type,
        }
    else:
        raise ValueError("Invalid listing type")


def preprocess_data():
    """
    Main function to preprocess the data.
    """
    logger.info("Preprocessing data")
    # read the zonal data
    zonal_data = pd.read_csv("data/Zoning_Bylaw_Geographical_Data_20240528.csv")

    df_residential = update_zoning(zonal_data, "residential")
    df_commercial = update_zoning(zonal_data, "commercial")
    # df_all = pd.concat([df_residential, df_commercial], ignore_index=True)

    # save the data to a csv file
    df_residential.to_csv("data/realtor_ca_data/residential_listings.csv", index=False)
    df_commercial.to_csv("data/realtor_ca_data/commercial_listings.csv", index=False)
    # save the data to a json file
    df_residential.to_json("data/realtor_ca_data/residential_listings.json", orient="records")
    df_commercial.to_json("data/realtor_ca_data/commercial_listings.json", orient="records")

    logger.info("Data preprocessing complete")

if __name__ == "__main__":
    preprocess_data()
