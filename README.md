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

## 🚀 Roadmap

### Fase 1 - Infraestrutura
- [x] Criação do projeto no Neon  
- [x] Criação dos schemas RAW, STAGING e DW  

### Fase 2 - Extração
- [x] Leitura automática do PDF  
- [x] Extração da DRE  

### Fase 3 - Transformação
- [x] Tratamento dos dados  
- [x] Padronização das contas  

### Fase 4 - Data Warehouse
- [x] Criação das dimensões  
- [x] Criação da tabela fato  

### Fase 5 - Analytics
- [x] Integração com Power BI  
- [x] Dashboard financeiro desenvolvido  

---

## 📊 Status

🟢 Concluído (versão inicial funcional da pipeline)
