# include/profiles.py
from cosmos import ProfileConfig
from cosmos.profiles.bigquery import GoogleCloudServiceAccountFileProfileMapping


airflow_db = ProfileConfig(
    profile_name="weather_project",
    target_name="dev",
    profile_mapping=GoogleCloudServiceAccountFileProfileMapping(
        conn_id="my_google_cloud_platform_connection",
        profile_args={
            "project": "weatherpipeline-488713",
            "dataset": "data_weather",
            "keyfile": "/usr/local/airflow/dags/dbt/weather_project/weatherpipeline-488713-9815ff5675b7.json"
        }
    ),
)