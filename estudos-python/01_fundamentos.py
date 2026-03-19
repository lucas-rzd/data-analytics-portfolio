import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ================================
# Conexão com SQLAlchemy
# ================================
senha = quote_plus("Oldsmobile@1979")
engine = create_engine(f'postgresql://postgres:{senha}@127.0.0.1:5432/estudos_dados')

# ================================
# Leitura dos dados com Pandas
# ================================
query = "SELECT * FROM vendas_superstore"
df = pd.read_sql(query, engine)

# ================================
# Explorando o DataFrame
# ================================
print("=== SHAPE (linhas, colunas) ===")
print(df.shape)

print("\n=== PRIMEIRAS 5 LINHAS ===")
print(df.head())

print("\n=== TIPOS DE DADOS ===")
print(df.dtypes)

print("\n=== ESTATÍSTICAS BÁSICAS ===")
print(df.describe())

# ================================
# Filtragem — só vendas acima de 1000
# ================================
vendas_altas = df[df['sales'] > 1000]
print(f"\nVendas acima de R$ 1.000: {len(vendas_altas)} registros")
print(vendas_altas[['product_name', 'sales', 'category']].head(10))

# ================================
# Agrupamento — faturamento por categoria
# ================================
fat_categoria = df.groupby('category')['sales'].sum().reset_index()
fat_categoria.columns = ['categoria', 'faturamento']
fat_categoria = fat_categoria.sort_values('faturamento', ascending=False)
print("\n=== FATURAMENTO POR CATEGORIA ===")
print(fat_categoria)

# ================================
# Gráfico — faturamento por categoria
# ================================
os.makedirs('estudos-python/outputs', exist_ok=True)

plt.figure(figsize=(8, 5))
plt.bar(fat_categoria['categoria'], fat_categoria['faturamento'], color=['#2196F3', '#4CAF50', '#FF9800'])
plt.title('Faturamento total por categoria')
plt.xlabel('Categoria')
plt.ylabel('Faturamento (R$)')
plt.tight_layout()
plt.savefig('estudos-python/outputs/grafico_categorias.png')
plt.show()
print("\nGráfico salvo em estudos-python/outputs/grafico_categorias.png")