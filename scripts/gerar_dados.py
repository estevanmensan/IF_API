from pathlib import Path


RAIZ = Path(__file__).resolve().parent.parent

df_resultado.to_csv(RAIZ / "saidas" / "resultado_et_hortif.csv", index=False)
df_resultado.to_excel(RAIZ / "saidas" / "resultado_et_hortif.xlsx", index=False)
with open(RAIZ / "docs" / "dados.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False)