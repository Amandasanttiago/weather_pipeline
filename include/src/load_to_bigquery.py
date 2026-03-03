from google.cloud import bigquery
import pandas as pd
import psycopg2


def load_to_bigquery():

        conn = psycopg2.connect(
            host="postgres_raw",
            database="raw_db",
            user="raw_user",
            password="raw_pass"
        )

        query = """
            SELECT *
            FROM raw_weather
            WHERE ingestion_timestamp >= CURRENT_DATE
        """

        df = pd.read_sql(query, conn)
        conn.close()

        if not df.empty:
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_file(
                "/usr/local/airflow/dags/dbt/weather_project/weatherpipeline-488713-9815ff5675b7.json"
            )

            client = bigquery.Client(
                credentials=credentials,
                project="weatherpipeline-488713"
            )
            table_id = "weatherpipeline-488713.weather_dataset.raw_weather"

            job = client.load_table_from_dataframe(df, table_id)
            job.result()