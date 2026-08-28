# Radiografia Urbana de Sorocaba

Plataforma web que mostra a infraestrutura urbana ao redor de diferentes
regiões de **Sorocaba (SP)** através de um **Índice de Infraestrutura Urbana
(0–100)** por região, visualizado num mapa.

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

- [x] **Esquema visual interativo** das 4 telas (`mockups/`).
- [x] **Estrutura do repositório + ambiente do pipeline** (`data-pipeline/`).
- [x] **Config das regiões** (`data-pipeline/config/regions.yaml`).
- [ ] **Passo 1 do pipeline** — carregar malha de setores (IBGE) + população e
      plotar um mapa de conferência (`src/step01_setores_populacao.py`).
- [ ] Passo 2 — extração de POIs via Overpass (OpenStreetMap).
- [ ] Cálculo do índice e geração do GeoJSON do site.
- [ ] App React + Leaflet.

## Por onde começar

Veja **[`data-pipeline/README.md`](data-pipeline/README.md)** para montar o
ambiente Python, baixar os dados e rodar o primeiro passo.
