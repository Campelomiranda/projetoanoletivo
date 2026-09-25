"""
Passo 2 do pipeline — CityLens · Radiografia Urbana de Sorocaba
==============================================================

Objetivo: atribuir cada SETOR CENSITÁRIO do IBGE (gerado no passo 1) a uma das
6 ZONAS OFICIAIS de Sorocaba, para que o índice possa ser calculado por zona.

Como decidimos a zona de cada setor — método "nearest_bairro":
  1. Lemos os bairros de cada zona em config/regions.yaml (transcritos do mapa
     oficial de zoneamento da Prefeitura/Urbes).
  2. Geocodificamos cada bairro (Nominatim/OpenStreetMap) -> um ponto lat/lon.
  3. Para cada setor, pegamos o CENTROIDE e o atribuímos à zona do BAIRRO
     geocodificado MAIS PRÓXIMO.
Isso é um recorte analítico APROXIMADO e documentado — as zonas são oficiais,
mas a fronteira setor-a-setor é inferida por proximidade, até existir a
geometria vetorial oficial das zonas.

Regra do projeto — NÃO INVENTAR DADO:
  • Bairro que não geocodificar é reportado e ignorado (nunca chutado).
  • Zona que ficar sem NENHUM bairro geocodificado interrompe o passo.
  • Sem internet / sem a malha do passo 1, o script explica e para — não simula.

Entradas:
  data/processed/setores_sorocaba.gpkg   (gerado pelo passo 1)
  data-pipeline/config/regions.yaml      (as 6 zonas e seus bairros)

Saídas:
  data/processed/setores_por_zona.csv    (CD_SETOR, zona, bairro_mais_proximo, dist_km)
  data/processed/geocode_bairros.json    (cache dos pontos geocodificados)
  data/processed/step02_zonas.png        (mapa de conferência, colorido por zona)

Uso:
  python data-pipeline/src/step02_zonas.py
  python data-pipeline/src/step02_zonas.py --autoteste   # testa a lógica, sem rede
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import paths  # módulo local

REGIONS_YAML = paths.REGIONS_YAML
GPKG_SETORES = paths.DATA_PROCESSED / "setores_sorocaba.gpkg"
CSV_SAIDA = paths.DATA_PROCESSED / "setores_por_zona.csv"
CACHE_GEO = paths.DATA_PROCESSED / "geocode_bairros.json"
PNG_SAIDA = paths.DATA_PROCESSED / "step02_zonas.png"

NOMINATIM = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "CityLens-Sorocaba/1.0 (projeto escolar; contato via repositório)"


# ----------------------------------------------------------------------------- #
# Saída bonitinha
def ok(msg):    print(f"  \033[32m✓\033[0m {msg}")
def aviso(msg): print(f"  \033[33m!\033[0m {msg}")
def erro_e_sair(titulo, detalhe):
    print(f"\n\033[31m✗ {titulo}\033[0m\n")
    print(detalhe + "\n")
    sys.exit(1)


# ----------------------------------------------------------------------------- #
# NÚCLEO PURO — sem geopandas, sem rede. É o que o --autoteste exercita.
def dist_km(lon1, lat1, lon2, lat2):
    """Distância aproximada (equiretangular) em km — ótima em escala de cidade."""
    R = 6371.0
    x = math.radians(lon2 - lon1) * math.cos(math.radians((lat1 + lat2) / 2))
    y = math.radians(lat2 - lat1)
    return R * math.hypot(x, y)


def atribuir_por_proximidade(setores_xy, pontos):
    """PURA. Atribui cada setor à zona do bairro mais próximo.

    setores_xy: lista de (id, lon, lat)
    pontos:     lista de (zona, bairro, lon, lat)  -- bairros geocodificados
    retorna:    lista de dicts {id, zona, bairro, dist_km}
    """
    if not pontos:
        raise ValueError("Nenhum bairro geocodificado — não há como atribuir zonas.")
    out = []
    for sid, slon, slat in setores_xy:
        melhor = None
        for zona, bairro, blon, blat in pontos:
            d = dist_km(slon, slat, blon, blat)
            if melhor is None or d < melhor[0]:
                melhor = (d, zona, bairro)
        out.append({"id": sid, "zona": melhor[1],
                    "bairro": melhor[2], "dist_km": round(melhor[0], 3)})
    return out


# ----------------------------------------------------------------------------- #
def carregar_zonas():
    try:
        import yaml
    except ImportError:
        erro_e_sair("Falta o pacote pyyaml.",
                    "Rode: pip install -r data-pipeline/requirements.txt")
    if not REGIONS_YAML.exists():
        erro_e_sair("Config das zonas não encontrada.",
                    f"Esperado em: {REGIONS_YAML}")
    d = yaml.safe_load(REGIONS_YAML.read_text(encoding="utf-8"))
    regions = d.get("regions", {})
    zonas = {}
    for key, z in regions.items():
        zonas[key] = {"nome": z.get("nome", key),
                      "bairros": list(z.get("bairros", []) or []),
                      "setores_manuais": [str(s) for s in (z.get("setores") or [])]}
    if not zonas:
        erro_e_sair("regions.yaml sem zonas.", "Verifique a seção 'regions:'.")
    return zonas


def geocodificar_bairros(zonas, municipio="Sorocaba", uf="SP"):
    """Geocodifica cada bairro via Nominatim, com cache em disco.

    Retorna (pontos, faltas):
      pontos: lista de (zona, bairro, lon, lat)
      faltas: lista de (zona, bairro) que não geocodificaram
    """
    try:
        import requests
    except ImportError:
        erro_e_sair("Falta o pacote requests.",
                    "Rode: pip install -r data-pipeline/requirements.txt")

    cache = {}
    if CACHE_GEO.exists():
        try:
            cache = json.loads(CACHE_GEO.read_text(encoding="utf-8"))
        except Exception:
            cache = {}

    pontos, faltas = [], []
    novos = 0
    sessao = requests.Session()
    sessao.headers.update({"User-Agent": USER_AGENT})

    for zona, z in zonas.items():
        for bairro in z["bairros"]:
            chave = f"{bairro}|{municipio}|{uf}"
            coord = cache.get(chave, "PENDENTE")
            if coord == "PENDENTE":
                q = f"{bairro}, {municipio}, {uf}, Brasil"
                try:
                    r = sessao.get(NOMINATIM,
                                   params={"q": q, "format": "json", "limit": 1,
                                           "countrycodes": "br"},
                                   timeout=25)
                    r.raise_for_status()
                    js = r.json()
                    coord = ([float(js[0]["lon"]), float(js[0]["lat"])] if js else None)
                except Exception as e:
                    erro_e_sair(
                        "Não consegui geocodificar (rede indisponível?).",
                        "O passo 2 precisa acessar o Nominatim (OpenStreetMap) para\n"
                        "converter os nomes dos bairros em coordenadas.\n"
                        f"Erro: {type(e).__name__}: {e}\n\n"
                        "• Rode este passo numa rede com saída para a internet.\n"
                        "• Já geocodificados ficam em cache "
                        f"({CACHE_GEO.name}) e não são refeitos.",
                    )
                cache[chave] = coord
                novos += 1
                CACHE_GEO.write_text(json.dumps(cache, ensure_ascii=False, indent=1),
                                     encoding="utf-8")
                time.sleep(1.1)  # política de uso do Nominatim: <= 1 req/s
            if coord:
                pontos.append((zona, bairro, coord[0], coord[1]))
            else:
                faltas.append((zona, bairro))

    if novos:
        ok(f"{novos} bairro(s) geocodificado(s) agora; cache em {CACHE_GEO.relative_to(paths.ROOT)}")
    else:
        ok(f"Todos os bairros vieram do cache ({CACHE_GEO.relative_to(paths.ROOT)})")

    # Nenhuma zona pode ficar sem ponto — senão setores seriam atribuídos errado.
    zonas_com_ponto = {p[0] for p in pontos}
    vazias = [z for z in zonas if z not in zonas_com_ponto]
    if vazias:
        nomes = ", ".join(zonas[z]["nome"] for z in vazias)
        erro_e_sair(
            "Zona(s) sem nenhum bairro geocodificado.",
            f"Estas zonas não têm ponto de referência: {nomes}.\n"
            "Sem isso, atribuir setores a elas seria inventar. Confira os nomes\n"
            "dos bairros em regions.yaml (ou remova a zona) e rode de novo.",
        )
    return pontos, faltas


def carregar_centroides():
    try:
        import geopandas as gpd
    except ImportError:
        erro_e_sair("Falta o geopandas.",
                    "Rode: pip install -r data-pipeline/requirements.txt")
    if not GPKG_SETORES.exists():
        erro_e_sair(
            "Malha de setores do passo 1 não encontrada.",
            f"Esperado: {GPKG_SETORES}\n"
            "Rode antes:\n"
            "    python data-pipeline/src/step01_setores_populacao.py",
        )
    gdf = gpd.read_file(GPKG_SETORES)
    if "CD_SETOR" not in gdf.columns:
        erro_e_sair("GeoPackage sem coluna CD_SETOR.",
                    "Regenere com o passo 1.")
    # WGS84 e centroide em CRS métrico (evita aviso de centroide em graus)
    gdf = gdf.to_crs(4326)
    cent = gdf.to_crs(3857).geometry.centroid.to_crs(4326)
    setores_xy = [(str(cd), pt.x, pt.y) for cd, pt in zip(gdf["CD_SETOR"], cent)]
    ok(f"{len(setores_xy)} setores carregados do passo 1")
    return gdf, setores_xy


def aplicar_override(atrib, zonas):
    """Se regions.yaml listar setores manuais, eles vencem a proximidade."""
    forcado = {}
    for zona, z in zonas.items():
        for cd in z["setores_manuais"]:
            forcado[str(cd)] = zona
    if not forcado:
        return atrib, 0
    n = 0
    for a in atrib:
        if a["id"] in forcado and a["zona"] != forcado[a["id"]]:
            a["zona"] = forcado[a["id"]]
            a["bairro"] = "(override manual)"
            n += 1
    return atrib, n


# ----------------------------------------------------------------------------- #
def autoteste():
    """Exercita o núcleo puro com uma malha SINTÉTICA (coordenadas só de teste,
    não são dados do projeto). Não usa rede nem geopandas."""
    print("\n== Autoteste do núcleo de atribuição (sem rede) ==\n")
    # 3 "bairros" de teste em 3 cantos, e 3 "setores" claramente perto de cada um.
    pontos = [
        ("zona_a", "A", 0.0, 0.0),
        ("zona_b", "B", 1.0, 0.0),
        ("zona_c", "C", 0.0, 1.0),
    ]
    setores = [
        ("s1", 0.05, 0.02),   # perto de A
        ("s2", 0.98, 0.05),   # perto de B
        ("s3", 0.03, 0.97),   # perto de C
        ("s4", 0.60, 0.10),   # mais perto de B que de A
    ]
    esperado = {"s1": "zona_a", "s2": "zona_b", "s3": "zona_c", "s4": "zona_b"}
    res = {a["id"]: a["zona"] for a in atribuir_por_proximidade(setores, pontos)}
    falhas = [k for k in esperado if res.get(k) != esperado[k]]
    # distância conhecida: ~111 km por grau de latitude no equador
    d = dist_km(0, 0, 0, 1)
    if not (110 < d < 112):
        falhas.append(f"dist_km(0,0,0,1)={d:.2f} fora do esperado (~111)")
    if falhas:
        erro_e_sair("Autoteste FALHOU.", f"Casos com problema: {falhas}")
    ok("Atribuição por proximidade: 4/4 setores na zona esperada")
    ok(f"Distância equiretangular calibrada (1° lat ≈ {d:.1f} km)")
    print("\n\033[32mAutoteste OK.\033[0m A lógica de recorte está sã.\n")


# ----------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Passo 2 — setores por zona")
    ap.add_argument("--autoteste", action="store_true",
                    help="Testa a lógica de atribuição com dados sintéticos (sem rede).")
    args = ap.parse_args()

    if args.autoteste:
        autoteste()
        return

    paths.garantir_pastas()
    print("\n== Passo 2: atribuir setores às 6 zonas (Sorocaba) ==\n")

    zonas = carregar_zonas()
    ok(f"{len(zonas)} zonas em regions.yaml: " + ", ".join(z["nome"] for z in zonas.values()))

    pontos, faltas = geocodificar_bairros(zonas)
    ok(f"{len(pontos)} bairros viraram pontos de referência")
    if faltas:
        aviso(f"{len(faltas)} bairro(s) não geocodificaram (ignorados): "
              + ", ".join(f"{b} [{zonas[z]['nome']}]" for z, b in faltas[:8])
              + (" ..." if len(faltas) > 8 else ""))

    gdf, setores_xy = carregar_centroides()
    atrib = atribuir_por_proximidade(setores_xy, pontos)
    atrib, n_over = aplicar_override(atrib, zonas)
    if n_over:
        ok(f"{n_over} setor(es) ajustado(s) por override manual do regions.yaml")

    # --- salva CSV ---
    linhas = ["CD_SETOR,zona,bairro_mais_proximo,dist_km"]
    for a in atrib:
        b = a["bairro"].replace(",", " ")
        linhas.append(f'{a["id"]},{a["zona"]},{b},{a["dist_km"]}')
    CSV_SAIDA.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    ok(f"Mapa setor→zona salvo em: {CSV_SAIDA.relative_to(paths.ROOT)}")

    # --- resumo por zona ---
    from collections import Counter
    cont = Counter(a["zona"] for a in atrib)
    print("\n  Setores por zona:")
    for z in zonas:
        print(f"    {zonas[z]['nome']:<16} {cont.get(z, 0):>5}")

    # --- mapa de conferência ---
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        zona_de = {a["id"]: a["zona"] for a in atrib}
        ordem = list(zonas.keys())
        gdf = gdf.copy()
        gdf["_zi"] = gdf["CD_SETOR"].astype(str).map(
            lambda cd: ordem.index(zona_de[cd]) if cd in zona_de else -1)
        fig, ax = plt.subplots(figsize=(9, 9))
        gdf.plot(column="_zi", categorical=True, cmap="tab10",
                 linewidth=0.12, edgecolor="white", ax=ax, legend=False)
        # legenda manual com os nomes das zonas
        import matplotlib.patches as mpatches
        cmap = plt.get_cmap("tab10")
        handles = [mpatches.Patch(color=cmap(i % 10), label=zonas[z]["nome"])
                   for i, z in enumerate(ordem)]
        ax.legend(handles=handles, loc="lower left", fontsize=8, frameon=True)
        ax.set_title("Sorocaba — setores atribuídos às 6 zonas (por proximidade)",
                     fontsize=12)
        ax.set_axis_off()
        fig.tight_layout()
        fig.savefig(PNG_SAIDA, dpi=150, bbox_inches="tight")
        ok(f"Mapa de conferência salvo em: {PNG_SAIDA.relative_to(paths.ROOT)}")
    except ImportError:
        aviso("matplotlib ausente — pulei o mapa de conferência (CSV foi gerado).")

    print("\n\033[32mPasso 2 concluído.\033[0m Confira o PNG: cada cor é uma zona.\n"
          "Se algum setor caiu na zona errada, ajuste os bairros em regions.yaml\n"
          "(ou use o override manual 'setores:') e rode de novo.\n")


if __name__ == "__main__":
    main()
