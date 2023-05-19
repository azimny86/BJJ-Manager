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


members = SHEET.worksheet('sheet1')

data = members.get_all_values()
print(data)