import pandas as pd
import psycopg2

# Conexão
conn = psycopg2.connect(
    host="127.0.0.1",
    port=5432,
    database="estudos_dados",
    user="postgres",
    password="Oldsmobile@1979"
)
cursor = conn.cursor()

# Leitura do CSV
df = pd.read_csv(r"C:\Users\Lucas Rezende\Desktop\projeto-data\projeto-03-marketing\data\raw\marketing_campaign_dataset.csv")

# Padronizar colunas
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Converter data
df['date'] = pd.to_datetime(df['date'])

# Limpar acquisition_cost — remover $ e converter para float
df['acquisition_cost'] = df['acquisition_cost'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)

# Limpar duration — remover " days" e converter para int
df['duration'] = df['duration'].str.replace(' days', '', regex=False).astype(int)

print("Amostra após limpeza:")
print(df[['campaign_id', 'acquisition_cost', 'duration', 'conversion_rate', 'roi']].head(3))

# Criar tabela
cursor.execute("""
    DROP TABLE IF EXISTS marketing_campanhas;
    CREATE TABLE marketing_campanhas (
        campaign_id         INT,
        company             VARCHAR(100),
        campaign_type       VARCHAR(50),
        target_audience     VARCHAR(50),
        duration            INT,
        channel_used        VARCHAR(50),
        conversion_rate     DECIMAL(6,4),
        acquisition_cost    DECIMAL(10,2),
        roi                 DECIMAL(8,4),
        location            VARCHAR(100),
        language            VARCHAR(50),
        clicks              INT,
        impressions         INT,
        engagement_score    INT,
        customer_segment    VARCHAR(100),
        date                DATE
    );
""")

# Importar dados em lotes de 1000 para ser mais rápido
batch_size = 1000
total = len(df)
for i in range(0, total, batch_size):
    batch = df.iloc[i:i+batch_size]
    records = [tuple(row) for _, row in batch.iterrows()]
    cursor.executemany("""
        INSERT INTO marketing_campanhas VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, records)
    if (i // batch_size) % 10 == 0:
        print(f"Importando... {min(i+batch_size, total)}/{total} linhas")

conn.commit()
print(f"\nImportação concluída! {total} linhas inseridas.")

cursor.close()
conn.close()