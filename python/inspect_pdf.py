import pdfplumber

PDF_PATH = "/workspaces/JussaraMoura/pdf/Vulcabras.pdf"

with pdfplumber.open(PDF_PATH) as pdf:
    page = pdf.pages[0]

    print("\n--- TEXTO ---\n")
    print(page.extract_text())

    print("\n--- TABELA ---\n")
    table = page.extract_table()
    print(table)