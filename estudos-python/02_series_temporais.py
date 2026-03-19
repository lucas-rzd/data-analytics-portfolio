import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ================================
# Conexão
# ================================
senha = quote_plus("Oldsmobile@1979")
engine = create_engine(f'postgresql://postgres:{senha}@127.0.0.1:5432/estudos_dados')

# ================================
# Leitura e preparação dos dados
# ================================
df = pd.read_sql("SELECT order_date, sales FROM vendas_superstore", engine)

# Converter order_date para datetime
df['order_date'] = pd.to_datetime(df['order_date'])

# Criar coluna mês/ano
df['mes_ano'] = df['order_date'].dt.to_period('M')

# ================================
# Agrupamento mensal
# ================================
vendas_mensais = df.groupby('mes_ano')['sales'].sum().reset_index()
vendas_mensais.columns = ['mes_ano', 'faturamento']
vendas_mensais['mes_ano'] = vendas_mensais['mes_ano'].astype(str)

print("=== EVOLUÇÃO MENSAL DE VENDAS ===")
print(vendas_mensais.to_string())

# ================================
# Mês com maior e menor faturamento
# ================================
mes_max = vendas_mensais.loc[vendas_mensais['faturamento'].idxmax()]
mes_min = vendas_mensais.loc[vendas_mensais['faturamento'].idxmin()]

print(f"\nMês com MAIOR faturamento: {mes_max['mes_ano']} — R$ {mes_max['faturamento']:,.2f}")
print(f"Mês com MENOR faturamento: {mes_min['mes_ano']} — R$ {mes_min['faturamento']:,.2f}")

# ================================
# Gráfico de linha
# ================================
os.makedirs('estudos-python/outputs', exist_ok=True)

plt.figure(figsize=(14, 5))
plt.plot(vendas_mensais['mes_ano'], vendas_mensais['faturamento'], marker='o', color='#2196F3', linewidth=2)
plt.title('Evolução mensal de faturamento — 2015 a 2017')
plt.xlabel('Mês')
plt.ylabel('Faturamento (R$)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('estudos-python/outputs/grafico_evolucao_mensal.png')
plt.show()
print("\nGráfico salvo em estudos-python/outputs/grafico_evolucao_mensal.png")