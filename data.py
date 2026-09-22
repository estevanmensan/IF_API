import pandas as pd
import requests
from calculo import converter_vento_2m

def obtemDados(past_days: int=2) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -24.49, #latitude de Registro
        "longitude": -47.84, #longitude de Registro
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,shortwave_radiation",
        "timezone": "America/Sao_Paulo",
        "past_days": past_days
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()

    return resp.json()


def dictDados(dados_brutos):

    #variavel para armazenar o dicionário das variáveis
    hourly = dados_brutos["hourly"]

    #dataframe para os dados
    meteoDF = pd.DataFrame ({
        "timestamps": pd.to_datetime(hourly["time"]),
        "temperatura": hourly["temperature_2m"],
        "umidade_relativa": hourly["relative_humidity_2m"],
        "vento_10m": hourly["wind_speed_10m"],
        "radiacao_wm2": hourly["shortwave_radiation"],
    })
    
    #transforma o U_10m em U_2m (velocidade do vento // wind speed)
    meteoDF["vento_2m"] = meteoDF["vento_10m"].apply(converter_vento_2m)

    #tratamento de lacunas
    colunas_numericas = ["temperatura", "umidade_relativa", 
                        "vento_2m", "radiacao_wm2"]
    meteoDF[colunas_numericas] = meteoDF[colunas_numericas].interpolate(method="linear").bfill().ffill()
    """
    O interpolate irá interpolar os valores que estiverem nulos na lista
    .bfill (Backward fill): em casos onde o valor nulo está no começo da série, este comando "olha pra frente"
                    e copia o próximo valor válido
    .ffill (Forward fill): quando o nulo está no final, o comando "olha para trás" e repete o último
                    valor válido pra frente
    """
    return meteoDF
dados_brutos = obtemDados()
dictDados(dados_brutos)