import time

import pandas as pd
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from app.pipeline import processar_clima

app = FastAPI(title="API HortIf")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Tempo-Resposta-ms"],
)


@app.middleware("http")
async def medir_tempo(request: Request, call_next):
    """Acrescenta em toda resposta o tempo gasto no servidor (ms)."""
    inicio = time.perf_counter()
    resposta = await call_next(request)
    resposta.headers["X-Tempo-Resposta-ms"] = f"{(time.perf_counter() - inicio) * 1000:.0f}"
    return resposta


def _processar(dias: int, forcar: bool) -> dict:
    try:
        return processar_clima(dias, forcar)
    except requests.RequestException as erro:
        raise HTTPException(status_code=502, detail=f"Falha ao consultar a Open-Meteo: {erro}")


@app.get("/saude")
def saude():
    """Resposta imediata, sem chamadas externas: mede só servidor + rede."""
    return {"status": "ok"}


@app.get("/clima/diario")
def clima_diario(dias: int = 7, forcar: bool = False):
    return _processar(dias, forcar)["historico"]


@app.get("/clima/horario")
def clima_horario(dias: int = 2, horas: int = 24, forcar: bool = False):
    """Últimas `horas` leituras horárias já ocorridas (a série traz também horas futuras de hoje)."""
    registros = _processar(dias, forcar)["horario"]
    agora = pd.Timestamp.now(tz="America/Sao_Paulo").tz_localize(None)
    passadas = [r for r in registros if pd.Timestamp(r["timestamp"]) <= agora]
    return passadas[-horas:]


@app.get("/irrigacao/etc")
def irrigacao_etc(dias: int = 7, forcar: bool = False):
    return _processar(dias, forcar)["etc"]


@app.get("/diagnostico")
def diagnostico(dias: int = 7):
    """Mostra de onde vieram os dados (cache ou Open-Meteo) e quanto tempo cada etapa levou."""
    return _processar(dias, False)["meta"]