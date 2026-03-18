-- ================================
-- LEFT JOIN — todos os produtos, mesmo sem vendas
-- ================================
SELECT 
    p.nome AS produto,
    COALESCE(SUM(v.quantidade * v.valor_unitario), 0) AS total_vendas
FROM produtos p
LEFT JOIN vendas v 
    ON p.id_produto = v.id_produto
GROUP BY p.id_produto, p.nome
ORDER BY p.nome;

-- ================================
-- SUBQUERY — produtos acima da média de faturamento
-- ================================
SELECT 
    product_name, 
    ROUND(SUM(sales)::numeric, 2) AS total
FROM vendas_superstore
GROUP BY product_name
HAVING SUM(sales) > (
    SELECT AVG(total_por_produto)
    FROM (
        SELECT SUM(sales) AS total_por_produto
        FROM vendas_superstore
        GROUP BY product_name
    ) sub
)
ORDER BY total DESC;

-- ================================
-- CTE — mesma análise com WITH, mais legível
-- ================================
WITH faturamento_por_produto AS (
    SELECT 
        product_name,
        SUM(sales) AS total
    FROM vendas_superstore
    GROUP BY product_name
),
media_geral AS (
    SELECT AVG(total) AS media
    FROM faturamento_por_produto
)
SELECT 
    f.product_name,
    ROUND(f.total::numeric, 2) AS faturamento_total
FROM faturamento_por_produto f, media_geral m
WHERE f.total > m.media
ORDER BY f.total DESC;