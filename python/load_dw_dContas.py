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
    # CARGA dContas CORRIGIDA
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

        -- ====================================================================
        -- 1. CORREÇÃO DO COD_CONTA
        -- ====================================================================
        -- Se for conta de 2 níveis (3.01, 3.02, 3.08), fixamos o '.01' no final.
        -- Se já for de 3 níveis (3.04.01), apenas removemos o '3.' inicial.
        CASE
            WHEN array_length(string_to_array(codigo_conta, '.'), 1) = 2
                THEN split_part(codigo_conta, '.', 2) || '.01'
            ELSE
                split_part(codigo_conta, '.', 2) || '.' || split_part(codigo_conta, '.', 3)
        END AS cod_conta,

        -- ====================================================================
        -- 2. GRUPO
        -- ====================================================================
        split_part(codigo_conta, '.', 2) AS cod_grupo,

        descricao AS desc_conta,

        -- ====================================================================
        -- 3. DESCRIÇÃO FORMATADA (Corrigido para não usar LIKE generalizado)
        -- ====================================================================
        CASE
            WHEN codigo_conta = '3.01' THEN '(+) Receita de Venda de Bens e/ou Serviços'
            WHEN codigo_conta = '3.02' THEN '(-) Custo dos Bens e/ou Serviços Vendidos'
            WHEN codigo_conta = '3.08' THEN '(-) Imposto de Renda e Contribuição Social sobre o Lucro'
            ELSE descricao
        END AS desc_conta_formatada

    FROM staging.staging_dre
    WHERE 
        -- Filtra apenas os grupos desejados
        split_part(codigo_conta, '.', 2) IN ('01','02','04','06','08')
        
        -- ====================================================================
        -- 4. FILTRO DE LINHAS ANALÍTICAS (Não calculáveis no Power BI)
        -- ====================================================================
        -- Remove as contas agregadoras (3.04, 3.06) que confundem o relacionamento.
        -- Só deixa passar contas com 3 partes (ex: 3.04.01) OU as contas base (3.01, 3.02, 3.08)
        AND (
            array_length(string_to_array(codigo_conta, '.'), 1) = 3 
            OR codigo_conta IN ('3.01', '3.02', '3.08')
        );
    """

    cursor.execute(insert_sql)
    conn.commit()

    print("dContas carregado com sucesso e corrigido! 🚀")

except Exception as e:
    conn.rollback()
    print("Erro ao carregar dContas:", e)

finally:
    cursor.close()
    conn.close()