from TestConnection import get_or_create_sheet, SpreadSheet
# wks = get_or_create_sheet(spreadsheet, name)
# Spreadsheet -- spreadsheet key
from TestParser import parse_creditstatement, credit_transaction_to_rows, parse_chequingsavingsstatement, chequingsavings_transaction_to_rows
# statement_date, transactions, total = parse_statement(pdf_path)
# list_of_lists = transaction_to_rows(transactions)
from datetime import datetime
from dateutil.relativedelta import relativedelta

### NOTE: This file is meant to prepare the lists to be imported to the google sheet

# change Xxx. xx, xxxx to functioning date
def convert(statement_date, prompt):
    if (prompt == "full"):
        functioning_date = datetime.strptime(statement_date, '%b. %d, %Y')
        return functioning_date
    elif (prompt == "full2"):
        functioning_date = datetime.strptime(statement_date, '%b %d %Y')
        return functioning_date
    elif (prompt == "month_string"):
        month = statement_date[0:3]
        month = datetime.strptime(month, '%b')
        month = datetime.strftime(month, '%B')
        return month
    elif (prompt == "month_string_minus1"):
        month = datetime.strptime(statement_date, '%B')
        month = month - relativedelta(months=1)
        month = datetime.strftime(month, '%B')
        return month
        


# Credit Statement ------------------------------------------------
credit_header = ['Date', 'Description','amount']
statement_date, transactions, total = parse_creditstatement("BankStatementPDFs/June 21, 2026.pdf")

functioning_statement_date = convert(statement_date, "full")
month = convert(statement_date, "month_string")
month_prev = convert(month, "month_string_minus1")
sheet_name_curr = month + " Credit"
sheet_name_prev = month_prev + " Credit"

wks_prev = get_or_create_sheet(SpreadSheet, sheet_name_prev, credit_header)
wks_curr = get_or_create_sheet(SpreadSheet, sheet_name_curr, credit_header)

credit_lists = credit_transaction_to_rows(transactions)

for row in credit_lists:
    row_date = row[0]
    row_date = convert(row_date, "full2")
    if row_date.month < functioning_statement_date.month:
        wks_prev.append_row(row, table_range="A1:B1")
    else:
        wks_curr.append_row(row, table_range="A1:B1")
# wks.append_rows(sheet_name, table_range="A1:B1")


# Chequing Statement ------------------------------------------------
statement_date, transactions, opening_balance, final_balance = parse_chequingsavingsstatement("BankStatementPDFs/June 25, 2026.pdf")

chequing_header = ['Date', 'Description', 'Outflow', 'Inflow', 'Opening Balance', opening_balance,'Final Balance', final_balance]
wks = get_or_create_sheet(SpreadSheet, "Chequing Statement", chequing_header)

chequing_lists = chequingsavings_transaction_to_rows(transactions)
wks.append_rows(chequing_lists, table_range="A1:E1")


# # Savings Statement ------------------------------------------------
# statement_date, transactions, opening_balance, final_balance = parse_chequingsavingsstatement("BankStatementPDFs/June 25, 2026_savings.pdf")

# savings_header = ['Date', 'Description', 'Outflow', 'Inflow', 'Opening Balance', opening_balance,'Final Balance', final_balance]
# wks = get_or_create_sheet(SpreadSheet, "Savings Statement", savings_header)

# savings_lists = chequingsavings_transaction_to_rows(transactions)
# wks.append_rows(savings_lists, table_range="A1:E1")

