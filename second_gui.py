from tkinter import *
from tkinter import messagebox
from validation_page import check_valid_cities, internet
from flight_search import FlightSearch
from flight_data import FlightData
import webbrowser

COLOR_2 = "#6fba2a"
COLOR_3 = "#da65b4"
COLOR_4 = "#735a9b"
COLOR_1 = "#30babc"

f_search = FlightSearch()
f_data = FlightData()


class SecondGui:
    def __init__(self, window):
        window.iconify()
        self.origin_city = ""
        self.destination_city = ""
        self.flight_link = ""
        self.new_window = Toplevel(window)
        self.new_window.title("Search Flight")
        self.new_window.geometry("1300x700+0+0")
        self.new_window.resizable(False, False)
        self.new_window.config(background=COLOR_1)

        new_company_label = Label(self.new_window, text="ALI FLIGHT CLUB", font=("Arial", 50, "bold"),
                                  background=COLOR_1,
                                  foreground=COLOR_4)
        new_company_label.place(x=360, y=10)

        from_label = Label(self.new_window, text="From 🔗", background=COLOR_2, foreground="white",
                           font=("Arial", 22, "bold"))
        from_label.place(x=365, y=250)
        self.from_entry = Entry(self.new_window, width=10, font=("Arial", 22), highlightthickness=2,
                                highlightbackground=COLOR_4,
                                highlightcolor=COLOR_4)
        self.from_entry.grid(row=0, column=1, padx=200, pady=20)
        self.from_entry.place(x=495, y=250)
        self.from_entry.focus()
        # Last Name
        to_label = Label(self.new_window, text="To 🎯", background=COLOR_2, foreground="white",
                         font=("Arial", 22, "bold"))
        to_label.place(x=672, y=250)
        self.to_entry = Entry(self.new_window, width=10, font=("Arial", 22), highlightthickness=2,
                              highlightbackground=COLOR_4,
                              highlightcolor=COLOR_4)
        self.to_entry.place(x=762, y=250)
        start_searching_button = Button(self.new_window, text="START SEARCHING", background="red", foreground="white",
                                        font=("Arial", 15, "bold"), command=self.get_valid_cities)
        start_searching_button.place(x=710, y=305, width=220)
        self.view_button = Button(self.new_window, text="VIEW FLIGHT DETAILS", background=COLOR_2, foreground="white",
                                  font=("Arial", 15, "bold"), state="disabled", command=self.view_flight_details)
        self.view_button.place(x=365, y=305, width=220)

    def get_valid_cities(self):
        if not internet():
            return
        cities = check_valid_cities(self.from_entry.get(), self.to_entry.get())
        if cities:
            self.origin_city = cities[0]
            self.destination_city = cities[1]
            f_search.get_iata_code(self.origin_city)
            if not f_search.iata_code:
                messagebox.showerror(title=f"Invalid City Name {self.origin_city}",
                                     message="Please enter a valid city name!")
                self.from_entry.delete(0, END)
            else:
                f_data.origin_city_iata_code = f_search.iata_code
                f_search.get_iata_code(self.destination_city)
                if not f_search.iata_code:
                    messagebox.showerror(title=f"Invalid City Name {self.destination_city}",
                                         message="Please enter a valid city name!")
                    self.to_entry.delete(0, END)
                else:
                    f_data.nights_in_dst_from = 0
                    f_data.nights_in_dst_to = 0
                    f_search.check_max_stop_overs = 5
                    f_data.destination_city_iata_code = f_search.iata_code
                    f_search.search_flight(origin_city_iata_code=f_data.origin_city_iata_code,
                                           destination_city_iata_code=f_data.destination_city_iata_code,
                                           from_date=f_data.from_date, to_date=f_data.to_date,
                                           flight_type=f_data.flight_type,
                                           nights_in_dst_from=f_data.nights_in_dst_from,
                                           nights_in_dst_to=f_data.nights_in_dst_to,
                                           one_for_city=f_data.one_for_city, max_stopovers=f_data.max_stopovers,
                                           curr=f_data.curr)
                    for flight in f_search.flight_data:
                        local_departure = flight['route'][0]['local_departure'].split('T')[0]
                        arrival = flight['route'][1]['local_arrival'].split('T')[0]
                        self.flight_link = f"https://www.google.com/travel/flights?q=Flights%20to%20{''.join(flight['cityTo'].split())}%20from%20" \
                                           f"{''.join(flight['cityFrom'].split())}%20on%20{local_departure}%20through%20{arrival}"
                        self.view_button.config(state="normal")
                    if not f_search.flight_data:
                        messagebox.showinfo(title="No Flight Found", message=f"No Flight Found from {self.from_entry.get()} to {self.to_entry.get()}")
                        self.clear_entries()

    def view_flight_details(self):
        webbrowser.open(self.flight_link, new=1)
        self.view_button.config(state="disabled")
        self.clear_entries()

    def clear_entries(self):
        self.from_entry.delete(0, END)
        self.to_entry.delete(0, END)
        self.from_entry.focus()