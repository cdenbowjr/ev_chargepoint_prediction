import pandas as pd
import requests


def generate_random_location(dataframe, england_only=True):
    assert isinstance(dataframe, pd.DataFrame)
    try:
        random_postcode_api = "http://api.postcodes.io/random/postcodes"
        if england_only:
            random_postcode_request = requests.get(random_postcode_api).json()['result']
            while random_postcode_request['country'] != 'England':
                random_postcode_request = requests.get(random_postcode_api).json()['result']
        else:
            random_postcode_request = requests.get(random_postcode_api).json()['result']

        postcode = random_postcode_request['postcode']
        msoa_nm = random_postcode_request['msoa']
        admin_district = dataframe[dataframe.msoa11nm == msoa_nm]['lad13nm'].values[0]

        return postcode, admin_district

    except KeyError:
        print("Dataframe does not contain necessary msoa column")
