import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DB_URL"))
cursor = conn.cursor()

try:
    # =====================================================
    # LIMPEZA + RESET SERIAL
    # =====================================================
    cursor.execute("TRUNCATE TABLE dw.dContas RESTART IDENTITY")

    # =====================================================
    # CARGA dContas (filtrando apenas grupos válidos)
    # =====================================================
    insert_sql = """
    INSERT INTO dw.dContas (
        cod_conta_original,
        cod_conta,
        cod_grupo,
        desc_conta,
        desc_conta_formatada
    )
    SELECT DISTINCT
        codigo_conta AS cod_conta_original,

        CASE
            WHEN codigo_conta = '3.04.01' THEN '04.01'
            WHEN codigo_conta = '3.04.02' THEN '04.02'
            WHEN codigo_conta = '3.04.03' THEN '04.03'
            WHEN codigo_conta = '3.04.04' THEN '04.04'
            WHEN codigo_conta = '3.04.05' THEN '04.05'
            WHEN codigo_conta = '3.04.06' THEN '04.06'
            WHEN codigo_conta = '3.06.01' THEN '06.01'
            WHEN codigo_conta = '3.06.02' THEN '06.02'
            ELSE SUBSTRING(codigo_conta FROM 3)
        END AS cod_conta,

        SUBSTRING(codigo_conta FROM 3 FOR 2) AS cod_grupo,

        descricao AS desc_conta,

        CASE
            WHEN codigo_conta = '3.01' THEN '(+) Receita de Venda de Bens e/ou Serviços'
            WHEN codigo_conta = '3.02' THEN '(-) Custo dos Bens e/ou Serviços Vendidos'
            WHEN codigo_conta = '3.04' THEN '(+/-) Despesas/Receitas Operacionais'
            WHEN codigo_conta = '3.06' THEN '(+/-) Resultado Financeiro'
            WHEN codigo_conta = '3.08' THEN '(-) IR/CS sobre o Lucro'
            ELSE descricao
        END AS desc_conta_formatada

    FROM staging.staging_dre
    WHERE SUBSTRING(codigo_conta FROM 3 FOR 2) IN ('01','02','04','06','08');
    """

    cursor.execute(insert_sql)
    conn.commit()

    print("dContas carregado com filtro de grupos válido 🚀")

except Exception as e:
    conn.rollback()
    print("Erro ao carregar dContas:", e)

finally:
    cursor.close()
    conn.close()