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
SHEET = 'Bjj-Manager'


def welcome():
    clear()
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
            group = input("Enter participant's group (B:Beginner/A:Advanced): ")
            payment_confirmed = input("Has the payment been confirmed? (Y/N): ").lower() == "y"
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
            print("\n")
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
            print('If you want to leave the about you have to press "E"')


def clear():
    """
    Clear screen during game
    """
    os.system("clear")


# Function to add a participant to the list and spreadsheet
def add_participant(name, group, payment_confirmed_input):
    current_month = datetime.now().strftime("%B-%Y")

    # Check if the spreadsheet for the current month already exists
    spreadsheet = GSPREAD_CLIENT.open('Bjj-Manager')

    # Check if the worksheet for the current month already exists
    worksheet_title = current_month
    worksheets = spreadsheet.worksheets()
    worksheet = None

    for sheet in worksheets:
        if sheet.title == worksheet_title:
            worksheet = sheet
            break

    if worksheet is None:
        # Create a new worksheet for the current month
        worksheet = spreadsheet.add_worksheet(title=worksheet_title, rows="100", cols="3")

        # Set column headers
        headers = ["Name", "Group", "Payment Confirmed"]
        worksheet.append_row(headers)

        # Set column width
        column_widths = [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": worksheet.id,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": 1
                    },
                    "properties": {
                        "pixelSize": 20
                    },
                    "fields": "pixelSize"
                }
            }
        ]
        spreadsheet.batch_update({"requests": column_widths})

    # Check if the participant limit has been exceeded
    if len(worksheet.get_all_values()) > 20:
        print("Participant limit exceeded!")
        return

    # Map user input for group
    group_mapping = {"a": "Advanced", "b": "Beginner"}
    group = group_mapping.get(group.lower(), "")

    # Map user input for payment confirmation
    payment_confirmation_mapping = {True: "Yes", False: "No"}
    payment_confirmed = payment_confirmation_mapping.get(
        payment_confirmed_input, "")

    # Add the participant to the list
    participant_info = [name, group, payment_confirmed]
    worksheet.append_row(participant_info)
    print("Participant added!")


# Function to remove a participant from the list
def remove_participant(name):
    current_month = datetime.now().strftime("%B-%Y")

    # Check if the worksheet for the current month already exists
    worksheet_title = current_month
    worksheets = GSPREAD_CLIENT.open('Bjj-Manager').worksheets()
    worksheet = None

    for sheet in worksheets:
        if sheet.title == worksheet_title:
            worksheet = sheet
            break

    if worksheet is not None:
        # Find the participant in the worksheet
        participants = worksheet.get_all_records()
        for participant in participants:
            if participant['Name'].lower() == name.lower():
                worksheet.delete_row(participants.index(participant) + 2)  # +2 because indexes are shifted by the header and 0-based indexing
                print("Participant removed!")
                return

    print("Participant with the given name not found.")


# Function to confirm participant's payment
def confirm_payment(name):
    current_month = datetime.now().strftime("%B-%Y")
    spreadsheet = GSPREAD_CLIENT.open('Bjj-Manager')

    # Check if the worksheet for the current month already exists
    worksheet_title = current_month
    worksheets = spreadsheet.worksheets()
    worksheet = None

    for sheet in worksheets:
        if sheet.title == worksheet_title:
            worksheet = sheet
            break

    if worksheet is not None:
        # Find the participant in the worksheet
        participants = worksheet.get_all_records()
        for participant in participants:
            if participant['Name'] == name:
                participant['Payment Confirmed'] = True
                index = participants.index(participant) + 2  # +2 because indexes are shifted by the header and 0-based indexing
                cell = worksheet.cell(index, 3)  # 3 - index of the "Payment Confirmed" column
                cell.value = "Yes"
                worksheet.update_cell(cell.row, cell.col, cell.value)
                print("Participant's payment confirmed!")
                return

        print("Participant with the given name not found.")
    else:
        print("Worksheet for the current month doesn't exist. Please add participants first.")


def main():
    welcome()


main()