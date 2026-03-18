# 🔧 Projeto 02 — Manutenção Preditiva Industrial

## Problema de negócio

> *Quais são os principais fatores que causam falhas em máquinas industriais? Existe um ponto crítico de desgaste onde o risco de falha aumenta significativamente?*

Uma indústria de manufatura precisa reduzir paradas não planejadas. O objetivo é identificar padrões nos dados de sensores que precedem falhas, permitindo manutenção preventiva antes que o problema ocorra.

---

## Contexto profissional

Este projeto conecta diretamente com experiência real na **General Motors** — onde métricas como MTTR, MCBF e downtime eram monitoradas diariamente — e na **MWM Motores e Geradores** — onde análise de painéis elétricos e lógica de CLP faziam parte da rotina operacional.

---

## Dataset

| Item | Detalhe |
|------|---------|
| Fonte | [Kaggle — AI4I 2020 Predictive Maintenance Dataset](https://www.kaggle.com/datasets/stephanmatzka/predictive-maintenance-dataset-ai4i-2020) |
| Volume | 10.000 linhas / 14 colunas |
| Variáveis | Temperatura, RPM, torque, desgaste e 5 modos de falha |

### Colunas principais

| Coluna | Descrição |
|--------|-----------|
| `type` | Qualidade do produto: L (baixa), M (média), H (alta) |
| `air_temperature_k` | Temperatura do ar em Kelvin |
| `process_temperature_k` | Temperatura do processo |
| `rotational_speed_rpm` | Velocidade de rotação |
| `torque_nm` | Torque aplicado em Nm |
| `tool_wear_min` | Desgaste acumulado da ferramenta em minutos |
| `machine_failure` | Falha ocorreu: 1 = sim, 0 = não |
| `twf / hdf / pwf / osf / rnf` | Tipos específicos de falha |

---

## Tecnologias

`PostgreSQL 18` `Python 3.13` `Pandas` `psycopg2` `Power BI`

---

## Análises e insights

### 1. Taxa de falha por qualidade do produto

```sql
SELECT type AS tipo_produto,
       COUNT(*) AS total_registros,
       SUM(machine_failure) AS total_falhas,
       ROUND(AVG(machine_failure) * 100, 2) AS percentual_falha
FROM manutencao_preditiva
GROUP BY type
ORDER BY percentual_falha DESC;
```

| Tipo | Registros | Falhas | Taxa |
|------|-----------|--------|------|
| L (baixa) | 6.000 | 235 | 3,92% |
| M (média) | 2.997 | 83 | 2,77% |
| H (alta) | 1.003 | 21 | 2,09% |

**Insight:** Qualidade do componente impacta diretamente a confiabilidade. Produtos de baixa qualidade falham quase 2x mais que os de alta qualidade.

---

### 2. Distribuição por tipo de falha

```sql
SELECT 'HDF - Dissipação de calor' AS tipo_falha, SUM(hdf) AS total FROM manutencao_preditiva
UNION ALL SELECT 'OSF - Sobrecarga',               SUM(osf) FROM manutencao_preditiva
UNION ALL SELECT 'PWF - Falha de potência',        SUM(pwf) FROM manutencao_preditiva
UNION ALL SELECT 'TWF - Desgaste de ferramenta',   SUM(twf) FROM manutencao_preditiva
UNION ALL SELECT 'RNF - Falha aleatória',          SUM(rnf) FROM manutencao_preditiva
ORDER BY total DESC;
```

| Tipo de falha | Ocorrências |
|---------------|-------------|
| HDF - Dissipação de calor | 115 |
| OSF - Sobrecarga | 98 |
| PWF - Falha de potência | 95 |
| TWF - Desgaste de ferramenta | 46 |
| RNF - Falha aleatória | 19 |

**Insight:** HDF e OSF juntos respondem por 57% das falhas. O sistema de resfriamento e o controle de sobrecarga são os pontos críticos de manutenção.

---

### 3. Parâmetros operacionais: falha vs normal

```sql
SELECT machine_failure AS falhou,
       COUNT(*) AS registros,
       ROUND(AVG(air_temperature_k)::numeric, 2) AS temp_ar_media,
       ROUND(AVG(rotational_speed_rpm)::numeric, 0) AS rpm_medio,
       ROUND(AVG(torque_nm)::numeric, 2) AS torque_medio,
       ROUND(AVG(tool_wear_min)::numeric, 0) AS desgaste_medio
FROM manutencao_preditiva
GROUP BY machine_failure;
```

| Situação | RPM | Torque (Nm) | Desgaste (min) |
|----------|-----|-------------|----------------|
| Normal | 1.540 | 39,63 | 107 |
| Falha | 1.496 | 50,17 | 144 |

**Insight:** Máquinas que falharam operavam com torque 27% mais alto e desgaste 35% maior. Monitorar esses dois parâmetros em tempo real permite antecipar falhas.

---

### 4. Ponto crítico de desgaste — principal descoberta

```sql
SELECT
    CASE
        WHEN tool_wear_min BETWEEN 0   AND 50  THEN '0-50 min'
        WHEN tool_wear_min BETWEEN 51  AND 100 THEN '51-100 min'
        WHEN tool_wear_min BETWEEN 101 AND 150 THEN '101-150 min'
        WHEN tool_wear_min BETWEEN 151 AND 200 THEN '151-200 min'
        ELSE 'Acima de 200 min'
    END AS faixa_desgaste,
    COUNT(*) AS total,
    SUM(machine_failure) AS falhas,
    ROUND(AVG(machine_failure) * 100, 2) AS percentual_falha
FROM manutencao_preditiva
GROUP BY faixa_desgaste
ORDER BY MIN(tool_wear_min);
```

| Faixa de desgaste | Total | Falhas | Taxa de falha |
|-------------------|-------|--------|---------------|
| 0–50 min | 2.396 | 52 | 2,17% |
| 51–100 min | 2.271 | 53 | 2,33% |
| 101–150 min | 2.295 | 50 | 2,18% |
| 151–200 min | 2.276 | 66 | 2,90% |
| **Acima de 200 min** | **762** | **118** | **15,49%** |

**Descoberta crítica:** A taxa de falha permanece estável entre 2,17% e 2,90% até 200 minutos de desgaste. Acima desse limite, a taxa salta para **15,49% — quase 7x maior**.

**Recomendação:** Implementar política de substituição preventiva da ferramenta antes de atingir 200 minutos de uso elimina a maioria das falhas evitáveis, reduzindo downtime e custo de manutenção corretiva.

---

## Conclusões

- Ponto de ruptura claro em **200 minutos** de desgaste — base objetiva para política de manutenção
- **Torque excessivo** combinado com ferramenta desgastada é o principal perfil de risco
- **HDF e OSF** respondem por mais de 57% das falhas — prioridade para investimento em manutenção
- Produtos de **baixa qualidade** demandam monitoramento mais frequente
- Dados de sensores permitem criar alertas preditivos antes que a falha ocorra

---

## Como reproduzir

```bash
# 1. Instale as dependências
pip install pandas psycopg2-binary

# 2. Execute a importação
python importar.py

# 3. Rode as queries
psql -U postgres -d estudos_dados -f sql/analises.sql
```

---

[← Voltar ao portfólio](../README.md)
