# Pipeline de dados — Radiografia Urbana de Sorocaba

Este pipeline **carrega** as fontes públicas, calcula os indicadores e gera os
arquivos estáticos do site. Regra de ouro: **não inventar dado**. Fonte ausente
ou com formato inesperado → o indicador fica *indisponível* e o script avisa;
nunca simula valor.

## Caminho FÁCIL — rodar no navegador (Google Colab), sem instalar nada

Não quer instalar Python nem lidar com o `geopandas` no Windows? Use o notebook
pronto **[`notebooks/CityLens_rodar_no_colab.ipynb`](notebooks/CityLens_rodar_no_colab.ipynb)**:

1. Abra <https://colab.research.google.com> → aba **Upload** → escolha esse
   arquivo `.ipynb` (baixe-o do GitHub primeiro, botão **Download raw file**).
2. No Colab: menu **Ambiente de execução → Executar tudo**.
3. Em ~2–4 min ele baixa a malha do IBGE sozinho, localiza os bairros pelo
   OpenStreetMap e mostra o **mapa das 6 zonas** + a contagem de setores por zona.

É autossuficiente (não precisa clonar o repositório nem baixar dados à mão) e
segue a mesma regra de **não inventar dado**. As seções abaixo são o caminho
"raiz", para rodar na sua própria máquina.

## 1. Montar o ambiente Python (caminho local)

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

## 4. Rodar o passo 2 — atribuir cada setor a uma das 6 zonas

A unidade de análise do CityLens são as **6 zonas oficiais** de Sorocaba
(Centro, Norte, Oeste, Sul, Leste, Industrial). O passo 2 decide **a que zona
cada setor pertence**, sem você digitar setor a setor:

```bash
python data-pipeline/src/step02_zonas.py
```

Como ele decide (método **`nearest_bairro`**):

1. lê os bairros de cada zona em [`config/regions.yaml`](config/regions.yaml)
   (transcritos do mapa oficial de zoneamento da Prefeitura/Urbes);
2. geocodifica cada bairro pelo **Nominatim/OpenStreetMap** (com cache em
   `data/processed/geocode_bairros.json`, respeitando ≤ 1 requisição/segundo);
3. atribui cada setor à zona do **bairro geocodificado mais próximo** do seu
   centroide.

Saídas:

- `data/processed/setores_por_zona.csv` — `CD_SETOR, zona, bairro_mais_proximo, dist_km`;
- `data/processed/step02_zonas.png` — mapa de conferência, uma cor por zona.

Regra **não inventar dado**: bairro que não geocodificar é avisado e ignorado;
zona que ficar **sem nenhum** bairro geocodificado **interrompe** o passo. Sem
internet, o script explica e para — não simula.

> Testar a lógica sem internet:
> `python data-pipeline/src/step02_zonas.py --autoteste`
> (roda o núcleo de atribuição com dados sintéticos e confere o resultado).

É um recorte **aproximado e documentado**: as zonas são oficiais, mas a fronteira
setor-a-setor é inferida por proximidade. Se um setor cair na zona errada,
ajuste os bairros em `regions.yaml` (ou use o campo opcional `setores:` como
override manual) e rode de novo. Nada aqui altera as fronteiras oficiais — é só
o recorte analítico do protótipo.

## Próximos passos (ainda não implementados)

- `step03_*` — extração de POIs via Overpass/OpenStreetMap (ônibus, escolas,
  saúde, mercados, farmácias, parques, vias) para o polígono de Sorocaba.
- cálculo do índice por zona (normalização min-max, pesos com redistribuição,
  selo de confiabilidade).
- geração do GeoJSON consumido pelo app web (mesma divisão do `regions.yaml`).
