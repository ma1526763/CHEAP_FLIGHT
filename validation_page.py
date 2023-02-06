import re
import requests
from tkinter import messagebox
import json

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def check_valid_data(first_name, last_name, email):
    if not first_name.isalpha() or not last_name.isalpha():
        messagebox.showerror(title="Invalid name", message="Please enter a valid name!")
        return False
    if not re.fullmatch(regex, email) or email[-9:] not in ['gmail.com', 'yahoo.com']:
        messagebox.showerror(title="Invalid Email", message="Please enter valid mail")
        return False
    return [first_name, last_name, email.lower()]
def check_valid_cities(from_city, to_city):
    if not from_city.isalpha():
        messagebox.showerror(title="Invalid Origin City", message="Please enter a valid origin city name!")
    elif not to_city.isalpha():
        messagebox.showerror(title="Invalid Destination City", message="Please enter a valid destination city name!")
    else:
        return [from_city, to_city]

def check_user_file_exist():
    try:
        with open("user_data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="File not exist", message="\"user_data.json\" file does not exist.")
        return False
    except json.decoder.JSONDecodeError:
        messagebox.showerror(title="Empty file", message="No user in \"user_data.json\".")
        return False
    else:
        return data
def internet():
    try:
        requests.get("https://api.tequila.kiwi.com/locations/query")
    except requests.exceptions.ConnectionError:
        messagebox.showerror(title="No internet Connection", message="Please check your internet connection!!")
        return False
    else:
        return True

