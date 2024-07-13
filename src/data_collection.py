from datetime import datetime
import pandas as pd
import requests
import json
import time
import logging
import config

logging.basicConfig(level=logging.INFO)

def extract_listing(
    listing_type,
    rapid_api_key,
    rapid_api_host,
    latitudeMin,
    latitudeMax,
    longitudeMin,
    longitudeMax,
    current_page_number=1,
    records_per_page=1000,
    sort_order="A",
    sort_by="1",
    culture_id="1",
    number_of_days="0",
    bed_range="0-0",
    bath_range="0-0",
    rent_min="0",
):
    """
        Extract residential listings from the API.

    Parameters
    ----------
    rapid_api_key: str, rapid api key
    rapid_api_host: str, rapid api host
    latitudeMin: str, minimum latitude
    latitudeMax: str, maximum latitude
    longitudeMin: str, minimum longitude
    longitudeMax: str, maximum longitude
    current_page_number: int, current page number
    records_per_page: int, records per page
    sort_order: str, sort order
    sort_by: str, sort by
    culture_id: str, culture id
    number_of_days: str, number of days
    bed_range: str, bed range
    bath_range: str, bath range
    rent_min: str, minimum rent

    Returns
    -------
    [json]: json data from the api

    """
    if listing_type == config.listings_type[0]:
        url = "https://{0}/properties/list-residential".format(rapid_api_host)
    else:
        url = "https://{0}/properties/list-commercial".format(rapid_api_host)
    
    print("URL: ", url)

    querystring = {
        "LatitudeMax": latitudeMax,
        "LatitudeMin": latitudeMin,
        "LongitudeMax": longitudeMax,
        "LongitudeMin": longitudeMin,
        "CurrentPage": current_page_number,
        "RecordsPerPage": records_per_page,
        "SortOrder": sort_order,
        "SortBy": sort_by,
        "CultureId": culture_id,
        "NumberOfDays": number_of_days,
        "BedRange": bed_range,
        "BathRange": bath_range,
        "RentMin": rent_min,
    }

    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": rapid_api_host,
    }

    response = requests.get(url, headers=headers, params=querystring)

    # print(response.json())

    # dump the json data
    data = response.json()

    # return the data
    return data


def collect_data():
    """
    Main function to collect data from the Realtor API.
    """
    logging.info("Collecting data from Realtor API")
    # get latitude and longitude bounding box - Edmonton as an example
    ll_bounding_box = {
        "latitudeMin": 53.432327,
        "latitudeMax": 53.655528,
        "longitudeMin": -113.666251,
        "longitudeMax": -113.334862,
    }

    for lstype in config.listings_type:
        page = 1
        while True:
            json_data = extract_listing(
                listing_type=lstype,
                rapid_api_key=config.RAPID_API_KEY,
                rapid_api_host=config.RAPID_API_HOST,
                latitudeMin=ll_bounding_box["latitudeMin"],
                latitudeMax=ll_bounding_box["latitudeMax"],
                longitudeMin=ll_bounding_box["longitudeMin"],
                longitudeMax=ll_bounding_box["longitudeMax"],
                current_page_number=page,
                records_per_page=50,
            )

            # check if there are any listings
            if len(json_data["Results"]) == 0:
                break
            else:
                # dump the json data
                json.dump(
                    json_data,
                    open(
                        "data/realtor_ca_data/{0}/listings_{1}.json".format(
                            lstype, page
                        ),
                        "w",
                    ),
                )
            page += 1

            # sleep for 1 second
            time.sleep(1)
    logging.info("Data collection complete")


if __name__ == "__main__":
    collect_data()
