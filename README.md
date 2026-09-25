# CityLens — Sorocaba

**CityLens** é uma plataforma web que faz a radiografia urbana de **Sorocaba (SP)**:
mostra a infraestrutura ao redor de diferentes regiões através de um **Índice de
Infraestrutura Urbana (0–100)** por região, visualizado num mapa.

> **Não é um ranking de "bairro bom ou ruim".** É uma radiografia transparente
> de acesso a serviços, mobilidade, meio ambiente etc. — cada nota é rastreável
> até um dado público real, uma fórmula e uma data.

## Princípio inegociável do projeto

**Não inventar dado.** Se uma fonte não existe ou ainda não foi baixada, o
indicador é marcado como *indisponível* — nunca preenchido com valor fictício
ou zero. Todo número exibido precisa ter fonte + fórmula + data.

## Estrutura do repositório

```
mockups/        Protótipo visual navegável das 4 telas (HTML único, sem build).
                → Alinhamento de interface antes de codar o app de verdade.

data-pipeline/  Pipeline de dados em Python (GeoPandas). Baixa/carrega as fontes,
                calcula os indicadores e gera os arquivos estáticos do site.
  config/       Configuração legível: composição das regiões, fontes, colunas.
  src/          Scripts do pipeline, numerados na ordem de execução.

data/
  raw/          Dados brutos baixados das fontes (NÃO versionado — cada um baixa).
  processed/    Saídas geradas (imagens de conferência, GeoJSON do site).

web/            App React + Leaflet (a construir), consome os arquivos estáticos.
```

## Estado atual

- [x] **Esquema visual interativo** com busca por bairro e as **6 zonas
      oficiais** de Sorocaba (`mockups/`).
- [x] **Estrutura do repositório + ambiente do pipeline** (`data-pipeline/`).
- [x] **Config das 6 zonas** (`data-pipeline/config/regions.yaml`).
- [x] **Passo 1 do pipeline — script pronto** (rodar localmente): carrega a
      malha de setores (IBGE) + população e plota um mapa de conferência
      (`src/step01_setores_populacao.py`).
- [x] **Passo 2 do pipeline — script pronto** (rodar localmente): atribui cada
      setor a uma das 6 zonas por proximidade ao bairro (`src/step02_zonas.py`);
      lógica coberta por `--autoteste`.
- [x] **Passo 3 + 4 rodados no Colab**: POIs do OpenStreetMap + malha de ruas,
      medindo a **distância a pé** de cada setor até saúde, escolas, comércio,
      ônibus e praças — nota real nos **4 eixos** por zona (incl. caminhabilidade).
- [x] **Dados reais no site** (`mockups/`): as notas das 6 zonas vêm do pipeline
      (OSM + IBGE), não mais de valores ilustrativos.
- [x] **Metodologia documentada** — ver [`METODOLOGIA.md`](METODOLOGIA.md).
- [ ] **Mapa por setor no site** (choropleth a partir do `setores_sorocaba.geojson`),
      no lugar dos pinos por zona. *(motor do mapa já validado)*
- [ ] Saúde via **CNES** e escolas via **INEP** (hoje ainda do OSM).
- [ ] População real por setor (Agregados do Censo 2022) para média por habitante.

## Por onde começar

Veja **[`data-pipeline/README.md`](data-pipeline/README.md)** para montar o
ambiente Python, baixar os dados e rodar o primeiro passo.
