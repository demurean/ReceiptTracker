import pdfplumber
# https://unstract.com/blog/guide-to-pdfplumber-text-and-table-extraction-capabilities/#elementor-toc__heading-anchor-1
import re
# https://www.w3schools.com/python/python_regex.asp
# https://www.geeksforgeeks.org/python/re-compile-in-python/
from datetime import datetime

# regex time
def parse_statement(pdf_path, year):
    transactions = []
    total_balance = 0
    total_pattern = re.compile(r"Total balance\s\$(?P<total>\d+\.\d{2})")
    # Total balance $722.26
    pattern = re.compile(r"(?P<trans_month>[A-Z][a-z]{2})\. (?P<trans_date>\d{1,2})\s?[A-Z][a-z]{2}\. \d{1,2} (?P<desc>.+?) (?P<amount>\d+\.\d{2})(?P<CREDIT>\s+CR)?$")
    # month. day month. day descdescdesc amount.00 (potential CR at end)
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            for line in page_text.split("\n"):

                total_match = total_pattern.search(line)
                if total_match:
                    total_balance = float(total_match.group("total"))

                match = pattern.search(line)
                if match:
                    cr = match.group("CREDIT")
                    transactions.append({
                        "date": datetime.strptime(match.group("trans_month") +" "+ match.group("trans_date") +" "+ str(year), "%b %d %Y").date(),
                        "description": match.group("desc"),
                        "amount": float(match.group("amount")),
                        "type": "credit" if cr else "debit"
                    })
            # print(f"Page {page.page_number}:\\n{page_text}\\n")
    return transactions, total_balance

# something about protecting debug prints
if __name__ == "__main__":
    transactions, total = parse_statement("BankStatementPDFs/June 21, 2026.pdf", 2026)
    print(transactions)
    print(total)