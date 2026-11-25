"""Mede o tempo de resposta da API HortIf.
Uso: python medir_latencia.py https://SEU-SERVICO.onrender.com [repeticoes]
Grava cada medição em resultados_latencia.csv (para usar no artigo)."""
import csv
import os
import statistics
import sys
import time
from datetime import datetime

import requests

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000").rstrip("/")
REPETICOES = int(sys.argv[2]) if len(sys.argv) > 2 else 20
LIMITE_MS = 5000   # meta do artigo: resposta abaixo de 5 segundos
ARQUIVO = "saidas/resultados_latencia.csv"

ENDPOINTS = [
    "/saude",
    "/clima/diario",
    "/clima/diario?forcar=true",   # força nova consulta à Open-Meteo (sem cache)
    "/irrigacao/etc",
]


def medir(caminho):
    inicio = time.perf_counter()
    try:
        r = requests.get(BASE + caminho, timeout=120)
        ok = r.status_code == 200
        servidor = r.headers.get("X-Tempo-Resposta-ms", "")
    except requests.RequestException:
        ok, servidor = False, ""
    total = round((time.perf_counter() - inicio) * 1000)
    return ok, total, servidor


def p95(valores):
    ordenados = sorted(valores)
    return ordenados[min(len(ordenados) - 1, int(len(ordenados) * 0.95))]


def agora():
    return datetime.now().isoformat(timespec="seconds")


def main():
    linhas = []

    # 1ª requisição: se o servidor estava dormindo, é o tempo de partida a frio
    ok, total, servidor = medir("/saude")
    print(f"Primeira requisição (/saude): {total} ms (servidor: {servidor or '-'} ms) ok={ok}")
    linhas.append([agora(), "primeira_requisicao", "/saude", ok, total, servidor])

    for caminho in ENDPOINTS:
        tempos, falhas = [], 0
        for _ in range(REPETICOES):
            ok, total, servidor = medir(caminho)
            linhas.append([agora(), "repeticao", caminho, ok, total, servidor])
            if ok:
                tempos.append(total)
            else:
                falhas += 1
            time.sleep(0.5)

        print(f"\n{caminho}")
        if tempos:
            abaixo = sum(t < LIMITE_MS for t in tempos) / len(tempos) * 100
            print(f"  média {statistics.mean(tempos):.0f} ms | mediana {statistics.median(tempos):.0f} ms | "
                  f"p95 {p95(tempos)} ms | máx {max(tempos)} ms")
            print(f"  abaixo de {LIMITE_MS} ms: {abaixo:.0f}% | falhas: {falhas}/{REPETICOES}")
        else:
            print(f"  todas as {REPETICOES} requisições falharam")

    novo = not os.path.exists(ARQUIVO)
    with open(ARQUIVO, "a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        if novo:
            escritor.writerow(["horario", "tipo", "endpoint", "ok", "total_ms", "servidor_ms"])
        escritor.writerows(linhas)
    print(f"\nMedições gravadas em {ARQUIVO}")


if __name__ == "__main__":
    main()
