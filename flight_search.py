import requests
import os

TEQUILA_API_KEY = os.environ['T_API_KEY']
TEQUILA_LOCATION_ENDPOINT = "https://api.tequila.kiwi.com/locations/query"
TEQUILA_SEARCH_ENDPOINT = f"https://api.tequila.kiwi.com/v2/search"

tequila_header = {
    "apikey": TEQUILA_API_KEY,
}

class FlightSearch:
    def __init__(self):
        self.iata_code = ""
        self.flight_data = ""
        self.max_stopper_overs = 0
        self.flight_link = ""
        self.check_max_stop_overs = 1

    def get_iata_code(self, city_name):
        search_iata_params = {
            "term": city_name,
            "location_types": "city"
        }
        try:
            self.iata_code = requests.get(TEQUILA_LOCATION_ENDPOINT, params=search_iata_params,
                                          headers=tequila_header).json()['locations'][0]['code']
        except IndexError:
            self.iata_code = ""

    def search_flight(self, origin_city_iata_code, destination_city_iata_code, from_date, to_date, nights_in_dst_from,
                      nights_in_dst_to, flight_type, one_for_city, max_stopovers, curr):
        self.max_stopper_overs = max_stopovers
        print(origin_city_iata_code, max_stopovers)
        flight_search_params = {
            "fly_from": origin_city_iata_code,
            "fly_to": destination_city_iata_code,
            "date_from": from_date,
            "date_to": to_date,
            "nights_in_dst_from": nights_in_dst_from,
            "nights_in_dst_to": nights_in_dst_to,
            "flight_type": flight_type,
            "one_for_city": one_for_city,
            "max_stopovers": max_stopovers,
            "curr": curr
        }
        try:
            self.flight_data = requests.get(url=TEQUILA_SEARCH_ENDPOINT, params=flight_search_params,
                                            headers=tequila_header).json()['data']
        except KeyError:
            print(f"No flights available")
            self.flight_data = ""
        else:
            # this will check if not direct flight then try to find flight with stops.
            if not self.flight_data and max_stopovers < self.check_max_stop_overs:
                self.max_stopper_overs += 1
                self.search_flight(origin_city_iata_code, destination_city_iata_code, from_date, to_date,
                                   nights_in_dst_from,
                                   nights_in_dst_to, flight_type, one_for_city, self.max_stopper_overs, curr)
