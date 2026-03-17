# 📊 Projeto 01 — Análise de Vendas e Faturamento

## Sobre o projeto

Análise exploratória de dados de vendas de uma rede varejista americana com o objetivo de identificar padrões de faturamento, sazonalidade, performance por categoria e segmentação de clientes de alto valor.

O projeto simula o trabalho real de um Analista de Dados — desde a ingestão dos dados brutos até a geração de insights estratégicos para tomada de decisão.

---

## Problema de negócio

> *"Quais categorias, regiões e clientes geram mais receita? Existe sazonalidade no faturamento? Quem são os clientes mais valiosos por região?"*

Essas são perguntas reais que gestores fazem — e que este projeto responde com dados.

---

## Dataset

| Item | Detalhe |
|------|---------|
| Fonte | [Kaggle — Superstore Sales Dataset](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting) |
| Volume | 9.800 linhas / 18 colunas |
| Período | Janeiro 2015 a Dezembro 2017 |
| Granularidade | Pedido por produto |

**Principais colunas:**

| Coluna | Descrição |
|--------|-----------|
| order_date | Data do pedido |
| category | Categoria do produto (Technology, Furniture, Office Supplies) |
| sub_category | Subcategoria do produto |
| region | Região de entrega (East, West, Central, South) |
| sales | Valor da venda |
| customer_name | Nome do cliente |
| segment | Segmento do cliente (Consumer, Corporate, Home Office) |

---

## Tecnologias utilizadas

- **Python 3.13** — ingestão e limpeza dos dados com Pandas
- **PostgreSQL 18** — armazenamento e análise com SQL
- **Power BI** — visualização e dashboard (em desenvolvimento)

---

## Estrutura do projeto

```
projeto-01-vendas/
├── data/
│   ├── raw/          # CSV original sem modificações
│   └── processed/    # Dados processados
├── sql/
│   └── analises.sql  # Queries de análise
├── notebooks/
│   └── analise.ipynb # Análise exploratória em Python
├── dashboard/
│   └── vendas.pbix   # Dashboard Power BI
├── importar.py       # Script de ingestão para PostgreSQL
└── README.md
```

---

## Análises realizadas

### 1. Faturamento por categoria e região

Technology lidera em faturamento no East e West mesmo com menos pedidos que Office Supplies — indicando ticket médio mais alto. Office Supplies tem o maior volume de pedidos mas menor valor por venda.

```sql
SELECT
    category,
    region,
    COUNT(*)                        AS pedidos,
    ROUND(SUM(sales)::numeric, 2)   AS faturamento
FROM vendas_superstore
GROUP BY category, region
ORDER BY faturamento DESC;
```

**Insight:** Technology no East gerou R$ 263.116 com 527 pedidos, enquanto Office Supplies no West gerou R$ 217.466 com 1.860 pedidos — 3,5x mais pedidos para um faturamento menor.

---

### 2. Sazonalidade — evolução mensal de faturamento

```sql
SELECT
    DATE_TRUNC('month', order_date)     AS mes,
    ROUND(SUM(sales)::numeric, 2)       AS faturamento,
    COUNT(DISTINCT order_id)            AS pedidos
FROM vendas_superstore
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY mes;
```

**Insight:** Setembro e Novembro são consistentemente os meses de maior faturamento nos 3 anos analisados. Janeiro e Fevereiro apresentam queda expressiva — padrão sazonal previsível que pode guiar planejamento de estoque e campanhas.

---

### 3. Top 10 produtos por faturamento

```sql
SELECT
    product_name,
    category,
    COUNT(*)                        AS vezes_vendido,
    ROUND(SUM(sales)::numeric, 2)   AS faturamento_total,
    ROUND(AVG(sales)::numeric, 2)   AS ticket_medio
FROM vendas_superstore
GROUP BY product_name, category
ORDER BY faturamento_total DESC
LIMIT 10;
```

**Insight:** Canon imageCLASS 2200 gerou R$ 61.599 em apenas 5 vendas — ticket médio de R$ 12.319. Produtos de Technology dominam o topo com alto valor por unidade, mesmo com baixo volume de pedidos.

---

### 4. Ranking de clientes por faturamento — Window Function

```sql
SELECT
    customer_name,
    segment,
    region,
    ROUND(SUM(sales)::numeric, 2)                              AS faturamento_total,
    COUNT(DISTINCT order_id)                                   AS total_pedidos,
    RANK() OVER (ORDER BY SUM(sales) DESC)                     AS ranking_geral,
    RANK() OVER (PARTITION BY region ORDER BY SUM(sales) DESC) AS ranking_por_regiao
FROM vendas_superstore
GROUP BY customer_name, segment, region
ORDER BY faturamento_total DESC
LIMIT 15;
```

**Insight:** Sean Miller (Home Office / South) é o cliente #1 com R$ 23.669 em apenas 2 pedidos — perfil de alto valor e baixa frequência. O ranking por região (`PARTITION BY`) permite identificar os clientes mais valiosos dentro de cada mercado local, viabilizando estratégias de retenção segmentadas.

---

## Principais conclusões

- **Technology** é a categoria de maior faturamento apesar do menor volume de pedidos
- **Setembro e Novembro** são os meses de pico — sazonalidade consistente nos 3 anos
- **Janeiro e Fevereiro** são os meses mais fracos — oportunidade para campanhas de reativação
- **Top 15 clientes** concentram parte relevante do faturamento — risco de concentração e oportunidade de fidelização
- **West e East** são as regiões de maior receita em todas as categorias

---

## Como reproduzir

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/projeto-data.git
```

**2. Configure o PostgreSQL**
```bash
# Crie o banco
psql -U postgres -c "CREATE DATABASE estudos_dados;"
```

**3. Instale as dependências Python**
```bash
pip install pandas psycopg2-binary
```

**4. Execute a importação**
```bash
python importar.py
```

**5. Rode as queries**
```bash
psql -U postgres -d estudos_dados -f sql/analises.sql
```

---

## Autor

**Lucas Rezende**
Analista de Dados | SQL · Power BI · Python | Background Industrial e Marketing Digital

[![LinkedIn](https://img.shields.io/badge/LinkedIn-lucas--rzd-blue)](https://www.linkedin.com/in/lucas-rzd/)
[![GitHub](https://img.shields.io/badge/GitHub-projeto--data-black)](https://github.com/seu-usuario)
