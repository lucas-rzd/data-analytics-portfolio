-- PROJETO 01 — Análise de Vendas Superstore
-- Autor: Lucas Rezende
-- Dataset: Kaggle Superstore Sales

-- ================================
-- 1. Faturamento total por categoria e região
-- ================================
SELECT
    category,
    region,
    COUNT(*)                        AS pedidos,
    ROUND(SUM(sales)::numeric, 2)   AS faturamento
FROM vendas_superstore
GROUP BY category, region
ORDER BY faturamento DESC;

-- ================================
-- 2. Evolução de faturamento por mês
-- ================================
SELECT
    DATE_TRUNC('month', order_date)     AS mes,
    ROUND(SUM(sales)::numeric, 2)       AS faturamento,
    COUNT(DISTINCT order_id)            AS pedidos
FROM vendas_superstore
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY mes;

-- ================================
-- 3. Top 10 produtos por faturamento
-- ================================
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

-- ================================
-- 4. Ranking de clientes por faturamento com window function
-- ================================
SELECT
    customer_name,
    segment,
    region,
    ROUND(SUM(sales)::numeric, 2)                           AS faturamento_total,
    COUNT(DISTINCT order_id)                                AS total_pedidos,
    RANK() OVER (ORDER BY SUM(sales) DESC)                  AS ranking_geral,
    RANK() OVER (PARTITION BY region ORDER BY SUM(sales) DESC) AS ranking_por_regiao
FROM vendas_superstore
GROUP BY customer_name, segment, region
ORDER BY faturamento_total DESC
LIMIT 15;