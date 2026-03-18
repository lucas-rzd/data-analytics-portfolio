# 📊 Projeto 01 — Análise de Vendas e Faturamento

## Problema de negócio

> *Quais categorias, regiões e clientes geram mais receita? Existe sazonalidade no faturamento? Quem são os clientes mais valiosos por região?*

Uma rede varejista americana precisa entender onde concentrar esforços de venda, quais períodos demandam mais estoque e quais clientes merecem atenção especial para retenção.

---

## Dataset

| Item | Detalhe |
|------|---------|
| Fonte | [Kaggle — Superstore Sales Dataset](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting) |
| Volume | 9.800 linhas / 18 colunas |
| Período | Janeiro 2015 a Dezembro 2017 |

---

## Tecnologias

`PostgreSQL 18` `Python 3.13` `Pandas` `psycopg2` `Power BI`

---

## Análises e insights

### 1. Faturamento por categoria e região

```sql
SELECT category, region,
       COUNT(*) AS pedidos,
       ROUND(SUM(sales)::numeric, 2) AS faturamento
FROM vendas_superstore
GROUP BY category, region
ORDER BY faturamento DESC;
```

**Insight:** Technology no East gerou R$ 263.116 com 527 pedidos. Office Supplies no West gerou R$ 217.466 com 1.860 pedidos — 3,5x mais pedidos para um faturamento menor. Ticket médio é o diferencial real.

---

### 2. Sazonalidade — evolução mensal

```sql
SELECT DATE_TRUNC('month', order_date) AS mes,
       ROUND(SUM(sales)::numeric, 2) AS faturamento,
       COUNT(DISTINCT order_id) AS pedidos
FROM vendas_superstore
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY mes;
```

**Insight:** Setembro e Novembro são consistentemente os meses de pico nos 3 anos analisados. Janeiro e Fevereiro apresentam queda expressiva. Padrão previsível que orienta planejamento de estoque e campanhas.

---

### 3. Top 10 produtos por faturamento

```sql
SELECT product_name, category,
       COUNT(*) AS vezes_vendido,
       ROUND(SUM(sales)::numeric, 2) AS faturamento_total,
       ROUND(AVG(sales)::numeric, 2) AS ticket_medio
FROM vendas_superstore
GROUP BY product_name, category
ORDER BY faturamento_total DESC
LIMIT 10;
```

**Insight:** Canon imageCLASS 2200 gerou R$ 61.599 em apenas 5 vendas — ticket médio de R$ 12.319. Cisco TelePresence gerou R$ 22.638 em uma única venda. Produtos de Technology dominam o topo com alto valor por unidade.

---

### 4. Ranking de clientes com Window Function

```sql
SELECT customer_name, segment, region,
       ROUND(SUM(sales)::numeric, 2) AS faturamento_total,
       COUNT(DISTINCT order_id) AS total_pedidos,
       RANK() OVER (ORDER BY SUM(sales) DESC) AS ranking_geral,
       RANK() OVER (PARTITION BY region ORDER BY SUM(sales) DESC) AS ranking_por_regiao
FROM vendas_superstore
GROUP BY customer_name, segment, region
ORDER BY faturamento_total DESC
LIMIT 15;
```

**Insight:** Sean Miller (#1 geral) gerou R$ 23.669 em apenas 2 pedidos — perfil de alto valor e baixa frequência. O `PARTITION BY region` permite identificar o cliente mais valioso dentro de cada região, viabilizando estratégias de retenção segmentadas por mercado.

---

## Conclusões

- **Technology** lidera faturamento apesar do menor volume de pedidos — ticket médio é o fator decisivo
- **Setembro e Novembro** são meses de pico consistentes — oportunidade para campanhas antecipadas
- **Janeiro e Fevereiro** são os mais fracos — ideal para ações de reativação de clientes
- **Top 15 clientes** concentram parte relevante da receita — programa de fidelização é estratégico
- **West e East** são as regiões mais lucrativas em todas as categorias

---

## Como reproduzir

```bash
# 1. Instale as dependências
pip install pandas psycopg2-binary

# 2. Configure o PostgreSQL e crie o banco
psql -U postgres -c "CREATE DATABASE estudos_dados;"

# 3. Execute a importação
python importar.py

# 4. Rode as queries
psql -U postgres -d estudos_dados -f sql/analises.sql
```

---

[← Voltar ao portfólio](../README.md)
