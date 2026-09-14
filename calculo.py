import math

# ETC = ET0  KC 
#ET0 = a / b
# a = 

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
    gamma = 0,665e-3*pressao_atm

    # calculando pela ET0
    numerador = (0,408*delta*radiacao_solar)+(gamma)
    denominador = delta 