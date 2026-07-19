from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime

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
SpreadSheet = gc.open_by_key('1LFKsn1_iR_rhZqDz8zxeU924k5FYKNnbuNPX_pRwr68')

##-------------------------------------------------------------------------------------------------
# finds worksheet by name 
    # -- if NF, creates it with default headers
    # -- if F, leaves alone,
    # returns the worksheet
def get_or_create_sheet(spreadsheet, name, headers):
    try:
        worksheet = spreadsheet.worksheet(name)
    except gspread.exceptions.WorksheetNotFound as shNF:
        print("Oops, no worksheet found by that name.", shNF)
        worksheet = spreadsheet.add_worksheet(title=name, rows=100, cols=20)
        # header installation -- hardcode:
        # worksheet.update_acell('A1', 'Date')
        # worksheet.update_acell('B1', 'WIP')
        # worksheet.update_acell('C1', 'Bank Statement for:')
        # worksheet.update_acell('D1', 'WIP')
        worksheet.append_row(headers)
    return worksheet

headers = ['Date', 'Description',' ','amount']
# 'Credit','Debit','Cash'
wks = get_or_create_sheet(SpreadSheet, "BankTransactions", headers)
# reference: https://stackoverflow.com/questions/67082749/append-a-new-row-to-the-end-of-sheets-using-gspread
# wks.append_row(['Hello', 'World']) 
# wks.append_rows([['test1', 'test2'], ['test3', 'test4']], table_range="A1:B1")
# so the input gotta be a list of list..
# ListTest = [['tes1', 'tes2', 'tes3', 'tes4']] # one row, 4 columns
# wks.append_rows(ListTest)
# I need that table_range for updating the table
# if i dont use table_range, the appending will be done on the tip (lowest cell with content) so it will change.. 