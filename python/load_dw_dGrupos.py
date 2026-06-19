import psycopg2
import os
from dotenv import load_dotenv

# =====================================================
# 1. CARREGAR VARIÁVEIS DE AMBIENTE
# =====================================================
load_dotenv()

DB_URL = os.getenv("DB_URL")

# =====================================================
# 2. CONEXÃO COM BANCO (NEON)
# =====================================================
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

print("Conectado ao DW com sucesso 🚀")

# =====================================================
# 3. LIMPAR TABELA DIMENSÃO (FULL REFRESH)
# =====================================================
cursor.execute("TRUNCATE TABLE dw.dGrupos RESTART IDENTITY;")

print("dGrupos limpo ✔")

# =====================================================
# 4. CARGA DA DIMENSÃO
# =====================================================
insert_sql = """
INSERT INTO dw.dGrupos (
    cod_grupo,
    cod_original,
    desc_grupo,
    grupo_curto,
    subtotal
)
SELECT DISTINCT
    REPLACE(codigo_conta, '3.', '') AS cod_grupo,
    codigo_conta AS cod_original,

    CASE
        WHEN codigo_conta = '3.01' THEN '(+) Receita de Venda de Bens e/ou Serviços'
        WHEN codigo_conta = '3.02' THEN '(-) Custo dos Bens e/ou Serviços Vendidos'
        WHEN codigo_conta = '3.03' THEN '(=) Resultado Bruto'
        WHEN codigo_conta = '3.04' THEN '(+/-) Despesas/Receitas Operacionais'
        WHEN codigo_conta = '3.05' THEN '(=) Resultado Operacional (EBIT)'
        WHEN codigo_conta = '3.06' THEN '(+/-) Resultado Financeiro'
        WHEN codigo_conta = '3.07' THEN '(=) Resultado Antes dos Tributos (EBT)'
        WHEN codigo_conta = '3.08' THEN '(-) IR/CS sobre o Lucro'
        WHEN codigo_conta = '3.09' THEN '(=) Lucro Líquido'
        ELSE NULL
    END AS desc_grupo,

    CASE
        WHEN codigo_conta = '3.01' THEN 'Receita'
        WHEN codigo_conta = '3.02' THEN 'CPV'
        WHEN codigo_conta = '3.03' THEN 'Lucro Bruto'
        WHEN codigo_conta = '3.04' THEN 'Operacional'
        WHEN codigo_conta = '3.05' THEN 'EBIT'
        WHEN codigo_conta = '3.06' THEN 'Financeiro'
        WHEN codigo_conta = '3.07' THEN 'EBT'
        WHEN codigo_conta = '3.08' THEN 'IR/CS'
        WHEN codigo_conta = '3.09' THEN 'Lucro Líquido'
        ELSE NULL
    END AS grupo_curto,

    CASE
        WHEN codigo_conta IN ('3.03','3.05','3.07','3.09') THEN 1
        ELSE -1
    END AS subtotal

FROM staging.staging_dre
WHERE LENGTH(codigo_conta) = 4
AND codigo_conta NOT IN ('3.11');
"""

cursor.execute(insert_sql)

# =====================================================
# 5. COMMIT
# =====================================================
conn.commit()

# =====================================================
# 6. ENCERRAR CONEXÃO
# =====================================================
cursor.close()
conn.close()

print("dGrupos carregado com sucesso 🚀")