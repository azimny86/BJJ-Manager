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


def about():
    clear()
    print("Welcome to BJJ Manager!")
    print("BJJ Manager is a powerful tool designed to manage your membrships in BJJ gym.")
    print("With this program, you can easily manage participant bookings, enforce class limits, and keep track of payments.")
    print("Here are some key features:")
    print("- Recording a members: Reserve your spot in BJJ training sessions by selecting the desired group (Beginner or Advanced).")
    print("- Class Limit: Each training session has a maximum capacity of 20 participants. If the limit is exceeded, you will be notified.")
    print("- Google Sheets Integration: The participant list will be automatically uploaded to a Google Sheets document for easy access and management.")
    print("- Payment Confirmation: To book a session, you must confirm your monthly payment. Only participants with confirmed payments can reserve a spot.")
    print("- Monthly Tracking: A new spreadsheet will be created for each month to keep your records organized.")
    print("- Removal of Participants: If needed, you can remove yourself from a booked session.")
    print("Enjoy the convenience and efficiency of BJJ Manager for managing your BJJ training sessions.")
    print("If you have any questions or need assistance, please don't hesitate to reach out to our support team.")
    print("==============================================")
    print("Press " + "E" + " to go back to the start menu")
    opt = False
    while not opt:
        settings = input("\n").lower()
        if settings == "e":
            opt = True
            clear()
            return welcome()
        else:
            print("\n")
            print('If you want to leave the rules you have to press "E"')


def clear():
    """
    Clear screen during game
    """
    os.system("clear")


def main():
    welcome()


main()