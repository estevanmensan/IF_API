import requests
import pandas as pd
from calculo import converter_vento_2m,calcular_et0, calcular_etc, KC_POR_CULTURA
from data import obtemDados, dictDados, agregar_diario

def main ():
    print("Buscando os dados meteorologicos (in Open-Meteo API)")
    print("[...]\n"*3)
    dados_brutos = obtemDados(past_days=2)

    print("Tratando a série temporal (interpolação e validação)...")
    df_tratado = dictDados(dados_brutos)

    print("Agregando por dia...")
    df_diario = agregar_diario(df_tratado)

    print("Calculando ET0 e ETc para cada dia:")
    lista_resultados = []
    for _, linha in df_diario.iterrows():
        et0 = calcular_et0 (
            temp_media=linha["temperatura"],
            umidade_relativa=linha["umidade_relativa"],
            velocidade_vento=linha["vento_2m"],
            radiacao_solar=linha["radiacao_mj"],
        )
    """
    calcular_et0 (temp_media,
                umidade_relativa, velocidade_vento, radiacao_solar, altitude=0
            )
    """
    #resultado_dia

if __name__ == "__main__":
    main()