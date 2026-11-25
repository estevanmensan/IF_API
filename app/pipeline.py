"""Orquestra o fluxo: Open-Meteo -> tratamento -> série horária + agregação diária -> ET0/ETc.
Devolve os dados prontos (não grava arquivos) e guarda um cache em memória."""
import time
from datetime import datetime, timezone

from app.data import obtemDados, dictDados, agregar_diario
from app.calculo import calcular_et0, KC_POR_CULTURA

ALTITUDE = 20          # altitude do HortIf em metros (ajustar)
CACHE_SEGUNDOS = 600   # 10 min; a Open-Meteo atualiza os dados de hora em hora

_cache = {}


def processar_clima(dias: int = 7, forcar: bool = False) -> dict:
    guardado = _cache.get(dias)
    if guardado and not forcar and time.time() - guardado["quando"] < CACHE_SEGUNDOS:
        resultado = dict(guardado["resultado"])
        resultado["meta"] = {**resultado["meta"], "origem": "cache"}
        return resultado

    t0 = time.perf_counter()
    bruto = obtemDados(dias)                       # chamada à Open-Meteo
    t1 = time.perf_counter()

    horario = dictDados(bruto)                     # uma linha por hora (já tratada)
    diario = agregar_diario(horario).round(2)
    diario["data"] = diario["data"].astype(str)
    diario["et0"] = diario.apply(
        lambda l: calcular_et0(l["temperatura"], l["umidade_rel"],
                               l["vento_2m"], l["radiacao_mj"], ALTITUDE),
        axis=1,
    )
    horas = horario[["timestamp", "temperatura", "umidade_relativa",
                     "vento_2m", "radiacao_wm2"]].copy()
    horas["timestamp"] = horas["timestamp"].astype(str)
    t2 = time.perf_counter()

    resultado = {
        "historico": diario.to_dict(orient="records"),
        "horario": horas.round(2).to_dict(orient="records"),
        "etc": {"et0": float(diario["et0"].iloc[-1]), "culturas": KC_POR_CULTURA},
        "meta": {
            "origem": "open-meteo",
            "open_meteo_ms": round((t1 - t0) * 1000),
            "processamento_ms": round((t2 - t1) * 1000),
            "atualizado_em": datetime.now(timezone.utc).isoformat(),
        },
    }
    _cache[dias] = {"quando": time.time(), "resultado": resultado}
    return resultado