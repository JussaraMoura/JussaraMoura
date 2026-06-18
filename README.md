DRE Pipeline

Este projeto surgiu como evolução do Dashboard Financeiro DRE, desenvolvido inicialmente de forma integral no Power BI.

O objetivo desta nova etapa é construir uma pipeline de dados para extração, tratamento, armazenamento e análise de Demonstrações de Resultado do Exercício (DRE) a partir de arquivos PDF.

Arquitetura da Solução

```text
          PDF
           ↓
          Python
           ↓
          RAW
           ↓
          STAGING
           ↓
          DW
           ↓
          Power BI
```

Tecnologias Utilizadas

- Python
- Pandas
- PostgreSQL (Neon)
- SQLAlchemy
- Power BI
- GitHub

Camadas de Dados

RAW

Armazena os dados exatamente como extraídos dos arquivos PDF, sem qualquer transformação.

STAGING

Responsável pela limpeza, padronização e transformação dos dados, preparando-os para a modelagem analítica.

DW

Camada analítica responsável por armazenar dimensões e fatos utilizados na construção de indicadores e dashboards no Power BI.

Roadmap

Fase 1 - Infraestrutura

- [x] Criação do projeto no Neon
- [x] Criação dos schemas RAW, STAGING e DW

#### Fase 2 - Extração

- [ ] Leitura automática do PDF
- [ ] Extração da DRE

#### Fase 3 - Transformação

- [ ] Tratamento dos dados
- [ ] Padronização das contas

#### Fase 4 - Data Warehouse

- [ ] Criação das dimensões
- [ ] Criação da tabela fato

#### Fase 5 - Analytics

- [ ] Integração com Power BI
- [x] Dashboard financeiro desenvolvido

### Status

🟢 Em desenvolvimento
