import os
import pandas as pd
import numpy as np
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

cursor = conn.cursor()

files_and_tables = [
    (r"C:\PhonePe Final Project\Output\agg_transaction.csv", "aggregated_transaction"),
    (r"C:\PhonePe Final Project\Output\agg_user.csv", "aggregated_user"),
    (r"C:\PhonePe Final Project\Output\agg_insurance.csv", "aggregated_insurance"),
    (r"C:\PhonePe Final Project\Output\map_transaction.csv", "map_transaction"),
    (r"C:\PhonePe Final Project\Output\map_user.csv", "map_user"),
    (r"C:\PhonePe Final Project\Output\map_insurance.csv", "map_insurance"),
    (r"C:\PhonePe Final Project\Output\top_transaction.csv", "top_transaction"),
    (r"C:\PhonePe Final Project\Output\top_user.csv", "top_user"),
    (r"C:\PhonePe Final Project\Output\top_insurance.csv", "top_insurance")
]

for file_path, table_name in files_and_tables:
    df = pd.read_csv(file_path)

    # Convert all columns to object first, then replace NaN with None
    df = df.astype(object)
    df = df.replace({np.nan: None})

    cols = ", ".join([f"`{col}`" for col in df.columns])
    placeholders = ", ".join(["%s"] * len(df.columns))
    insert_query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

    data = [tuple(row) for row in df.itertuples(index=False, name=None)]

    cursor.executemany(insert_query, data)
    conn.commit()

    print(f"Data loaded into {table_name}")

cursor.close()
conn.close()

print("All CSV files loaded successfully into MySQL!")