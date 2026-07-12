# ReceiptTracker
I want to automate the data entry of my receipts. So I can analyze my spending habits

Journal entries of my progression -- thoughts and plans
## July 7th:
Made this repo. Started with exploring how to connect python to a google sheet.

Worksheets and spreadsheets are 2 different things. Spreadsheet is the FILE. worksheet is the sheet in the file.
I want to implement bank statements in a separate Spreadsheet, with each worksheet for each month (some tidying needs to be done)
And for receipt tracker, to be in a separate spreadsheet, separated by months for each worksheet.
For now, TestConnection.py is a testing ground for my next steps: OCR and pdf parser

## July 11th:
Continued the experimenting, i didnt know the google api has rate limits so we dont do update_a_cell anymore. append_row is my new best friend
Things to consider: I have Chequing, Savings, and Credit statements to import. I will need to merge them as one before i fuse with receipts table
Started on TestParser.py, Monty Python and the holy grail reference spotted in the parse library example LMAO
Decided not to go with parse, stick with regex bcs theres no clear delimitter

WIP to get to later:
Year for the date object in list -- lookout for december, take the year from the pdf title?
can do location analysis too in the desc
input type (credit, chequing, savings) assigned on when importing the list to the corresponding worksheet

