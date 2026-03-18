# 📊 Data Analytics Portfolio — Lucas Rezende

Portfólio de projetos em Análise de Dados com foco em SQL, Python e Power BI.  
Background em indústria (General Motors, MWM Motores) e marketing digital (Coders).

[![LinkedIn](https://img.shields.io/badge/LinkedIn-lucas--rzd-blue)](https://www.linkedin.com/in/lucas-rzd/)
[![GitHub](https://img.shields.io/badge/GitHub-data--analytics--portfolio-black)](https://github.com/lucas-rzd/data-analytics-portfolio)

---

## 🗂️ Projetos

| # | Projeto | Ferramentas | Linhas | Status |
|---|---------|-------------|--------|--------|
| 01 | [Análise de Vendas e Faturamento](#projeto-01--análise-de-vendas-e-faturamento) | SQL · Python · Power BI | 9.800 | ✅ Concluído |
| 02 | [Manutenção Preditiva Industrial](#projeto-02--manutenção-preditiva-industrial) | SQL · Python · Power BI | 10.000 | ✅ Concluído |
| 03 | [Performance de Marketing Digital](#projeto-03--performance-de-marketing-digital) | SQL · Python · Looker Studio | 200.000 | ✅ Concluído |

---

## Projeto 01 — Análise de Vendas e Faturamento

### Problema de negócio
> *Quais categorias, regiões e clientes geram mais receita? Existe sazonalidade no faturamento? Quem são os clientes mais valiosos por região?*

### Dataset
- **Fonte:** [Kaggle — Superstore Sales Dataset](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting)
- **Volume:** 9.800 linhas / 18 colunas
- **Período:** Janeiro 2015 a Dezembro 2017

### Tecnologias
`PostgreSQL 18` `Python 3.13` `Pandas` `Power BI`

### Análises realizadas

**1. Faturamento por categoria e região**
```sql
SELECT category, region, COUNT(*) AS pedidos,
       ROUND(SUM(sales)::numeric, 2) AS faturamento
FROM vendas_superstore
GROUP BY category, region
ORDER BY faturamento DESC;
```
> Technology no East gerou R$ 263.116 com 527 pedidos, enquanto Office Supplies no West gerou R$ 217.466 com 1.860 pedidos — 3,5x mais pedidos para um faturamento menor.

**2. Sazonalidade — evolução mensal**
```sql
SELECT DATE_TRUNC('month', order_date) AS mes,
       ROUND(SUM(sales)::numeric, 2) AS faturamento,
       COUNT(DISTINCT order_id) AS pedidos
FROM vendas_superstore
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY mes;
```
> Setembro e Novembro são consistentemente os meses de pico nos 3 anos. Janeiro e Fevereiro apresentam queda expressiva — padrão sazonal previsível.

**3. Top 10 produtos por faturamento**
```sql
SELECT product_name, category, COUNT(*) AS vezes_vendido,
       ROUND(SUM(sales)::numeric, 2) AS faturamento_total,
       ROUND(AVG(sales)::numeric, 2) AS ticket_medio
FROM vendas_superstore
GROUP BY product_name, category
ORDER BY faturamento_total DESC LIMIT 10;
```
> Canon imageCLASS 2200 gerou R$ 61.599 em apenas 5 vendas — ticket médio de R$ 12.319.

**4. Ranking de clientes com Window Function**
```sql
SELECT customer_name, segment, region,
       ROUND(SUM(sales)::numeric, 2) AS faturamento_total,
       RANK() OVER (ORDER BY SUM(sales) DESC) AS ranking_geral,
       RANK() OVER (PARTITION BY region ORDER BY SUM(sales) DESC) AS ranking_por_regiao
FROM vendas_superstore
GROUP BY customer_name, segment, region
ORDER BY faturamento_total DESC LIMIT 15;
```
> Sean Miller (Home Office / South) é o cliente #1 com R$ 23.669 em apenas 2 pedidos. O PARTITION BY permite identificar os clientes mais valiosos dentro de cada região.

### Principais conclusões
- Technology é a categoria de maior faturamento apesar do menor volume de pedidos
- Setembro e Novembro são os meses de pico — sazonalidade consistente nos 3 anos
- Top 15 clientes concentram parte relevante do faturamento — oportunidade de fidelização
- West e East são as regiões de maior receita em todas as categorias

---

## Projeto 02 — Manutenção Preditiva Industrial

### Problema de negócio
> *Quais são os principais fatores que causam falhas em máquinas industriais? Existe um ponto crítico de desgaste onde o risco de falha aumenta significativamente?*

### Contexto
Projeto com conexão direta ao histórico profissional na **General Motors** (análise de MTTR, downtime e métricas produtivas) e **MWM Motores e Geradores** (integração eletromecânica e análise de painéis com CLP).

### Dataset
- **Fonte:** [Kaggle — AI4I 2020 Predictive Maintenance Dataset](https://www.kaggle.com/datasets/stephanmatzka/predictive-maintenance-dataset-ai4i-2020)
- **Volume:** 10.000 linhas / 14 colunas
- **Variáveis:** temperatura, RPM, torque, desgaste de ferramenta e 5 modos de falha

### Tecnologias
`PostgreSQL 18` `Python 3.13` `Pandas` `Power BI`

### Análises realizadas

**1. Taxa de falha por tipo de produto**
```sql
SELECT type AS tipo_produto, COUNT(*) AS total_registros,
       SUM(machine_failure) AS total_falhas,
       ROUND(AVG(machine_failure) * 100, 2) AS percentual_falha
FROM manutencao_preditiva
GROUP BY type ORDER BY percentual_falha DESC;
```
> Produtos de baixa qualidade (L) têm taxa de falha de 3,92% vs 2,09% para alta qualidade (H).

**2. Distribuição por tipo de falha**
```sql
SELECT 'HDF - Dissipação de calor' AS tipo_falha, SUM(hdf) AS total FROM manutencao_preditiva
UNION ALL SELECT 'OSF - Sobrecarga', SUM(osf) FROM manutencao_preditiva
UNION ALL SELECT 'PWF - Falha de potência', SUM(pwf) FROM manutencao_preditiva
UNION ALL SELECT 'TWF - Desgaste de ferramenta', SUM(twf) FROM manutencao_preditiva
UNION ALL SELECT 'RNF - Falha aleatória', SUM(rnf) FROM manutencao_preditiva
ORDER BY total DESC;
```
> HDF (dissipação de calor) é a causa mais frequente com 115 ocorrências.

**3. Parâmetros médios: falha vs operação normal**
```sql
SELECT machine_failure AS falhou, COUNT(*) AS registros,
       ROUND(AVG(torque_nm)::numeric, 2) AS torque_medio,
       ROUND(AVG(tool_wear_min)::numeric, 0) AS desgaste_medio,
       ROUND(AVG(rotational_speed_rpm)::numeric, 0) AS rpm_medio
FROM manutencao_preditiva
GROUP BY machine_failure;
```
> Máquinas que falharam operavam com torque 27% mais alto (50,17 vs 39,63 Nm) e desgaste 35% maior (144 vs 107 min).

**4. Ponto crítico de desgaste identificado**
```sql
SELECT CASE WHEN tool_wear_min BETWEEN 0 AND 50 THEN '0-50 min'
            WHEN tool_wear_min BETWEEN 51 AND 100 THEN '51-100 min'
            WHEN tool_wear_min BETWEEN 101 AND 150 THEN '101-150 min'
            WHEN tool_wear_min BETWEEN 151 AND 200 THEN '151-200 min'
            ELSE 'Acima de 200 min' END AS faixa_desgaste,
       COUNT(*) AS total, SUM(machine_failure) AS falhas,
       ROUND(AVG(machine_failure) * 100, 2) AS percentual_falha
FROM manutencao_preditiva
GROUP BY faixa_desgaste ORDER BY MIN(tool_wear_min);
```
> **Descoberta crítica:** taxa de falha estável entre 2,17% e 2,90% até 200 minutos. Acima de 200 minutos salta para 15,49% — quase 7x maior. Substituir a ferramenta antes de 200 minutos elimina a maior parte das falhas evitáveis.

### Principais conclusões
- Ponto de ruptura claro em 200 minutos de desgaste — base para política de manutenção preventiva
- Torque excessivo combinado com ferramenta desgastada é o principal fator de falha
- HDF e OSF juntos respondem por mais de 60% das falhas
- Produtos de baixa qualidade demandam monitoramento mais frequente

---

## Projeto 03 — Performance de Marketing Digital

### Problema de negócio
> *Quais tipos de campanha e canais geram melhor ROI? Existe variação de performance por segmento de cliente ou duração da campanha?*

### Contexto
Projeto com conexão direta ao histórico profissional na **Coders** (monitoramento de CAC, ROAS, CPL e taxa de conversão em campanhas digitais).

### Dataset
- **Fonte:** [Kaggle — Marketing Campaign Performance Dataset](https://www.kaggle.com/datasets/manishabhatt22/marketing-campaign-performance-dataset)
- **Volume:** 200.000 linhas / 16 colunas
- **Nota:** Dataset sintético com distribuição uniforme — projeto focado em demonstrar domínio técnico com grandes volumes de dados.

### Tecnologias
`PostgreSQL 18` `Python 3.13` `Pandas` `Looker Studio`

### Análises realizadas
- ROI e taxa de conversão por tipo de campanha
- Performance por canal e segmento de cliente
- Evolução mensal de investimento e ROI
- Impacto da duração da campanha na performance

### Aprendizado técnico
Importação em lotes de 200.000 registros com Python, limpeza de campos monetários com caracteres especiais, análises temporais e de segmentação com SQL em grande volume de dados.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso |
|------------|-----|
| PostgreSQL 18 | Banco de dados relacional |
| Python 3.13 | Ingestão e limpeza de dados |
| Pandas | Manipulação de dataframes |
| psycopg2 | Conexão Python → PostgreSQL |
| Power BI | Dashboards e visualizações |
| Looker Studio | Visualizações web |
| Git / GitHub | Versionamento de código |
| VSCode | Ambiente de desenvolvimento |

---

## 📁 Estrutura do repositório

```
data-analytics-portfolio/
├── projeto-01-vendas/
│   ├── data/raw/          
│   ├── sql/analises.sql   
│   ├── importar.py        
│   └── README.md
├── projeto-02-manutencao/
│   ├── data/raw/
│   ├── sql/analises.sql
│   ├── importar.py
│   └── README.md
├── projeto-03-marketing/
│   ├── data/raw/
│   ├── sql/analises.sql
│   ├── importar.py
│   └── README.md
└── README.md
```

---

## 👤 Sobre mim

Analista de Dados com background em indústria e marketing digital. Experiência real com métricas produtivas (MTTR, downtime, OEE) na General Motors e métricas digitais (CAC, ROAS, CPL) na Coders. Cursando Bacharelado em Matemática e Ciência da Computação.

**Objetivo:** Analista de Dados Jr/Pl com evolução para Engenharia de Dados.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-lucas--rzd-blue)](https://www.linkedin.com/in/lucas-rzd/)
