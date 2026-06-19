import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DB_URL"))
cursor = conn.cursor()

try:
    # =====================================================
    # LIMPEZA
    # =====================================================
    cursor.execute("TRUNCATE TABLE dw.dcontas RESTART IDENTITY")

    # =====================================================
    # CARGA dContas (REGRA FINAL CORRETA)
    # =====================================================
    insert_sql = """
    INSERT INTO dw.dcontas (
        cod_conta_original,
        cod_conta,
        cod_grupo,
        desc_conta,
        desc_conta_formatada
    )
    SELECT DISTINCT
        codigo_conta AS cod_conta_original,

        -- =========================
        -- COD_CONTA (REGRA FINAL)
        -- =========================
        CASE
            WHEN array_length(string_to_array(codigo_conta, '.'), 1) = 2
                THEN split_part(codigo_conta, '.', 2) || '.' || split_part(codigo_conta, '.', 2)

            ELSE
                split_part(codigo_conta, '.', 2) || '.' || split_part(codigo_conta, '.', 3)
        END AS cod_conta,

        -- =========================
        -- GRUPO
        -- =========================
        split_part(codigo_conta, '.', 2) AS cod_grupo,

        descricao AS desc_conta,

        -- =========================
        -- DESCRIÇÃO FORMATADA
        -- =========================
        CASE
            WHEN codigo_conta = '3.01'
                THEN '(+) Receita de Venda de Bens e/ou Serviços'

            WHEN codigo_conta = '3.02'
                THEN '(-) Custo dos Bens e/ou Serviços Vendidos'

            WHEN codigo_conta LIKE '3.04%'
                THEN 'Despesas com Vendas / Operacionais'

            WHEN codigo_conta LIKE '3.06%'
                THEN 'Resultado Financeiro'

            WHEN codigo_conta = '3.08'
                THEN '(-) IR/CS sobre o Lucro'

            ELSE descricao
        END AS desc_conta_formatada

    FROM staging.staging_dre
    WHERE split_part(codigo_conta, '.', 2) IN ('01','02','04','06','08');
    """

    cursor.execute(insert_sql)
    conn.commit()

    print("dContas carregado com regra final correta 🚀")

except Exception as e:
    conn.rollback()
    print("Erro ao carregar dContas:", e)

finally:
    cursor.close()
    conn.close()