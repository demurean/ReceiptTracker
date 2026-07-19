from TestConnection import get_or_create_sheet, SpreadSheet
# wks = get_or_create_sheet(spreadsheet, name)
# Spreadsheet -- spreadsheet key
from TestParser import parse_creditstatement, transaction_to_rows
# statement_date, transactions, total = parse_statement(pdf_path)
# list_of_lists = transaction_to_rows(transactions)

headers = ['Date', 'Description','amount']

# Credit Statement
wks = get_or_create_sheet(SpreadSheet, "Credit Statement", headers)

statement_date, transactions, total = parse_creditstatement("BankStatementPDFs/June 21, 2026.pdf")
list_of_lists = transaction_to_rows(transactions)
wks.append_rows(list_of_lists, table_range="A1:B1")

# Chequing Statement