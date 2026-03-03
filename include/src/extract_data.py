import requests
import logging
import json


def extract_data_weather(url:str)->dict:

    params = {
        "latitude": -22.9515,
        "longitude": -43.1880,
        "hourly": ["temperature_2m", "relativehumidity_2m", "precipitation"],
        "forecast_days": 16,  # 👈 AQUI! Quantos dias de previsão
        "timezone": "America/Sao_Paulo"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        logging.erro("Erro na conexão")
        raise Exception("Erro na API")

    data = response.json()

    if not data:
        logging.warning("Nenhum dado retornado")
        raise Exception("Resposta vazia")

    logging.info("Dados extraídos com sucesso")

    return data