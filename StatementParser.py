import pdfplumber
# https://unstract.com/blog/guide-to-pdfplumber-text-and-table-extraction-capabilities/#elementor-toc__heading-anchor-1
# https://deepwiki.com/jsvine/pdfplumber/3.3-table-extraction
import re
# https://www.w3schools.com/python/python_regex.asp
# https://www.geeksforgeeks.org/python/re-compile-in-python/
from datetime import datetime

### NOTE: This file is meant to parse directly from the pdf statements

### VV THIS IS BUILT TO PARSE THE CREDIT STATEMENT 
def parse_creditstatement(pdf_path):
    transactions = []
    total_balance = 0
    statement_date = "2026"

    statement_paper_date_pattern = re.compile(r"Statement date (?P<statementDate>[A-Z][a-z]{2}\. \d{1,2}\, \d{4})")
    # Statement period May. 22, 2026 - June. 21, 2026 << kalo mau di apa2in

    total_pattern = re.compile(r"Total balance\s\$(?P<total>\d+\.\d{2})")
    # Total balance $722.26
    pattern = re.compile(r"(?P<trans_month>[A-Z][a-z]{2})\. (?P<trans_date>\d{1,2})\s?[A-Z][a-z]{2}\. \d{1,2} (?P<desc>.+?) (?P<amount>\d+\.\d{2})(?P<CREDIT>\s+CR)?$")
    # month. day month. day descdescdesc amount.00 (potential CR at end)
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            for line in page_text.split("\n"):

                statement_date_match = statement_paper_date_pattern.search(line)
                if statement_date_match:
                    statement_date = statement_date_match.group("statementDate")
                    # print(statement_date)

                total_match = total_pattern.search(line)
                if total_match:
                    total_balance = float(total_match.group("total"))

                match = pattern.search(line)
                if match:
                    cr = match.group("CREDIT")
                    transactions.append({
                        # "date": datetime.strptime(match.group("trans_month") +" "+ match.group("trans_date") +" "+ statement_date[-4:], "%b %d %Y").date(),
                        "date": match.group("trans_month") +" "+ match.group("trans_date") +" "+ statement_date[-4:],
                        "description": match.group("desc"),
                        "amount": -float(match.group("amount")) if cr else float(match.group("amount")),
                        # negative if inflow!!
                        # "type": "Credit"
                    })
            # print(f"Page {page.page_number}:\\n{page_text}\\n")
    return statement_date, transactions, total_balance

# convert list of dicts to list of lists
def credit_transaction_to_rows(transactions):
    big_list = []
    for entry in transactions:
        small_list = []
        small_list.append(entry.get("date"))
        small_list.append(entry.get("description"))
        small_list.append(entry.get("amount"))
        big_list.append(small_list)
    return big_list

def chequingsavings_transaction_to_rows(transactions):
    big_list = []
    for entry in transactions:
        row = []
        row.append(entry.get("date"))
        row.append(entry.get("description"))
        row.append(entry.get("outflow"))
        row.append(entry.get("inflow"))
        row.append(entry.get("balance"))
        
        if entry.get("description") == "Openingbalance":
            continue
        else:
            big_list.append(row)
    return big_list

## VV meant to parse only the chequing statement (and savings bcs they have same format)
def parse_chequingsavingsstatement(pdf_path):
    transactions = []
    final_balance = 0
    opening_balance = 0
    statement_date = "2026"

    with pdfplumber.open(pdf_path) as pdf:
        # extract statement date
        date_page = pdf.pages[0].extract_text()
        date_pattern = re.compile(r"For the period ending (?P<date_month>[A-Z][a-z]{2,8}) (?P<date_day>\d{1,2}), (?P<date_year>\d{4})")
        for line in date_page.split("\n"):
            statement_date_match = date_pattern.search(line)
            if statement_date_match:
                statement_month = statement_date_match.group("date_month")
                statement_day = statement_date_match.group("date_day")
                statement_year = statement_date_match.group("date_year")
                statement_date = statement_month + " " + statement_day + " " + statement_year
        
        # table of money flows
        column_lines = [60, 100, 345, 430, 490, 533.9599995]
        for page in pdf.pages:
            if page.page_number == 1: #first page table starts at bottom of page
                page1_table_area = page.crop((60.0, 526, 600 ,735.0)) # x0, top, x1, bottom
                first_row = page1_table_area.bbox[1]
               
                table = page1_table_area.extract_table({
                    "vertical_strategy": "explicit",
                    "explicit_vertical_lines": column_lines,
                    "horizontal_strategy": "lines",
                    "explicit_horizontal_lines": [first_row]
                    })
                
            else: # table starts at top
                pagex_table_area = page.crop((60, 110, 600, 735))
                first_row = pagex_table_area.bbox[1]
                
                table = pagex_table_area.extract_table({
                    "vertical_strategy": "explicit",
                    "explicit_vertical_lines": column_lines,
                    "horizontal_strategy": "lines",
                    "explicit_horizontal_lines": [first_row]
                })

            if table:
                pattern = re.compile(r"(?P<date_month>[A-Z][a-z]{2})(?P<date_day>\d{1,2})")
                for row in table:
                    # print(row)
                    datetext = pattern.search(row[0])
                    if datetext:
                        date_month = datetext.group("date_month")
                        date_day = datetext.group("date_day")
                    desc = row[1]
                    outflow = row[2]
                    inflow = row[3]
                    balance = row[4]
                    final_balance = balance
                    # ------------------------------------------------
                    transactions.append({
                        "date": date_month + " " + date_day +" "+ statement_date[-4:],
                        "description": desc,
                        "outflow": outflow,
                        "inflow": inflow,
                        "balance": balance
                    })
                    if desc == "Openingbalance":
                        opening_balance = balance
    # print(transactions)
    # print(statement_date)
    return statement_date, transactions, opening_balance, final_balance


# something about protecting debug prints
if __name__ == "__main__":
    statement_date, transactions, total = parse_creditstatement("BankStatementPDFs/June 21, 2026.pdf")
    credit_list = credit_transaction_to_rows(transactions)

    statement_date, transactions, opening_balance, final_balance = parse_chequingsavingsstatement("BankStatementPDFs/June 25, 2026.pdf")
    chequing_list = chequingsavings_transaction_to_rows(transactions)

    statement_date, transactions, opening_balance, final_balance = parse_chequingsavingsstatement("BankStatementPDFs/June 25, 2026_savings.pdf")
    savings_list = chequingsavings_transaction_to_rows(transactions)
