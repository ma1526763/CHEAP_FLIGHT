import requests
import os

SHEETY_ENDPOINT = "https://api.sheety.co/813216c1c7b89ca2bcd35e1ec6989347/cheapFlightDeal/prices"
sheety_baerer_header = {
    "Authorization": f"Bearer {os.environ['SHEET_BAERER_HEADER']}"
}

def update_sheet_data(city_iata_code, row_id):
    sheety_params = {
        "price": {
            "iataCode": city_iata_code,
        }
    }
    requests.put(f"{SHEETY_ENDPOINT}/{row_id}", json=sheety_params, headers=sheety_baerer_header)

class DataManager:
    def __init__(self):
        self.sheet_data = {}

    def get_sheet_data(self):
        self.sheet_data = requests.get(SHEETY_ENDPOINT, headers=sheety_baerer_header).json()['prices']
