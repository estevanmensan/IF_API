import math
"""
Equação de Penman-Moneith "desmontada" para garantir  
 o calculo correto

"""

# Equação para descobrir a velocidade do vento a 2m como exigido pela equação de Penman-Moneith
def converter_vento_2m(vento_10):
    return vento_10 * (4.87 / math.log(67.8 * 10 -5.42))

def calcular_et0 (temp_media, temp_max, temp_min, 
                umidade_relativa, velocidade_vento, radiacao_solar, altitude=0
                ):

    #es=Pressão de saturação de vapor (KPa)
    es = 0.6108 * math.exp((17.27*temp_media)/(temp_media+237.3))

    #ea=Pressão de saturação de vapor (KPa)
    ea = (es * umidade_relativa)/100

    #delta_e = es - ea
    delta_e = (es-ea)

    #delta = declividade da curva da curva de pressão
    delta = (4098*(es))/((temp_media+237.3)**2)

    #constante psicométrica
    pressao_atm = 101.3 * ((293-0.0065*altitude)/293)**5.26
    gamma = 0.665e-3*pressao_atm

    # calculando pela ET0
    numerador = (0.408*delta*radiacao_solar)+(gamma*(900/(temp_media+273))*velocidade_vento*delta_e)
    denominador = delta + gamma * (1 + 0.34 * velocidade_vento)

    et0 = numerador/denominador
    return(et0)

def calcular_etc(et0, kc):
    return round(et0 * kc, 2)

# kc = Coef de cultura 
KC_POR_CULTURA = {
    "alface": 0.9,
    "tomate": 1.05,
    "couve": 0.95
}

calcular_et0(0,0,0,0,0,0)