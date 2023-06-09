from datetime import datetime
import os
import gspread
import sys
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
        print("4. Display members for this month")
        print("9. About program")
        print("Q. Exit the program")
        print("=====================")
        choice = input("Choose an option:\n ")

        if choice == "1":
            name = input("Enter participant's name:\n ")
            group = input(
                "Enter participant's group (B:Beginner/A:Advanced):\n ")
            payment_confirmed = input(
                "Has the payment been confirmed? (Y/N):\n ").lower() == "y"
            add_participant(name, group, payment_confirmed)
        elif choice == "2":
            name = input("Enter participant's name to remove:\n ")
            remove_participant(name)
        elif choice == "3":
            name = input("Enter participant's name to confirm payment:\n ")
            confirm_payment(name)
        elif choice == "4":
            display_members()
        elif choice == "9":
            about()
        elif choice == "q":
            sys.exit(0)
        else:
            print("\n")
            print("Invalid option.")

    print("Thank you for using BJJ Manager!")


def about():
    clear()
    print("Welcome to BJJ Manager! \n BJJ Manager is a powerful tool designed to manage your membrships in BJJ gym.\n With this program, you can easily manage participant membership, enforce class limits, and keep track of payments. Here are some key features:\n- Recording a members: Reserve your spot in BJJ training sessions by selecting the desired group (Beginner or Advanced).\n- Class Limit: Each training session has a maximum capacity of 20 participants. If the limit is exceeded, you will be notified.\n- Google Sheets Integration: The participant list will be automatically uploaded to a Google Sheets document for easy access and management.\n- Payment Confirmation: To book a session, you must confirm your monthly payment. Only participants with confirmed payments can reserve a spot.\n- Monthly Tracking: A new spreadsheet will be created for each month to keep your records organized.\n- Removal of Participants: If needed, you can remove yourself from a booked session.\nEnjoy the convenience and efficiency of BJJ Manager for managing your BJJ training sessions.\nIf you have any questions or need assistance, please don't hesitate to reach out to our support team.\n")
    
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
        worksheet = spreadsheet.add_worksheet(
            title=worksheet_title, rows="100", cols="3")

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

    # Convert boolean input to string
    payment_confirmed = "Yes" if payment_confirmed_input else "No"

    # Add the participant to the list
    participant_info = [name, group, payment_confirmed]
    worksheet.append_row(participant_info)
    print("\nParticipant added!\n")


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
                # +2 because indexes are shifted by the header and 0- indexing
                worksheet.delete_row(participants.index(participant) + 2)
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
            # +2 because indexes are shifted by the header and 0-based indexing
                index = participants.index(participant) + 2
            # 3 - index of the "Payment Confirmed" column
                cell = worksheet.cell(index, 3)
                cell.value = "Yes"
                worksheet.update_cell(cell.row, cell.col, cell.value)
                print("Participant's payment confirmed!")
                return

        print("Participant with the given name not found.")
    else:
        print("Worksheet for the current month doesn't exist. \
             Please add participants first.")


# Function to display members for the current month
def display_members():
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
        # Get all participants' information
        participants = worksheet.get_all_records()

        if not participants:
            print("No participants found for the current month.")
        else:
            print(f"Members for {current_month}:\n")
            for participant in participants:
                name = participant['Name']
                group = participant['Group']
                payment_confirmed = participant['Payment Confirmed']
                payment_status = "Paid" if payment_confirmed.lower() == "yes" else "Not Paid"
                print(
                    f"Name: {name}\nGroup: {group}\nPayment Status: \
                         {payment_status}\n")
    else:
        print("Worksheet for the current month doesn't exist. Please add \
            participants first.")


def main():
    welcome()


main()
