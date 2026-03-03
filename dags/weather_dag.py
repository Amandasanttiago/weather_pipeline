# weather_dag.py
from airflow.decorators import task, dag
from datetime import datetime
from include.src.extract_data import extract_data_weather
from include.src.load_raw import load_raw_weather
from include.src.load_to_bigquery import load_to_bigquery  # Corrigido: loado_to_bigquery -> load_to_bigquery
from cosmos import DbtDag, ProjectConfig, DbtTaskGroup, ProfileConfig, ExecutionConfig  # Adicionados ProfileConfig e ExecutionConfig
from include.profiles import airflow_db
from include.constants import weather_path, venv_execution_config


@dag(
    start_date=datetime(2026, 2, 27),
    schedule="@daily",
    catchup=False
)
def weather_pipeline():

    @task
    def extract():
        url = 'https://api.open-meteo.com/v1/forecast'
        return extract_data_weather(url)

    @task
    def load_raw(json_data: dict):
        load_raw_weather(json_data)
    
    @task
    def load_to_bq():
        # Se precisar receber dados do load_raw
        load_to_bigquery()

    dbt_tasks = DbtTaskGroup(
        project_config=ProjectConfig(weather_path),
        profile_config=airflow_db,
        execution_config=venv_execution_config,
    )

    # 🔗 Encadeamento correto
    json_data = extract()
    raw_data = load_raw(json_data)  # Renomeado para clareza
    bq_task = load_to_bq()  # Renomeado para evitar conflito com função importada
    
    json_data >> raw_data >> bq_task >> dbt_tasks


weather_pipeline()