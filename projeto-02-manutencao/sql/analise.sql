-- PROJETO 02 — Manutenção Preditiva Industrial
-- Autor: Lucas Rezende
-- Dataset: AI4I 2020 Predictive Maintenance Dataset

-- ================================
-- 1. Visão geral de falhas por tipo de produto
-- ================================
SELECT
    type                                        AS tipo_produto,
    COUNT(*)                                    AS total_registros,
    SUM(machine_failure)                        AS total_falhas,
    ROUND(AVG(machine_failure) * 100, 2)        AS percentual_falha
FROM manutencao_preditiva
GROUP BY type
ORDER BY percentual_falha DESC;

-- ================================
-- 2. Análise de cada tipo de falha
-- ================================
SELECT
    'TWF - Desgaste de ferramenta'  AS tipo_falha, SUM(twf) AS total FROM manutencao_preditiva
UNION ALL
SELECT 'HDF - Dissipação de calor',      SUM(hdf) FROM manutencao_preditiva
UNION ALL
SELECT 'PWF - Falha de potência',        SUM(pwf) FROM manutencao_preditiva
UNION ALL
SELECT 'OSF - Sobrecarga',               SUM(osf) FROM manutencao_preditiva
UNION ALL
SELECT 'RNF - Falha aleatória',          SUM(rnf) FROM manutencao_preditiva
ORDER BY total DESC;

-- ================================
-- 3. Temperatura e rotação média nas falhas vs operação normal
-- ================================
SELECT
    machine_failure                             AS falhou,
    COUNT(*)                                    AS registros,
    ROUND(AVG(air_temperature_k)::numeric, 2)   AS temp_ar_media,
    ROUND(AVG(process_temperature_k)::numeric, 2) AS temp_processo_media,
    ROUND(AVG(rotational_speed_rpm)::numeric, 0) AS rpm_medio,
    ROUND(AVG(torque_nm)::numeric, 2)           AS torque_medio,
    ROUND(AVG(tool_wear_min)::numeric, 0)       AS desgaste_medio
FROM manutencao_preditiva
GROUP BY machine_failure
ORDER BY machine_failure;

-- ================================
-- 4. Taxa de falha por faixa de desgaste da ferramenta
-- ================================
SELECT
    CASE
        WHEN tool_wear_min BETWEEN 0   AND 50  THEN '0-50 min'
        WHEN tool_wear_min BETWEEN 51  AND 100 THEN '51-100 min'
        WHEN tool_wear_min BETWEEN 101 AND 150 THEN '101-150 min'
        WHEN tool_wear_min BETWEEN 151 AND 200 THEN '151-200 min'
        ELSE 'Acima de 200 min'
    END                                         AS faixa_desgaste,
    COUNT(*)                                    AS total,
    SUM(machine_failure)                        AS falhas,
    ROUND(AVG(machine_failure) * 100, 2)        AS percentual_falha,
    ROUND(AVG(torque_nm)::numeric, 2)           AS torque_medio
FROM manutencao_preditiva
GROUP BY faixa_desgaste
ORDER BY MIN(tool_wear_min);