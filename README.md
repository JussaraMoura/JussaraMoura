## DRE Pipeline

Pipeline de dados para extração, tratamento, armazenamento e análise de Demonstrações de Resultado do Exercício (DRE) a partir de arquivos PDF.
#### Objetivo: Automatizar o processo de obtenção e preparação de dados financeiros, substituindo transformações manuais realizadas no Power Query por uma arquitetura baseada em Python, PostgreSQL e Power BI.
#### Arquitetura

                    PDF
                     ↓
                    Python
                     ↓
                    RAW
                     ↓
                    STAGING
                     ↓
                    DATA WAREHOUSE
                     ↓
                    Power BI

#### Tecnologias Utilizadas

* Python
* Pandas
* PostgreSQL (Neon)
* SQLAlchemy
* Power BI
* GitHub

### Camadas de Dados
#### RAW: Armazena os dados exatamente como extraídos do PDF.
### STAGING: Responsável pela padronização e transformação dos dados.
### DW: Contém as tabelas dimensionais e fatos utilizadas pelo Power BI.

## Roadmap
### Fase 1 - Infraestrutura
* [x] Criação do projeto no Neon
* [x] Criação dos schemas RAW, STAGING e DW
### Fase 2 - Extração
* [ ] Leitura automática do PDF
* [ ] Extração da DRE
### Fase 3 - Transformação
* [ ] Tratamento dos dados
* [ ] Padronização das contas
### Fase 4 - Data Warehouse
* [ ] Criação das dimensões
* [ ] Criação da tabela fato
### Fase 5 - Analytics
* [ ] Integração com Power BI (Dashboard financeiro já construído)

## Status: 🟢 Em desenvolvimento
