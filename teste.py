import requests
import pandas as pd
from calculo import converter_vento_2m,calcular_et0, calcular_etc, KC_POR_CULTURA

"""
calcular_et0 (temp_media, temp_max, temp_min, 
                umidade_relativa, velocidade_vento, radiacao_solar, altitude=0
                ):
"""

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": -24.49, #latitude de Registro
    "longitude": -47.84, #longitude de Registro
    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,shortwave_radiation",
    "timezone": "America/Sao_Paulo"
}

resp = requests.get(url, params=params)
dados = resp.json()
print(url, params)
print(dados['hourly'])

#definindo os valores para as variaveis
vento_10m = dados["hourly"]["wind_speed_10m"][1]
temp_media = dados["hourly"]["temperature_2m"][1]
umidade_rel = dados["hourly"]["relative_humidity_2m"][1]
radiacao_solar = dados["hourly"]["shortwave_radiation"][1]
kc = KC_POR_CULTURA["alface"]

#definindo os argumentos das funções
vento_2m = converter_vento_2m(vento_10m)
et0 = calcular_et0(temp_media,0, 0,umidade_rel,vento_2m,radiacao_solar,altitude=15)
etc = calcular_etc(et0, kc)

#imprimindo os resultados na tela
print(vento_2m)
print(f"\n{kc}")
print(f"\n{et0}")
print(f"\n{etc}")
