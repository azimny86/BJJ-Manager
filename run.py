from datetime import datetime
import os
import gspread
from google.oauth2.service_account import Credentials

# Configuration of access to Google Sheets
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Spread sheet name
SHEET = GSPREAD_CLIENT.open('Bjj-Manager')


def welcome():
    while True:
        print("==== BJJ Manager ====")
        print("1. Add participant")
        print("2. Remove participant")
        print("3. Confirm payment")
        print("9. About program")
        print("Q. Exit the program")
        print("=====================")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter participant's name: ")
            group = input("Enter participant's group (Beginner/Advanced): ")
            payment_confirmed = input("Has the payment been confirmed? (Yes/No): ").lower() == "yes"
            add_participant(name, group, payment_confirmed)
        elif choice == "2":
            name = input("Enter participant's name to remove: ")
            remove_participant(name)
        elif choice == "3":
            name = input("Enter participant's name to confirm payment: ")
            confirm_payment(name)
        elif choice == "9":
            about()
        elif choice == "q":
            exit()
        else:
            print("Invalid option.")

    print("Thank you for using BJJ Manager!")




def clear():
    """
    Clear screen during game
    """
    os.system("clear")


def main():
    welcome()


main()