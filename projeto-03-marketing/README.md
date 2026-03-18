# 📱 Projeto 03 — Performance de Marketing Digital

## Problema de negócio

> *Quais tipos de campanha e canais geram melhor ROI? Existe variação de performance por segmento de cliente ou duração da campanha?*

Uma empresa de marketing digital precisa entender quais combinações de canal, tipo de campanha e segmento de cliente entregam melhor retorno sobre investimento para orientar a alocação de budget.

---

## Contexto profissional

Este projeto conecta diretamente com experiência real na **Coders** — onde o monitoramento de CAC, ROAS, CPL e taxa de conversão era realizado diariamente para suporte a decisões baseadas em métricas.

---

## Dataset

| Item | Detalhe |
|------|---------|
| Fonte | [Kaggle — Marketing Campaign Performance Dataset](https://www.kaggle.com/datasets/manishabhatt22/marketing-campaign-performance-dataset) |
| Volume | 200.000 linhas / 16 colunas |
| Período | 2021–2022 |
| Nota | Dataset sintético com distribuição uniforme |

### Colunas principais

| Coluna | Descrição |
|--------|-----------|
| `campaign_type` | Tipo de campanha (Email, Social Media, Search, Display, Influencer) |
| `channel_used` | Canal utilizado (Facebook, Google Ads, Instagram, YouTube, etc) |
| `conversion_rate` | Taxa de conversão |
| `acquisition_cost` | Custo de aquisição (CAC) |
| `roi` | Retorno sobre investimento |
| `clicks` | Total de cliques |
| `impressions` | Total de impressões |
| `engagement_score` | Score de engajamento (1–10) |
| `customer_segment` | Segmento do cliente |
| `duration` | Duração da campanha em dias |

---

## Tecnologias

`PostgreSQL 18` `Python 3.13` `Pandas` `psycopg2` `Looker Studio`

---

## Análises realizadas

### 1. ROI e conversão por tipo de campanha

```sql
SELECT campaign_type,
       COUNT(*) AS total_campanhas,
       ROUND(AVG(roi)::numeric, 2) AS roi_medio,
       ROUND(AVG(conversion_rate)::numeric, 4) AS conversao_media,
       ROUND(AVG(acquisition_cost)::numeric, 2) AS cac_medio,
       ROUND(AVG(clicks)::numeric, 0) AS cliques_medios
FROM marketing_campanhas
GROUP BY campaign_type
ORDER BY roi_medio DESC;
```

---

### 2. Performance por canal e segmento de cliente

```sql
SELECT channel_used, customer_segment,
       COUNT(*) AS campanhas,
       ROUND(AVG(roi)::numeric, 2) AS roi_medio,
       ROUND(AVG(conversion_rate)::numeric, 4) AS conversao_media,
       ROUND(SUM(clicks)::numeric, 0) AS total_cliques
FROM marketing_campanhas
GROUP BY channel_used, customer_segment
ORDER BY roi_medio DESC
LIMIT 10;
```

---

### 3. Evolução mensal de ROI e investimento

```sql
SELECT DATE_TRUNC('month', date) AS mes,
       COUNT(*) AS campanhas,
       ROUND(AVG(roi)::numeric, 2) AS roi_medio,
       ROUND(AVG(conversion_rate)::numeric, 4) AS conversao_media,
       ROUND(SUM(acquisition_cost)::numeric, 2) AS investimento_total
FROM marketing_campanhas
GROUP BY DATE_TRUNC('month', date)
ORDER BY mes;
```

---

### 4. Impacto da duração na performance

```sql
SELECT duration AS duracao_dias,
       COUNT(*) AS campanhas,
       ROUND(AVG(roi)::numeric, 2) AS roi_medio,
       ROUND(AVG(conversion_rate)::numeric, 4) AS conversao_media,
       ROUND(AVG(acquisition_cost)::numeric, 2) AS cac_medio,
       ROUND(AVG(engagement_score)::numeric, 2) AS engajamento_medio
FROM marketing_campanhas
GROUP BY duration
ORDER BY roi_medio DESC;
```

---

## Aprendizado técnico

Este projeto foi focado em demonstrar domínio técnico com grandes volumes de dados:

- **Importação em lotes** de 200.000 registros com Python para otimização de performance
- **Limpeza de dados** — remoção de caracteres especiais em campos monetários (`$`) e conversão de tipos
- **Análises temporais** com `DATE_TRUNC` em grande volume
- **Segmentação multi-dimensional** combinando canal, tipo de campanha e segmento de cliente

O dataset é sintético com distribuição uniforme entre categorias — em projetos com dados reais de campanhas, as variações de ROI e conversão entre canais seriam mais expressivas, como observado na experiência prática na Coders.

---

## Como reproduzir

```bash
# 1. Instale as dependências
pip install pandas psycopg2-binary

# 2. Execute a importação (200k linhas — aguarde alguns minutos)
python importar.py

# 3. Rode as queries
psql -U postgres -d estudos_dados -f sql/analises.sql
```

---

[← Voltar ao portfólio](../README.md)
