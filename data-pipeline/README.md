# Pipeline de dados — Radiografia Urbana de Sorocaba

Este pipeline **carrega** as fontes públicas, calcula os indicadores e gera os
arquivos estáticos do site. Regra de ouro: **não inventar dado**. Fonte ausente
ou com formato inesperado → o indicador fica *indisponível* e o script avisa;
nunca simula valor.

## 1. Montar o ambiente Python

Requer Python 3.10+.

```bash
# a partir da raiz do repositório
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r data-pipeline/requirements.txt
```

> `geopandas` traz dependências geoespaciais (GDAL/GEOS via wheels). Se o
> `pip install` falhar no seu sistema, instale antes com conda/mamba:
> `conda install -c conda-forge geopandas osmnx`.

## 2. Dados brutos

A **geometria** (malha de setores) é baixada automaticamente pelo `geobr` — você
**não precisa** baixar shapefile à mão. A **população** ainda é um CSV do IBGE
(o geobr não fornece população), colocado em `data/raw/`:

```
data/raw/
  populacao_ibge/    → CSV de população por setor (Agregados por Setor, Censo 2022)
  setores_ibge/      → (opcional) shapefile, só se você usar --shapefile
```

Essa pasta **não** é versionada — cada pessoa baixa das fontes. Links e passo a
passo: [`GUIA_DOWNLOAD_IBGE.md`](GUIA_DOWNLOAD_IBGE.md) e
[`../data/raw/README.md`](../data/raw/README.md).

## 3. Rodar o passo 1 — conferir malha + população

```bash
python data-pipeline/src/step01_setores_populacao.py
```

O que ele faz e imprime:

- baixa a malha de setores de Sorocaba via **geobr** (fonte: IBGE) e informa a
  contagem — já filtrada pelo código `3552205`;
- salva a geometria em **`data/processed/setores_sorocaba.gpkg`** (para os
  próximos passos reutilizarem);
- junta a população pela chave do setor e mostra quantos setores casaram;
- salva **`data/processed/setores_sorocaba.txt`** (lista de códigos, útil para
  preencher o `regions.yaml`);
- salva **`data/processed/step01_setores_sorocaba.png`** — o mapa de conferência.

Opções úteis:

```bash
# escolher o ano da malha (padrão 2022)
python data-pipeline/src/step01_setores_populacao.py --ano 2010

# usar um shapefile local em vez do geobr (data/raw/setores_ibge/)
python data-pipeline/src/step01_setores_populacao.py --shapefile

# se o nome da coluna de população for diferente do detectado automaticamente
python data-pipeline/src/step01_setores_populacao.py --coluna-pop V0001

# só a malha, sem juntar população
python data-pipeline/src/step01_setores_populacao.py --sem-populacao
```

Se algo estiver faltando ou com formato diferente, o script **para com uma
mensagem explicando o que fazer** (e lista as colunas disponíveis) — em vez de
adivinhar.

## 4. Preencher as regiões-piloto

Com a lista de setores em mãos (`data/processed/setores_sorocaba.txt`), edite
[`config/regions.yaml`](config/regions.yaml) e informe quais setores compõem
cada região. Já há **uma região de exemplo preenchida** para você ver o formato.

## Próximos passos (ainda não implementados)

- `step02_*` — extração de POIs via Overpass/OpenStreetMap (ônibus, escolas,
  saúde, mercados, farmácias, parques, vias) para o polígono de Sorocaba.
- cálculo do índice (normalização min-max, pesos com redistribuição, selo).
- geração do GeoJSON consumido pelo app web.
