import requests
from fastapi import FastAPI

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": -24.49,
    "longitude": -47.84,
    #"daily": "temperatura_2m_max,temperature_2m_min",
    "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
    "hourly": "temperature_2m,precipitation_probability",
    "timezone": "America/Sao_Paulo"
}

resp = requests.get(url, params=params)
dados = resp.json()
print(url, params)
#print("Current:")
print(dados["current"])
