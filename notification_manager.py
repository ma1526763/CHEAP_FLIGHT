import json
import os
from email.message import EmailMessage
from smtplib import SMTP
from tkinter import messagebox
from validation_page import check_user_file_exist

class NotificationManager:
    def __init__(self):
        self.SENDER_MAIL = os.environ['SENDER_MAIL']
        self.Password = os.environ['PASSWORD']

    def send_mail(self, message_to_send, new_user_data):
        if not new_user_data:
            data = check_user_file_exist()
            if data:
                for key in data:
                    self.send_email_to_user(data[key]['first_name'], data[key]['last_name'], key, message_to_send)
                messagebox.showinfo(title="Sent Successfully",
                                    message="Email has been sent successfully to all of our customers.")
        else:
            self.send_email_to_user(new_user_data[0], new_user_data[1], new_user_data[2], message_to_send)
            self.add_new_user_in_records(user_data=new_user_data)
            messagebox.showinfo(title="Sent Successfully",
                                message="Email has been sent successfully. Please Check your email")

    def send_email_to_user(self, first_name, last_name, email, message_to_send):
        message_to_user = f"Dear {first_name.title()} {last_name.title()}!\n" + message_to_send
        message = EmailMessage()
        message["Subject"] = "CHEAP FLIGHT INFO"
        message["From"] = self.SENDER_MAIL
        message["To"] = email
        message.set_content(message_to_user)

        with SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.SENDER_MAIL, password=self.Password)
            connection.send_message(message)

    @classmethod
    def add_new_user_in_records(cls, user_data):
        new_user_info = {
            user_data[2]: {
                "first_name": user_data[0],
                "last_name": user_data[1],
            }
        }
        try:
            with open("user_data.json", "r+") as file:
                data = json.load(file)
                for email in data:
                    if email == user_data[2]:
                        return
                data[user_data[2]] = {
                    "first_name": user_data[0],
                    "last_name": user_data[1],
                }
                file.seek(0)
                json.dump(data, file, indent=4)

        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("user_data.json", "w") as file:
                json.dump(new_user_info, file, indent=4)
