from TestConnection import get_or_create_sheet, SpreadSheet
# wks = get_or_create_sheet(spreadsheet, name)
# Spreadsheet -- spreadsheet key
from StatementParser import parse_creditstatement, credit_transaction_to_rows, parse_chequingsavingsstatement, chequingsavings_transaction_to_rows
# statement_date, transactions, total = parse_statement(pdf_path)
# list_of_lists = transaction_to_rows(transactions)
from datetime import datetime
import calendar

### NOTE: This file is meant to prepare the lists to be imported to the google sheet

# change Xxx. xx, xxxx to functioning date
def convert(statement_date, prompt):
    if (prompt == "full"):
        # for Jun. 21, 2026
        functioning_date = datetime.strptime(statement_date, '%b. %d, %Y')
        return functioning_date
    elif (prompt == "full2"):
        # for Jun 21 2026
        functioning_date = datetime.strptime(statement_date, '%b %d %Y')
        return functioning_date
    elif (prompt == "full3"):
        # for June 21 2026
        functioning_date = datetime.strptime(statement_date, '%B %d %Y')
        return functioning_date
    
    elif (prompt == "month_string"):
        ## receives integer month, returns full month name string

        # month = statement_date[0:3]
        # month = datetime.strptime(month, '%b')
        # month = datetime.strftime(month, '%B')
        month = calendar.month_name[statement_date.month]
        return month
    
    elif (prompt == "month_string2"):
        ## receives 
        month = statement_date.strftime("%B")
        return month
    
    elif (prompt == "month_string_minus1"):
        # month = datetime.strptime(statement_date, '%B')
        # month = month - relativedelta(months=1)
        # month = datetime.strftime(month, '%B')
        month = calendar.month_name[statement_date.month - 1]
        ### FINNICKY IF ITS JANUARY...
        return month
        


# Credit Statement ------------------------------------------------
def credit_statement_sheet(pdf_path, SpreadSheet):
    credit_header = ['Date', 'Description','amount']
    statement_date, transactions, total = parse_creditstatement(pdf_path)

    functioning_statement_date = convert(statement_date, "full")
    month = convert(functioning_statement_date, "month_string")
    month_prev = convert(functioning_statement_date, "month_string_minus1")
    sheet_name_curr = month + " Credit"
    sheet_name_prev = month_prev + " Credit"

    wks_curr = get_or_create_sheet(SpreadSheet, sheet_name_curr, credit_header)
    wks_prev = get_or_create_sheet(SpreadSheet, sheet_name_prev, credit_header)

    credit_lists = credit_transaction_to_rows(transactions)

    for row in credit_lists:
        row_date = row[0]
        row_date = convert(row_date, "full2")
        if row_date.month < functioning_statement_date.month:
            wks_prev.append_row(row, table_range="A1:B1")
        else:
            wks_curr.append_row(row, table_range="A1:B1")


# Chequing Statement ------------------------------------------------
def chequing_statement_sheet(pdf_path, SpreadSheet):
    statement_date, transactions, opening_balance, final_balance = parse_chequingsavingsstatement(pdf_path)
    chequing_header = ['Date', 'Description', 'Outflow', 'Inflow', 'Opening Balance', '', 'Final Balance']
    # Opening Balance = F1
    # Final Balance = H1

    functioning_statement_date = convert(statement_date, "full3")
    month = convert(functioning_statement_date, "month_string")
    month_prev = convert(functioning_statement_date, "month_string_minus1")
    sheet_name_curr = month + " Chequing"
    sheet_name_prev = month_prev + " Chequing"

    wks_curr = get_or_create_sheet(SpreadSheet, sheet_name_curr, chequing_header)
    wks_prev = get_or_create_sheet(SpreadSheet, sheet_name_prev, chequing_header)
    prev_worksheet_list = []
    curr_worksheet_list = []

    chequing_lists = chequingsavings_transaction_to_rows(transactions)
    curr_Fbalance = 0
    prev_Fbalance = 0

    for row in chequing_lists:
        row_date = row[0]
        row_date = convert(row_date, "full2")
        
        if row_date.month < functioning_statement_date.month:
            prev_worksheet_list.append(row)
            prev_Fbalance = row[4]
        else:
            curr_worksheet_list.append(row)
            curr_Fbalance = row[4]
    
    wks_curr.append_rows(curr_worksheet_list, table_range="A1:E1")
    wks_prev.append_rows(prev_worksheet_list, table_range="A1:E1")

    wks_prev.update_acell('H1', prev_Fbalance) # final balance of prev month
    wks_curr.update_acell('F1', prev_Fbalance) # opening balance of curr month
    wks_curr.update_acell('H1', curr_Fbalance) # final balance of curr month


# Savings Statement ------------------------------------------------
def savings_statement_sheet(pdf_path, SpreadSheet):
    statement_date, transactions, opening_balance, final_balance = parse_chequingsavingsstatement(pdf_path)
    savings_header = ['Date', 'Description', 'Outflow', 'Inflow', 'Opening Balance', '','Final Balance']
    # Opening Balance = F1
    # Final Balance = H1

    functioning_statement_date = convert(statement_date, "full3")
    month = convert(functioning_statement_date, "month_string")
    month_prev = convert(functioning_statement_date, "month_string_minus1")
    sheet_name_curr = month + " Savings"
    sheet_name_prev = month_prev + " Savings"

    wks_curr = get_or_create_sheet(SpreadSheet, sheet_name_curr, savings_header)
    wks_prev = get_or_create_sheet(SpreadSheet, sheet_name_prev, savings_header)

    savings_lists = chequingsavings_transaction_to_rows(transactions)
    curr_Fbalance = 0
    prev_Fbalance = 0

    ## to avoid google sheets api write limit
    prev_worksheet_list = []
    curr_worksheet_list = []

    for row in savings_lists:
        row_date = row[0]
        row_date = convert(row_date, "full2")
        
        if row_date.month < functioning_statement_date.month:
            prev_worksheet_list.append(row)
            prev_Fbalance = row[4]
        else:
            curr_worksheet_list.append(row)
            curr_Fbalance = row[4]

    wks_curr.append_rows(curr_worksheet_list, table_range="A1:E1")
    wks_prev.append_rows(prev_worksheet_list, table_range="A1:E1")

    wks_prev.update_acell('H1', prev_Fbalance) # final balance of prev month
    wks_curr.update_acell('F1', prev_Fbalance) # opening balance of curr month
    wks_curr.update_acell('H1', curr_Fbalance) # final balance of curr month


