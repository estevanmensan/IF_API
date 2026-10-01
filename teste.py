import requests
import pandas as pd
from calculo import converter_vento_2m,calcular_et0, calcular_etc, KC_POR_CULTURA
from data import obtemDados, dictDados, agregar_diario

def main ():
    print("Buscando os dados meteorologicos (in Open-Meteo API)")
    print("[...]\n"*3)
    #variavel para "chamar" os dados da estação
    dados_brutos = obtemDados(past_days=2) 

    print("Tratando a série temporal (interpolação e validação)...")
    #variavel para tratar os dados
    df_tratado = dictDados(dados_brutos)

    print("Agregando por dia...")
    #variavel para agregar os dados por dia
    df_diario = agregar_diario(df_tratado)

    print("Calculando ET0 e ETc para cada dia:")
    lista_resultados = [] #lista para os resultados
    for _, linha in df_diario.iterrows(): #laço de repetição para calculos com os dados do 'df.diario'
        et0 = calcular_et0 ( #calculo da ET0
            temp_media=linha["temperatura"],
            umidade_relativa=linha["umidade_rel"],
            velocidade_vento=linha["vento_2m"],
            radiacao_solar=linha["radiacao_mj"],
        )
        """
            calcular_et0 (temp_media,
                        umidade_relativa, velocidade_vento, radiacao_solar, altitude=0
                    )
        """
        resultado_dia = { #dicionario para armazenar os resultados do dia
            "data": linha["data"],
            "temp_media_C": round(linha["temperatura"], 1),
            "umidade_media_%": round(linha["umidade_rel"], 1),
            "vento_2m_ms": round(linha["vento_2m"], 2),
            "radiacao_MJ_m2": round(linha["radiacao_mj"], 2),
            "ET0_mm_dia": et0,
        }
        for cultura, kc in KC_POR_CULTURA.items(): 
            resultado_dia[f"ETc_{cultura}_mm_dia"] = calcular_etc(et0,kc)

        #armezando o resultado em lista
        lista_resultados.append(resultado_dia)
    df_resultado = pd.DataFrame(lista_resultados)
    pd.set_option("display.width", 140)
    print(df_resultado.to_string(index=False))

    #arquivo .csv
    df_resultado.to_csv("resultado_et_hortif.csv", index=False)
    print("\nResultado salvo em resultado_et_hortif.csv")
    
    

if __name__ == "__main__":
    main()