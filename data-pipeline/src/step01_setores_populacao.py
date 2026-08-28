"""
Passo 1 do pipeline — Radiografia Urbana de Sorocaba
=====================================================

Objetivo: CARREGAR (não inventar) a malha de setores censitários do IBGE para
Sorocaba e os dados de população, e PLOTAR um mapa simples de conferência, só
para confirmarmos visualmente que os dados entraram certo antes de irmos além.

Fonte da geometria (duas opções):
  • PADRÃO — `geobr`: baixa a malha de setores do IBGE direto pelo Python,
    sem download manual. Basta ter internet.
  • ALTERNATIVA — `--shapefile`: usa um shapefile do IBGE que você baixou para
    data/raw/setores_ibge/ (ver data-pipeline/GUIA_DOWNLOAD_IBGE.md).

População: vem do CSV de Agregados por Setor (Censo 2022) em
data/raw/populacao_ibge/. O geobr NÃO fornece população, então essa parte
continua sendo o CSV do IBGE (é opcional: dá para conferir só a malha primeiro).

Regra do projeto — NÃO INVENTAR DADO:
  Se uma fonte falhar ou tiver formato inesperado, o script AVISA com instruções
  claras e para — nunca simula/preenche valores.

Uso:
  python data-pipeline/src/step01_setores_populacao.py                 # geobr, ano 2022
  python data-pipeline/src/step01_setores_populacao.py --ano 2010
  python data-pipeline/src/step01_setores_populacao.py --shapefile     # usa data/raw
  python data-pipeline/src/step01_setores_populacao.py --coluna-pop V0001
  python data-pipeline/src/step01_setores_populacao.py --sem-populacao
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import paths  # módulo local (o diretório do script entra no sys.path automaticamente)

CODIGO_SOROCABA = "3552205"

# Nomes de coluna que já vimos nas fontes do IBGE. O script tenta detectar
# automaticamente; se falhar, lista as colunas disponíveis e explica como
# informar a correta — em vez de adivinhar.
COLS_MUNICIPIO = ["CD_MUN", "CD_GEOCMU", "CD_GEOCODM", "CD_MUNICIP", "code_muni"]
COLS_SETOR_SHP = ["CD_SETOR", "CD_GEOCODI", "CD_GEOCODIGO", "CD_GEOCOD", "code_tract"]
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


def aviso(msg: str) -> None:
    print(f"  \033[33m⚠ {msg}\033[0m")


def erro_e_sair(titulo: str, detalhe: str) -> None:
    print(f"\n\033[31m✗ {titulo}\033[0m\n{detalhe}\n")
    sys.exit(1)


def detectar_coluna(cols, candidatas, o_que: str, contexto: str) -> str:
    for c in candidatas:
        if c in cols:
            return c
    erro_e_sair(
        f"Não consegui identificar a coluna de {o_que} em {contexto}.",
        "Colunas disponíveis:\n    "
        + ", ".join(map(str, cols))
        + "\n\nAjuste a lista de candidatas no topo do script (ou passe a coluna "
        "por argumento, quando aplicável). Não vou adivinhar para não inventar dado.",
    )


# --------------------------------------------------------------------------- #
# Fonte da geometria
# --------------------------------------------------------------------------- #
def carregar_via_geobr(gpd, ano: int, simplificado: bool):
    """Baixa a malha de setores de Sorocaba via geobr (fonte: IBGE)."""
    try:
        import geobr
    except ImportError:
        erro_e_sair(
            "Pacote 'geobr' não instalado.",
            "Instale as dependências do pipeline:\n"
            "    pip install -r data-pipeline/requirements.txt\n"
            "Ou use o shapefile local:  --shapefile",
        )
    print(f"  … baixando malha de setores de Sorocaba via geobr (ano {ano})…")
    try:
        soro = geobr.read_census_tract(
            year=ano, code_tract=CODIGO_SOROCABA,
            simplified=simplificado, show_progress=False,
        )
    except Exception as e:  # rede indisponível, ano inexistente, etc.
        erro_e_sair(
            "Falha ao baixar a malha pelo geobr.",
            f"Detalhe: {type(e).__name__}: {str(e)[:300]}\n\n"
            "Possíveis causas:\n"
            f"  • sem internet ou host do geobr bloqueado;\n"
            f"  • o ano {ano} não tem malha de setores no geobr (tente --ano 2010);\n\n"
            "Alternativa: baixe o shapefile do IBGE e use --shapefile\n"
            f"    {URL_MALHA}",
        )
    if soro is None or len(soro) == 0:
        erro_e_sair(
            "geobr não retornou setores para Sorocaba.",
            f"Código usado: {CODIGO_SOROCABA}, ano {ano}. Tente outro --ano.",
        )
    col_setor = detectar_coluna(soro.columns, COLS_SETOR_SHP,
                                "código do setor", "no retorno do geobr")
    ok(f"Malha baixada via geobr: {len(soro):,} setores em Sorocaba (ano {ano})")
    return soro, col_setor


def carregar_via_shapefile(gpd):
    """Carrega a malha de um shapefile local em data/raw/setores_ibge/."""
    if not paths.RAW_SETORES.exists():
        erro_e_sair(
            "Malha de setores não encontrada.",
            f"Crie a pasta e coloque o shapefile do IBGE dentro dela:\n"
            f"    {paths.RAW_SETORES}\n\n"
            f"Guia de download: data-pipeline/GUIA_DOWNLOAD_IBGE.md\n"
            f"Fonte: {URL_MALHA}",
        )
    shps = sorted(paths.RAW_SETORES.rglob("*.shp"))
    if not shps:
        erro_e_sair(
            "Nenhum arquivo .shp em data/raw/setores_ibge/.",
            f"Descompacte o shapefile do IBGE dentro de:\n    {paths.RAW_SETORES}\n"
            f"(precisa dos arquivos .shp, .dbf, .shx e .prj juntos).",
        )
    shp = shps[0]
    ok(f"Shapefile encontrado: {shp.name}")
    gdf = gpd.read_file(shp)
    ok(f"Arquivo carregado: {len(gdf):,} setores (todos os municípios)")

    col_mun = detectar_coluna(gdf.columns, COLS_MUNICIPIO, "município", "no shapefile")
    gdf[col_mun] = gdf[col_mun].astype(str)
    soro = gdf[gdf[col_mun] == CODIGO_SOROCABA].copy()
    if soro.empty:
        erro_e_sair(
            "Nenhum setor de Sorocaba encontrado na malha.",
            f"A coluna '{col_mun}' não trouxe o código {CODIGO_SOROCABA}. "
            f"Confira se você baixou a malha de SP (ou do Brasil inteiro).",
        )
    col_setor = detectar_coluna(soro.columns, COLS_SETOR_SHP,
                                "código do setor", "no shapefile")
    ok(f"Setores de Sorocaba (cód. {CODIGO_SOROCABA}): {len(soro):,}")
    return soro, col_setor


# --------------------------------------------------------------------------- #
# População (CSV do IBGE)
# --------------------------------------------------------------------------- #
def juntar_populacao(soro, pd, coluna_pop_arg):
    """Junta população do CSV de Agregados por Setor. Retorna nome da coluna usada
    (ou None se não houver CSV)."""
    csvs = sorted(paths.RAW_POPULACAO.rglob("*.csv")) if paths.RAW_POPULACAO.exists() else []
    if not csvs:
        aviso("População não encontrada em data/raw/populacao_ibge/.")
        print(f"    Baixe os Agregados por Setor (Censo 2022) em:\n      {URL_POP}")
        print("    Seguindo só com a malha por enquanto (sem inventar população).")
        return None

    csv = csvs[0]
    try:  # IBGE costuma usar ';' e latin-1
        df = pd.read_csv(csv, sep=";", dtype=str, encoding="latin-1")
    except Exception:
        df = pd.read_csv(csv, dtype=str)
    ok(f"CSV de população: {csv.name} ({len(df):,} linhas)")

    col_setor_csv = detectar_coluna(df.columns, COLS_SETOR_CSV,
                                    "código do setor", "no CSV de população")
    if coluna_pop_arg:
        if coluna_pop_arg not in df.columns:
            erro_e_sair("Coluna de população informada não existe no CSV.",
                        "Colunas disponíveis:\n    " + ", ".join(df.columns))
        col_pop = coluna_pop_arg
    else:
        col_pop = detectar_coluna(df.columns, COLS_POPULACAO,
                                  "população", "no CSV (use --coluna-pop NOME)")

    df[col_setor_csv] = df[col_setor_csv].astype(str).str.strip()
    df["_pop"] = pd.to_numeric(df[col_pop], errors="coerce")
    soro_merged = soro.merge(df[[col_setor_csv, "_pop"]],
                             left_on="CD_SETOR", right_on=col_setor_csv, how="left")
    # devolve as colunas ao gdf original (merge preserva geometria/índice)
    soro["_pop"] = soro_merged["_pop"].values
    casados = soro["_pop"].notna().sum()
    ok(f"População juntada: {casados:,}/{len(soro):,} setores com valor (coluna '{col_pop}')")
    if casados == 0:
        aviso("Nenhum setor casou com o CSV. Verifique se a chave do setor tem o "
              "mesmo formato (15 dígitos) nos dois arquivos.")
    return col_pop


# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(description="Passo 1 — setores + população")
    parser.add_argument("--ano", type=int, default=2022,
                        help="Ano da malha de setores no geobr (padrão: 2022).")
    parser.add_argument("--shapefile", action="store_true",
                        help="Usa shapefile local (data/raw/setores_ibge) em vez do geobr.")
    parser.add_argument("--simplificado", action="store_true",
                        help="Geometria simplificada (mais leve) ao usar o geobr.")
    parser.add_argument("--coluna-pop", help="Nome exato da coluna de população no CSV.")
    parser.add_argument("--sem-populacao", action="store_true",
                        help="Só carrega/plota a malha (sem juntar população).")
    args = parser.parse_args()

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

    # ---- 1. Geometria dos setores -------------------------------------------
    if args.shapefile:
        soro, col_setor = carregar_via_shapefile(gpd)
    else:
        soro, col_setor = carregar_via_geobr(gpd, args.ano, args.simplificado)

    # chave padronizada para todo o restante do pipeline
    soro["CD_SETOR"] = soro[col_setor].astype(str).str.strip()

    # salva a lista de setores (útil para preencher regions.yaml)
    lista_txt = paths.DATA_PROCESSED / "setores_sorocaba.txt"
    lista_txt.write_text("\n".join(sorted(soro["CD_SETOR"])), encoding="utf-8")
    ok(f"Lista de setores salva em: {lista_txt.relative_to(paths.ROOT)}")

    # salva a geometria para os próximos passos reutilizarem
    try:
        gpkg = paths.DATA_PROCESSED / "setores_sorocaba.gpkg"
        soro[["CD_SETOR", "geometry"]].to_file(gpkg, driver="GPKG")
        ok(f"Geometria salva em: {gpkg.relative_to(paths.ROOT)}")
    except Exception as e:
        aviso(f"Não consegui salvar o GeoPackage ({type(e).__name__}); seguindo mesmo assim.")

    # ---- 2. População --------------------------------------------------------
    coluna_pop_usada = None
    if not args.sem_populacao:
        coluna_pop_usada = juntar_populacao(soro, pd, args.coluna_pop)

    # ---- 3. Mapa de conferência ---------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 9))
    tem_pop = coluna_pop_usada and "_pop" in soro and soro["_pop"].notna().any()
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
