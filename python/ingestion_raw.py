import os
import pdfplumber
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

# =====================================================
# Configuração de ambiente
# =====================================================
load_dotenv()
DB_URL = os.getenv("DB_URL")

PDF_PATH = "/workspaces/JussaraMoura/pdf/Vulcabras.pdf"


# =====================================================
# Conexão com banco
# =====================================================
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()


# =====================================================
# Função de insert na RAW
# =====================================================
def insert_raw(file_name, page_num, line_text):
    cursor.execute("""
        INSERT INTO raw.raw_dre (
            fonte_arquivo,
            pagina,
            linha_original,
            data_carga
        )
        VALUES (%s, %s, %s, %s)
    """, (
        file_name,
        page_num,
        line_text,
        datetime.now()
    ))


# =====================================================
# Leitura do PDF + ingestão
# =====================================================
with pdfplumber.open(PDF_PATH) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):

        text = page.extract_text()

        if not text:
            continue

        lines = text.split("\n")

        for line in lines:
            line = line.strip()

            if line:  # evita linhas vazias
                insert_raw(
                    file_name="Vulcabras.pdf",
                    page_num=page_num,
                    line_text=line
                )

# =====================================================
# Commit e fechamento
# =====================================================
conn.commit()
cursor.close()
conn.close()

print("Carga RAW concluída com sucesso 🚀")