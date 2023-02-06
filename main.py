from data_manager import DataManager, update_sheet_data
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
from tkinter import *
from validation_page import check_valid_data, internet
from datetime import datetime, timedelta
from second_gui import SecondGui
import webbrowser

d_manager = DataManager()

f_search = FlightSearch()
f_data = FlightData()
notification = NotificationManager()
f_data.destination_city_iata_code = "LON"

if internet():
    d_manager.get_sheet_data()
    # GET IATA CODE FOR CITY
    for row in d_manager.sheet_data:
        if not row['iataCode']:
            f_search.get_iata_code(row['city'])
            update_sheet_data(f_search.iata_code, row['id'])

def start_searching_flight(user_data, cheap_6_month_flights=False, tour_flights=False):
    f_data.one_for_city = 0 if cheap_6_month_flights else 1
    f_search.check_max_stop_overs = 6 if tour_flights else 1
    message = ""
    # city_prices = {"DPS": 1000, "DADA": 100, "PAR": 200, "BER": 42, "TYO": 485, "SYD": 551, "IST": 95, "KUL": 414,
    #                "NYC": 240, "SFO": 260, "CPT": 378, }
    for sheet_row in d_manager.sheet_data:
        f_search.search_flight(origin_city_iata_code=sheet_row['iataCode'], destination_city_iata_code=f_data.destination_city_iata_code,
                               from_date=f_data.from_date, to_date=f_data.to_date, flight_type=f_data.flight_type,
                               nights_in_dst_from=f_data.nights_in_dst_from, nights_in_dst_to=f_data.nights_in_dst_to,
                               one_for_city=f_data.one_for_city, max_stopovers=f_data.max_stopovers, curr=f_data.curr)

        for flight in f_search.flight_data:
            if flight['price'] <= sheet_row['lowestPrice'] or tour_flights:
                route = flight['route'][0]
                departure_date = flight['route'][0]['local_departure'].split('T')[0]
                return_date = flight['route'][1]['local_departure'].split('T')[0]
                flight_information = f"🌐Low Price Alert!✈ {flight['cityFrom']}({flight['cityCodeFrom']})-{flight['cityTo']}" \
                                     f"({flight['cityCodeTo']})available.\nFlight# {route['flight_no']}" \
                                     f"\nAirline: {flight['airlines'][0]}\nPrice: £{flight['price']}" \
                                     f"\nNights Stay: {flight['nightsInDest']}\nDeparture Date: {departure_date}\n"

                stopover_city = ""
                if f_search.max_stopper_overs > 0:
                    d = departure_date.split('-')
                    return_date = (datetime(year=int(d[0]), month=int(d[1]), day=int(d[2])) + timedelta(
                        days=flight['nightsInDest'])).strftime('%Y-%m-%d')
                    flight_information += f"Return Date: {return_date}\n"
                    route = flight['route'][0]
                    stopover_city = f"\nFlight has 1 stopover via {route['cityTo']}({route['cityCodeTo']}) city." \
                                    f"Flight# {route['flight_no']} at airline {route['airline']}\n"
                else:
                    flight_information += f"Return Date: {return_date}\n"
                flight_link = f"https://www.google.com/travel/flights?q=Flights%20to%20{''.join(flight['cityTo'].split())}%20from%20" \
                              f"{''.join(flight['cityFrom'].split())}%20on%20{departure_date}%20through%20{return_date}\n\n"
                message += f"{flight_information}{stopover_city}{flight_link}\n"
    notification.send_mail(message, user_data)
    clear_screen()

def clear_screen():
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    email_entry.delete(0, END)
    first_name_entry.focus()

def get_user_data():
    if internet():
        return check_valid_data(first_name=first_name_entry.get(),
                                last_name=last_name_entry.get(),
                                email=email_entry.get())

def first_available_flight():
    user_data = get_user_data()
    if user_data:
        start_searching_flight(user_data)

def cheap_flights_in_6_months():
    user_data = get_user_data()
    if user_data:
        start_searching_flight(user_data, cheap_6_month_flights=True)

def tour_flight_prices():
    user_data = get_user_data()
    if user_data:
        start_searching_flight(user_data, tour_flights=True)

def send_mails_to_all():
    if internet():
        start_searching_flight("")

def go_to_second_gui():
    SecondGui(window)
def view_records():
    if internet():
        webbrowser.open(
            url="https://docs.google.com/spreadsheets/d/1aOCCi9TUd7r5V9J6pujreJEVDtHSO3wBUWhWEZ9Gmuo/edit#gid=0", new=1)

################# GUI #################
window = Tk()
window.title("Cheap Flight")
window.geometry("1300x700+0+0")
window.resizable(False, False)
canvas = Canvas(width=1300, height=700)
canvas.place(x=0, y=0)

img = PhotoImage(file="img.png")
canvas.create_image(650, 350, image=img)
COLOR_2 = "#6fba2a"
COLOR_3 = "#da65b4"
COLOR_4 = "#735a9b"
COLOR_1 = "#30babc"

company_label = Label(text="ALI FLIGHT CLUB", font=("Arial", 50, "bold"), foreground="gold")
company_label.place(x=360, y=10)
# First Name
first_label = Label(text="First Name", background=COLOR_1, foreground="white", font=("Arial", 22, "bold"))
first_label.place(x=300, y=250)
first_name_entry = Entry(width=10, font=("Arial", 22), highlightthickness=2, highlightbackground=COLOR_1,
                         highlightcolor=COLOR_1)
first_name_entry.grid(row=0, column=1, padx=200, pady=20)
first_name_entry.place(x=462, y=250)
first_name_entry.focus()
# Last Name
last_label = Label(text="Last Name", background=COLOR_1, foreground="white", font=("Arial", 22, "bold"))
last_label.place(x=637, y=250)
last_name_entry = Entry(width=10, font=("Arial", 22), highlightthickness=2, highlightbackground=COLOR_1,
                        highlightcolor=COLOR_1)
last_name_entry.place(x=797, y=250)
# Email
email_label = Label(text="Your Email", background=COLOR_1, foreground="white", font=("Arial", 22, "bold"))
email_label.place(x=300, y=310)
email_entry = Entry(width=31, font=("Arial", 22), highlightthickness=2, highlightbackground=COLOR_1,
                    highlightcolor=COLOR_1)
email_entry.place(x=462, y=310)

# BUTTONS
cheap_flights_button = Button(text="CHEAP TOUR FLIGHTS", background=COLOR_2, foreground="white",
                              font=("Arial", 15, "bold"), command=first_available_flight)
cheap_flights_button.place(x=300, y=370, width=325)
cheap_flights_in_6_month_button = Button(text="CHEAP FLIGHTS IN 6 MONTHS", background=COLOR_4, foreground="white",
                                         font=("Arial", 15, "bold",), command=cheap_flights_in_6_months)
cheap_flights_in_6_month_button.place(x=642, y=370, width=325)

check_flight_button = Button(text="TOUR FLIGHTS PRICES", background=COLOR_1, foreground="white",
                             font=("Arial", 15, "bold"), command=tour_flight_prices)
check_flight_button.place(x=300, y=430, width=325)
send_emails_to_all_customers_button = Button(text="SEND EMAILS TO ALL", background=COLOR_3, foreground="white",
                                             font=("Arial", 15, "bold"), command=send_mails_to_all)
send_emails_to_all_customers_button.place(x=642, y=430, width=325)

tour_destination_button = Button(text="SEARCH NEW FLIGHT", background="red", foreground="white",
                                 font=("Arial", 15, "bold"), command=go_to_second_gui)
tour_destination_button.place(x=300, y=490, width=325)
view_record_button = Button(text="TOUR RECORDS INFO", background="gold", foreground="white",
                            font=("Arial", 15, "bold"), command=view_records)
view_record_button.place(x=642, y=490, width=325)

window.mainloop()
