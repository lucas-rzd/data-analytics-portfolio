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
df = pd.read_csv(r"C:\Users\Lucas Rezende\Desktop\projeto-data\projeto-01-vendas\data\raw\train.csv")

# Padronizar nomes das colunas (minúsculo e sem espaços)
df.columns = [col.lower().replace(" ", "_").replace("-", "_") for col in df.columns]

# Converter datas
df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True)
df['ship_date'] = pd.to_datetime(df['ship_date'], dayfirst=True)

# Criar tabela no banco
cursor.execute("""
    DROP TABLE IF EXISTS vendas_superstore;
    CREATE TABLE vendas_superstore (
        row_id        INT,
        order_id      VARCHAR(20),
        order_date    DATE,
        ship_date     DATE,
        ship_mode     VARCHAR(50),
        customer_id   VARCHAR(20),
        customer_name VARCHAR(100),
        segment       VARCHAR(50),
        country       VARCHAR(50),
        city          VARCHAR(100),
        state         VARCHAR(100),
        postal_code   VARCHAR(20),
        region        VARCHAR(50),
        product_id    VARCHAR(20),
        category      VARCHAR(50),
        sub_category  VARCHAR(50),
        product_name  VARCHAR(255),
        sales         DECIMAL(10,2)
    );
""")

# Importar linha por linha
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO vendas_superstore VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    """, tuple(row))

conn.commit()
print(f"Importação concluída! {len(df)} linhas inseridas.")

cursor.close()
conn.close()