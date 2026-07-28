import StatementSheet, TestConnection

## ideally, this is where the frontend touches w backend

credit_pdf_path = "BankStatementPDFs/June 21, 2026.pdf"
StatementSheet.credit_statement_sheet(credit_pdf_path, TestConnection.SpreadSheet)

chequing_pdf_path = "BankStatementPDFs/June 25, 2026.pdf"
StatementSheet.chequing_statement_sheet(chequing_pdf_path, TestConnection.SpreadSheet)

savings_pdf_path = "BankStatementPDFs/June 25, 2026_savings.pdf"
StatementSheet.savings_statement_sheet(savings_pdf_path, TestConnection.SpreadSheet)