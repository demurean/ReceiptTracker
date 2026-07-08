from google.oauth2.service_account import Credentials
import gspread

# Loads service account credentials
# reference: https://googleapis.dev/python/google-auth/latest/reference/google.oauth2.service_account.html#module-google.oauth2.service_account
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = Credentials.from_service_account_file('PythonToSheetsServiceAccount.json', scopes=scopes)

# Opens gsheet
# reference: https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account
gc = gspread.authorize(credentials)
wks = gc.open_by_url('https://docs.google.com/spreadsheets/d/1LFKsn1_iR_rhZqDz8zxeU924k5FYKNnbuNPX_pRwr68/edit?gid=0#gid=0').sheet1

# # updates a row
wks.update_acell('A1', 'Hello World')