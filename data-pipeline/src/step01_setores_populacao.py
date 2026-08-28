"""
Passo 1 do pipeline — Radiografia Urbana de Sorocaba
=====================================================

Objetivo: CARREGAR (não inventar) a malha de setores censitários do IBGE para
Sorocaba e os dados de população, e PLOTAR um mapa simples de conferência, só
para confirmarmos visualmente que os dados entraram certo antes de irmos além.

O que este script faz:
  1. Lê o shapefile da malha de setores (data/raw/setores_ibge/).
  2. Filtra apenas os setores de Sorocaba (código IBGE 3552205).
  3. Lê o CSV de população por setor (data/raw/populacao_ibge/) e junta pela
     chave do setor (CD_SETOR, 15 dígitos).
  4. Salva um mapa PNG em data/processed/ e a lista de setores de Sorocaba
     (útil para preencher config/regions.yaml).

Regra do projeto — NÃO INVENTAR DADO:
  Se uma fonte não estiver presente ou tiver formato inesperado, o script AVISA
  com instruções claras e para — nunca simula/preenche valores.

Uso:
  python data-pipeline/src/step01_setores_populacao.py
  python data-pipeline/src/step01_setores_populacao.py --coluna-pop V0001
  python data-pipeline/src/step01_setores_populacao.py --sem-populacao
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import paths  # módulo local (rode a partir de data-pipeline/src ou veja README)

CODIGO_SOROCABA = "3552205"

# Nomes de coluna que já vimos nas fontes do IBGE. O script tenta detectar
# automaticamente; se falhar, ele lista as colunas disponíveis e explica como
# informar a correta — em vez de adivinhar.
COLS_MUNICIPIO = ["CD_MUN", "CD_GEOCMU", "CD_GEOCODM", "CD_MUNICIP"]
COLS_SETOR_SHP = ["CD_SETOR", "CD_GEOCODI", "CD_GEOCODIGO", "CD_GEOCOD"]
COLS_SETOR_CSV = ["CD_SETOR", "CD_GEOCODI", "Cod_setor", "cod_setor", "CD_setor"]
COLS_POPULACAO = ["V0001", "v0001", "POP", "Pop", "populacao", "POPULACAO",
                  "pessoas", "moradores", "PESSOAS"]

URL_MALHA = ("https://www.ibge.gov.br/geociencias/organizacao-do-territorio/"
             "malhas-territoriais/26565-malhas-de-setores-censitarios-"
             "divisoes-intramunicipais.html")
URL_POP = ("https://biblioteca.ibge.gov.br/index.php/biblioteca-catalogo?"
           "view=detalhes&id=2102136")


def ok(msg: str) -> None:
    print(f"  \033[32m✓\033[0m {msg}")


def erro_e_sair(titulo: str, detalhe: str) -> None:
    print(f"\n\033[31m✗ {titulo}\033[0m\n{detalhe}\n")
    sys.exit(1)


def achar_shapefile() -> Path:
    if not paths.RAW_SETORES.exists():
        erro_e_sair(
            "Malha de setores não encontrada.",
            f"Crie a pasta e coloque o shapefile do IBGE dentro dela:\n"
            f"    {paths.RAW_SETORES}\n\n"
            f"Baixe a malha de SETORES CENSITÁRIOS (Censo 2022) de SP/Sorocaba em:\n"
            f"    {URL_MALHA}\n"
            f"Descompacte de forma que exista um arquivo .shp (com .dbf/.shx/.prj juntos).",
        )
    shps = sorted(paths.RAW_SETORES.rglob("*.shp"))
    if not shps:
        erro_e_sair(
            "Nenhum arquivo .shp em data/raw/setores_ibge/.",
            f"Descompacte o shapefile do IBGE dentro de:\n    {paths.RAW_SETORES}\n"
            f"(precisa dos arquivos .shp, .dbf, .shx e .prj juntos).",
        )
    return shps[0]


def detectar_coluna(cols, candidatas, o_que: str, contexto: str) -> str:
    for c in candidatas:
        if c in cols:
            return c
    erro_e_sair(
        f"Não consegui identificar a coluna de {o_que} em {contexto}.",
        "Colunas disponíveis:\n    "
        + ", ".join(map(str, cols))
        + f"\n\nAjuste a lista de candidatas no topo do script (ou passe a coluna "
        f"por argumento, quando aplicável). Não vou adivinhar para não inventar dado.",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Passo 1 — setores + população")
    parser.add_argument("--coluna-pop", help="Nome exato da coluna de população no CSV.")
    parser.add_argument("--sem-populacao", action="store_true",
                        help="Só carrega/plota a malha (sem juntar população).")
    args = parser.parse_args()

    # Import tardio para dar mensagem amigável se o ambiente não estiver montado.
    try:
        import geopandas as gpd
        import pandas as pd
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as e:
        erro_e_sair(
            "Ambiente Python incompleto.",
            f"Faltou instalar dependências ({e.name}). Rode:\n"
            f"    python -m venv .venv && source .venv/bin/activate\n"
            f"    pip install -r data-pipeline/requirements.txt",
        )

    paths.garantir_pastas()
    print("\n== Passo 1: malha de setores + população (Sorocaba) ==\n")

    # ---- 1. Malha de setores -------------------------------------------------
    shp = achar_shapefile()
    ok(f"Shapefile encontrado: {shp.name}")
    gdf = gpd.read_file(shp)
    ok(f"Malha carregada: {len(gdf):,} setores no arquivo (todos os municípios)")

    col_mun = detectar_coluna(gdf.columns, COLS_MUNICIPIO, "município", "no shapefile")
    gdf[col_mun] = gdf[col_mun].astype(str)
    soro = gdf[gdf[col_mun] == CODIGO_SOROCABA].copy()
    if soro.empty:
        erro_e_sair(
            "Nenhum setor de Sorocaba encontrado na malha.",
            f"A coluna '{col_mun}' não trouxe o código {CODIGO_SOROCABA}. "
            f"Confira se você baixou a malha de SP (ou o Brasil inteiro).",
        )
    ok(f"Setores de Sorocaba (cód. {CODIGO_SOROCABA}): {len(soro):,}")

    col_setor = detectar_coluna(soro.columns, COLS_SETOR_SHP, "código do setor", "no shapefile")
    soro[col_setor] = soro[col_setor].astype(str)

    # Salva a lista de setores para ajudar a preencher regions.yaml
    lista_txt = paths.DATA_PROCESSED / "setores_sorocaba.txt"
    lista_txt.write_text("\n".join(sorted(soro[col_setor])), encoding="utf-8")
    ok(f"Lista de setores salva em: {lista_txt.relative_to(paths.ROOT)}")

    # ---- 2. População --------------------------------------------------------
    coluna_pop_usada = None
    if not args.sem_populacao:
        csvs = sorted(paths.RAW_POPULACAO.rglob("*.csv")) if paths.RAW_POPULACAO.exists() else []
        if not csvs:
            print()
            print("  \033[33m⚠ População não encontrada em data/raw/populacao_ibge/.\033[0m")
            print(f"    Baixe os Agregados por Setor (Censo 2022) em:\n      {URL_POP}")
            print("    Seguindo só com a malha por enquanto (sem inventar população).\n")
        else:
            csv = csvs[0]
            # IBGE costuma usar ';' e latin-1; tenta de forma tolerante.
            try:
                df = pd.read_csv(csv, sep=";", dtype=str, encoding="latin-1")
            except Exception:
                df = pd.read_csv(csv, dtype=str)
            ok(f"CSV de população: {csv.name} ({len(df):,} linhas)")

            col_setor_csv = detectar_coluna(df.columns, COLS_SETOR_CSV,
                                            "código do setor", "no CSV de população")
            if args.coluna_pop:
                if args.coluna_pop not in df.columns:
                    erro_e_sair("Coluna de população informada não existe no CSV.",
                                "Colunas disponíveis:\n    " + ", ".join(df.columns))
                col_pop = args.coluna_pop
            else:
                col_pop = detectar_coluna(df.columns, COLS_POPULACAO,
                                          "população", "no CSV (use --coluna-pop NOME)")
            coluna_pop_usada = col_pop

            df[col_setor_csv] = df[col_setor_csv].astype(str)
            df["_pop"] = pd.to_numeric(df[col_pop], errors="coerce")
            soro = soro.merge(df[[col_setor_csv, "_pop"]],
                              left_on=col_setor, right_on=col_setor_csv, how="left")
            casados = soro["_pop"].notna().sum()
            ok(f"População juntada: {casados:,}/{len(soro):,} setores com valor "
               f"(coluna '{col_pop}')")
            if casados == 0:
                print("  \033[33m⚠ Nenhum setor casou com o CSV. Verifique se a chave do "
                      "setor tem o mesmo formato nos dois arquivos.\033[0m")

    # ---- 3. Mapa de conferência ---------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 9))
    tem_pop = coluna_pop_usada and soro["_pop"].notna().any()
    if tem_pop:
        soro.plot(column="_pop", cmap="viridis", linewidth=0.15, edgecolor="white",
                  legend=True, ax=ax, legend_kwds={"label": "População por setor"})
        titulo = "Sorocaba — setores censitários por população (conferência)"
    else:
        soro.boundary.plot(linewidth=0.3, color="#0C6E6C", ax=ax)
        titulo = "Sorocaba — malha de setores censitários (conferência)"
    ax.set_title(titulo, fontsize=13)
    ax.set_axis_off()
    saida = paths.DATA_PROCESSED / "step01_setores_sorocaba.png"
    fig.tight_layout()
    fig.savefig(saida, dpi=150, bbox_inches="tight")
    ok(f"Mapa de conferência salvo em: {saida.relative_to(paths.ROOT)}")

    print("\n\033[32mPasso 1 concluído.\033[0m Abra o PNG acima para conferir "
          "visualmente antes de seguirmos.\n")


if __name__ == "__main__":
    main()
