import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DB_URL"))
cursor = conn.cursor()

# =====================================================
# 1. Buscar dados da RAW
# =====================================================
cursor.execute("""
    SELECT pagina, linha_original
    FROM raw.raw_dre
""")

rows = cursor.fetchall()

# =====================================================
# 2. Parsing (RAW → STAGING)
# =====================================================
parsed = []

for pagina, linha in rows:

    linha = linha.strip()

    if "3." not in linha:
        continue

    parts = linha.split()

    try:
        codigo = parts[0]
        valor_2025, valor_2024, valor_2023 = parts[-3:]
        descricao = " ".join(parts[1:-3])

        parsed.append((
            pagina,
            codigo,
            descricao,
            float(valor_2025.replace(".", "").replace(",", ".")),
            float(valor_2024.replace(".", "").replace(",", ".")),
            float(valor_2023.replace(".", "").replace(",", "."))
        ))

    except Exception:
        continue


# =====================================================
# 3. INSERT no STAGING
# =====================================================
insert_query = """
INSERT INTO staging.staging_dre (
    pagina,
    codigo_conta,
    descricao,
    valor_2025,
    valor_2024,
    valor_2023,
    data_carga
)
VALUES (%s, %s, %s, %s, %s, %s, NOW())
"""

cursor.executemany(insert_query, parsed)

conn.commit()

cursor.close()
conn.close()

print(f"STAGING carregado com sucesso 🚀 | registros: {len(parsed)}")