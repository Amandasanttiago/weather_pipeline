#load_raw.py
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

# Conexão dentro do Docker
user = "raw_user"
password = "raw_pass"
database = "raw_db"
host = "postgres_raw"

def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:5432/{database}"
    )

engine = get_engine()

# 🔹 1️⃣ Criar tabela RAW automaticamente
def create_raw_table():
    logging.info("→ Verificando existência da tabela raw_weather")

    query = text("""
        CREATE TABLE IF NOT EXISTS raw_weather (
            id SERIAL PRIMARY KEY,
            data JSONB NOT NULL,
            ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    with engine.begin() as conn:
        conn.execute(query)

    logging.info("✓ Tabela raw_weather pronta")

# 🔹 2️⃣ Inserir dados na RAW
def load_raw_weather(json_data: dict):
    create_raw_table()

    logging.info("→ Inserindo dados na camada RAW")

    insert_query = text("""
        INSERT INTO raw_weather (data, ingestion_timestamp)
        VALUES (:data, :ingestion_timestamp)
    """)

    with engine.begin() as conn:
        conn.execute(
            insert_query,
            {
                "data": json.dumps(json_data),
                "ingestion_timestamp": datetime.utcnow()
            }
        )

    logging.info("✅ Dados inseridos na RAW com sucesso")
