from datetime import datetime, timedelta
class FlightData:
    def __init__(self):
        self.origin_city_iata_code = ""
        self.destination_city_iata_code = "LON"
        self.from_date = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        self.to_date = (datetime.now() + timedelta(days=180)).strftime("%d/%m/%Y")
        self.nights_in_dst_from = 7
        self.nights_in_dst_to = 28
        self.flight_type = "round"
        self.one_for_city = 1
        self.max_stopovers = 0
        self.curr = "GBP"
