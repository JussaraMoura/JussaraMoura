import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DB_URL"))
cursor = conn.cursor()

try:
    # =====================================================
    # LIMPEZA DA FATO
    # =====================================================
    cursor.execute("""
        TRUNCATE TABLE dw.flancamentos RESTART IDENTITY;
    """)

    # =====================================================
    # LISTA DE CONTAS ANALÍTICAS
    # =====================================================
    contas_validas = """
        '3.01',
        '3.02',
        '3.04.01',
        '3.04.02',
        '3.04.03',
        '3.04.04',
        '3.04.05',
        '3.04.06',
        '3.06.01',
        '3.06.02',
        '3.08'
    """

    # =====================================================
    # INSERT COM UNPIVOT (2023 / 2024 / 2025)
    # =====================================================
    sql = f"""
    INSERT INTO dw.flancamentos (
        cod_conta,
        desc_conta,
        data_referencia,
        valor
    )

    -- =========================
    -- 2023
    -- =========================
    SELECT
        CASE
            WHEN codigo_conta = '3.01' THEN '01.01'
            WHEN codigo_conta = '3.02' THEN '02.01'
            WHEN codigo_conta = '3.08' THEN '08.01'
            ELSE SUBSTRING(codigo_conta FROM 3)
        END AS cod_conta,
        descricao,
        DATE '2023-12-31',
        valor_2023
    FROM staging.staging_dre
    WHERE codigo_conta IN ({contas_validas})

    UNION ALL

    -- =========================
    -- 2024
    -- =========================
    SELECT
        CASE
            WHEN codigo_conta = '3.01' THEN '01.01'
            WHEN codigo_conta = '3.02' THEN '02.01'
            WHEN codigo_conta = '3.08' THEN '08.01'
            ELSE SUBSTRING(codigo_conta FROM 3)
        END,
        descricao,
        DATE '2024-12-31',
        valor_2024
    FROM staging.staging_dre
    WHERE codigo_conta IN ({contas_validas})

    UNION ALL

    -- =========================
    -- 2025
    -- =========================
    SELECT
        CASE
            WHEN codigo_conta = '3.01' THEN '01.01'
            WHEN codigo_conta = '3.02' THEN '02.01'
            WHEN codigo_conta = '3.08' THEN '08.01'
            ELSE SUBSTRING(codigo_conta FROM 3)
        END,
        descricao,
        DATE '2025-12-31',
        valor_2025
    FROM staging.staging_dre
    WHERE codigo_conta IN ({contas_validas});
    """

    cursor.execute(sql)
    conn.commit()

    print("fLancamentos carregada com sucesso 🚀")

except Exception as e:
    conn.rollback()
    print("Erro na carga fLancamentos:", e)

finally:
    cursor.close()
    conn.close()