# ReceiptTracker
I want to automate the data entry of my receipts. So I can analyze my spending habits

Journal entries of my progression -- thoughts and plans
## July 7th:
Made this repo. Started with exploring how to connect python to a google sheet.

- Worksheets and spreadsheets are 2 different things. Spreadsheet is the FILE. worksheet is the sheet in the file.
- I want to implement bank statements in a separate Spreadsheet, with each worksheet for each month (some tidying needs to be done)
- And for receipt tracker, to be in a separate spreadsheet, separated by months for each worksheet.
- For now, TestConnection.py is a testing ground for my next steps: OCR and pdf parser

## July 11th:
- Continued the experimenting, i didnt know the google api has rate limits so we dont do update_a_cell anymore. append_row is my new best friend
- Things to consider: I have Chequing, Savings, and Credit statements to import. I will need to merge them as one before i fuse with receipts table
- Started on TestParser.py, Monty Python and the holy grail reference spotted in the parse library example LMAO
- Decided not to go with parse, stick with regex bcs theres no clear delimitter

### WIP to get to later:
- Year for the date object in list -- lookout for december, take the year from the pdf title?
- can do location analysis too in the desc
- input type (credit, chequing, savings) assigned on when importing the list to the corresponding worksheet

## July 18th:
- I got exhausted from my food service job but now I've got time and tidied my receipts. I realize the receipts have different date formats and that would be hell to upload Unless I do machine learning on the image to extract it.
- Anyways I want this functional soon bcs I have so much receipt backlog all the way from September... I do not want to be manually matching these receipts.
- Today I plan to have the bank statement JSON uploadable to the google sheets.
- Fixed up TestParser.py & TestConnection.py to be modular with minimized inputs
- Realized the Regex i made only caters to my credit bank statements. I need to make a separate regex to read my chequing statements...
- Working on the chequing bank statement parser. It seems I have come into the problem of the parser reading differently of the tables per page. I have no choice but to read it as table as the spaces between columns is monumental to differentiating if it is an inflow or outflow.

### WIP:
- Receipt parser -- have a cash/debit/credit for the reconciliation process to skip cash
- If no receipt - bank statement entry still goes thru
- if no bank statement entry -- what happens to receipt?

## July 21st:
- Since these bank statements are only parsing my bank statements (and given they do not change their formatting).
- I've decided I am going to crop the PDF since the chequing statement has been problematic (defining the border 1 column short, inconsisten column definition across pages).
- The first row in each page is hell... Why are the newlines fused. The first row is being ignored if i crop it right bcs there is no visible line defining the ceiling...
- I can't use "text" horizontal strategy bcs one entry can occupy two "rows" (it uses newline fsr)
- thanks to RickVincent's discussion on the pdfplumber discussion page. ~~I've got it :)~~ NVM that answer was from 2025. things changed since then probably..?
- Ending today on refining the extraction on chequing still. first row extraction is tricky...

### Data flow:
all bank statements -> into one sheet -> parse into separate months biweekly (2x a month)

## July 24th:
- today is a short one, since I have a dragonboat race to get to with Shockwave soon
- first row on first page is included! never thought that I can both use the strategy and explicit. Thanks Claude
- second page onwards, the same strategy does not work. 