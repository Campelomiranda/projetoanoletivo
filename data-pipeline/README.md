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

## 2. Baixar os dados brutos

Coloque cada fonte em `data/raw/` (essa pasta **não** é versionada — cada pessoa
baixa das fontes oficiais). Estrutura esperada pelo passo 1:

```
data/raw/
  setores_ibge/      → shapefile da malha de SETORES CENSITÁRIOS (Censo 2022)
                       de SP/Sorocaba (.shp + .dbf + .shx + .prj juntos)
  populacao_ibge/    → CSV de população por setor (Agregados por Setor, Censo 2022)
```

Links das fontes (confirmadas no projeto) estão em
[`../data/raw/README.md`](../data/raw/README.md).

## 3. Rodar o passo 1 — conferir malha + população

```bash
python data-pipeline/src/step01_setores_populacao.py
```

O que ele faz e imprime:

- carrega o shapefile e informa quantos setores há no arquivo;
- filtra Sorocaba (código IBGE `3552205`) e informa a contagem;
- junta a população pela chave do setor e mostra quantos setores casaram;
- salva **`data/processed/setores_sorocaba.txt`** (lista de códigos, útil para
  preencher o `regions.yaml`);
- salva **`data/processed/step01_setores_sorocaba.png`** — o mapa de conferência.

Opções úteis:

```bash
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
