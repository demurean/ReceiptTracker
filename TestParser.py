import pdfplumber
# https://unstract.com/blog/guide-to-pdfplumber-text-and-table-extraction-capabilities/#elementor-toc__heading-anchor-1
# https://deepwiki.com/jsvine/pdfplumber/3.3-table-extraction
import re
# https://www.w3schools.com/python/python_regex.asp
# https://www.geeksforgeeks.org/python/re-compile-in-python/
from datetime import datetime

# regex time
### VV THIS IS BUILT TO PARSE THE CREDIT STATEMENT 
def parse_creditstatement(pdf_path):
    transactions = []
    total_balance = 0
    statement_date = "2026"

    statement_paper_date = re.compile(r"Statement date (?P<statementDate>[A-Z][a-z]{2}\. \d{1,2}\, \d{4})")
    # Statement period May. 22, 2026 - June. 21, 2026 << kalo mau di apa2in

    total_pattern = re.compile(r"Total balance\s\$(?P<total>\d+\.\d{2})")
    # Total balance $722.26
    pattern = re.compile(r"(?P<trans_month>[A-Z][a-z]{2})\. (?P<trans_date>\d{1,2})\s?[A-Z][a-z]{2}\. \d{1,2} (?P<desc>.+?) (?P<amount>\d+\.\d{2})(?P<CREDIT>\s+CR)?$")
    # month. day month. day descdescdesc amount.00 (potential CR at end)
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            for line in page_text.split("\n"):

                statement_date_match = statement_paper_date.search(line)
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
def transaction_to_rows(transactions):
    big_list = []
    for entry in transactions:
        small_list = []
        small_list.append(entry.get("date"))
        small_list.append(entry.get("description"))
        small_list.append(entry.get("amount"))
        # small_list.append(entry.get("type"))
        big_list.append(small_list)
        # print(small_list)
    return big_list

## VV meant to parse only the chequing statement
def parse_chequingstatement(pdf_path):
    transactions = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if page.page_number == 1:
                page1_table_area = page.crop((60.0, 520, 600 ,735.0))
                column_lines = [60, 100, 348.24, 436.31999999999994, 511.91999999999996, 533.9599995]

            #     # debugging
            #     page1_table_image = page1_table_area.to_image()
            #     page1_table_image.debug_tablefinder(table_settings={
            #         "vertical_strategy": "explicit",
            #         "explicit_vertical_lines": column_lines,
            #         "horizontal_strategy": "lines",
            #         })
            #     page1_table_image.show()
            #    # test = page1_table_area.debug_tablefinder(table_settings={"vertical_strategy": "text", "horizontal_strategy": "lines",})
            #    # print(test.cells)
               
                test = page1_table_area.extract_text_lines(return_chars=False)[0] # I CANT USE THIS SOLUTION IF THE COLUMN IS IMPORTANT >.<
                print(test)
                table = page1_table_area.extract_table({
                    "vertical_strategy": "explicit",
                    "explicit_vertical_lines": column_lines,
                    "horizontal_strategy": "lines",
                    })
                for row in table:
                    print(row)
            # else:
            #     table = page.extract_tables({
            #         "vertical_strategy": "text",
            #         "horizontal_strategy": "lines",
            #         # "intersection_x_tolerance": 10,
            #     })

            # # visual debugging
            # image = page.to_image()
            # image.debug_tablefinder(table_settings={"vertical_strategy": "text", "horizontal_strategy": "lines",})
            # image.show()
            # test = page.debug_tablefinder(table_settings={"vertical_strategy": "text", "horizontal_strategy": "lines",})
            # print(test.cells)

            # if table:
            #     prev_balance = 0
            #     for row in table:
            #         # print(row)
            #         if len(row) == 4:
            #             date_desc = row[0]
            #             date = date_desc[0:3] + " " + date_desc[3:5]
            #             desc = date_desc[6:]
            #             outflow = row[1]
            #             inflow = row[2]
            #             balance = row[3]
            #             transactions.append({
            #                 "date": date,
            #                 "desc": desc,
            #                 "outflow": outflow,
            #                 "inflow": inflow
            #             })
            #             prev_balance = balance

            #         elif len(row) == 1:
            #             pattern = re.compile(r"(?P<trans_month>[A-Z][a-z]{2})(?P<trans_date>\d{1,2})\s(?P<desc>.+?) (?P<amount>\d+\.\d{2}) (?P<balance>\d+\.\d{2})$")
            #             match = pattern.search(row[0])
            #             if match:
            #                 amount = match.group("amount")
            #                 balance = match.group("balance")
            #                 # if (balance - amount) == transactions:

            #                 transactions.append({
            #                     "date": match.group("trans_month") +" "+ match.group("trans_date"),
            #                     "desc": match.group("desc"),
            #                     "amount": amount,
            #                     "balance": balance
            #                     # gotta do some calc with the previous entry to see if balance grows or shrinks to know if this is an inflow or outflow
            #                 })
            #     print(transactions)
            # print(f"Page {page.page_number}:\\n{table}\\n")



# something about protecting debug prints
if __name__ == "__main__":
    statement_date, transactions, total = parse_creditstatement("BankStatementPDFs/June 21, 2026.pdf")
    # print(statement_date)
    # print(transactions)
    # print(total)
    list_of_lists = transaction_to_rows(transactions)
    # print(list_of_lists)

    parse_chequingstatement("BankStatementPDFs/June 25, 2026.pdf")