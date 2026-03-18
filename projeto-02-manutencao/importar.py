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
df = pd.read_csv(r"C:\Users\Lucas Rezende\Desktop\projeto-data\projeto-02-manutencao\data\raw\ai4i2020.csv")

# Padronizar nomes das colunas
df.columns = (
    df.columns
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("[", "", regex=False)
    .str.replace("]", "", regex=False)
    .str.replace("/", "_")
)

print("Colunas padronizadas:")
print(df.columns.tolist())

# Criar tabela
cursor.execute("""
    DROP TABLE IF EXISTS manutencao_preditiva;
    CREATE TABLE manutencao_preditiva (
        udi                     INT,
        product_id              VARCHAR(20),
        type                    VARCHAR(5),
        air_temperature_k       DECIMAL(6,1),
        process_temperature_k   DECIMAL(6,1),
        rotational_speed_rpm    INT,
        torque_nm               DECIMAL(6,1),
        tool_wear_min           INT,
        machine_failure         INT,
        twf                     INT,
        hdf                     INT,
        pwf                     INT,
        osf                     INT,
        rnf                     INT
    );
""")

# Importar dados
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO manutencao_preditiva VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

conn.commit()
print(f"Importação concluída! {len(df)} linhas inseridas.")

cursor.close()
conn.close()