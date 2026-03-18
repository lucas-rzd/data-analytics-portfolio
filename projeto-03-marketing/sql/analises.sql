-- PROJETO 03 — Performance de Marketing Digital
-- Autor: Lucas Rezende
-- Dataset: Marketing Campaign Performance Dataset

-- ================================
-- 1. ROI e taxa de conversão por tipo de campanha
-- ================================
SELECT
    campaign_type,
    COUNT(*)                                    AS total_campanhas,
    ROUND(AVG(roi)::numeric, 2)                 AS roi_medio,
    ROUND(AVG(conversion_rate)::numeric, 4)     AS conversao_media,
    ROUND(AVG(acquisition_cost)::numeric, 2)    AS cac_medio,
    ROUND(AVG(clicks)::numeric, 0)              AS cliques_medios
FROM marketing_campanhas
GROUP BY campaign_type
ORDER BY roi_medio DESC;

-- ================================
-- 2. Performance por canal e segmento de cliente
-- ================================
SELECT
    channel_used,
    customer_segment,
    COUNT(*)                                    AS campanhas,
    ROUND(AVG(roi)::numeric, 2)                 AS roi_medio,
    ROUND(AVG(conversion_rate)::numeric, 4)     AS conversao_media,
    ROUND(SUM(clicks)::numeric, 0)              AS total_cliques
FROM marketing_campanhas
GROUP BY channel_used, customer_segment
ORDER BY roi_medio DESC
LIMIT 10;

-- ================================
-- 3. Evolução mensal de ROI e investimento
-- ================================
SELECT
    DATE_TRUNC('month', date)                   AS mes,
    COUNT(*)                                    AS campanhas,
    ROUND(AVG(roi)::numeric, 2)                 AS roi_medio,
    ROUND(AVG(conversion_rate)::numeric, 4)     AS conversao_media,
    ROUND(SUM(acquisition_cost)::numeric, 2)    AS investimento_total
FROM marketing_campanhas
GROUP BY DATE_TRUNC('month', date)
ORDER BY mes;

-- ================================
-- 4. Relação entre duração da campanha e performance
-- ================================
SELECT
    duration                                    AS duracao_dias,
    COUNT(*)                                    AS campanhas,
    ROUND(AVG(roi)::numeric, 2)                 AS roi_medio,
    ROUND(AVG(conversion_rate)::numeric, 4)     AS conversao_media,
    ROUND(AVG(acquisition_cost)::numeric, 2)    AS cac_medio,
    ROUND(AVG(engagement_score)::numeric, 2)    AS engajamento_medio
FROM marketing_campanhas
GROUP BY duration
ORDER BY roi_medio DESC;