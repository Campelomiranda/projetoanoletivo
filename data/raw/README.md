# data/raw — dados brutos (não versionados)

Coloque aqui os dados baixados das fontes oficiais. O conteúdo desta pasta é
ignorado pelo git (é grande e cada pessoa baixa da fonte). **Não edite os
arquivos brutos à mão** — o pipeline lê daqui como vieram da fonte.

## Fontes confirmadas do projeto

| Dado | Fonte | Formato | Pasta esperada |
|---|---|---|---|
| Malha de setores censitários (Censo 2022) | [IBGE — Malhas de setores / divisões intramunicipais](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/26565-malhas-de-setores-censitarios-divisoes-intramunicipais.html) | Shapefile | `setores_ibge/` |
| População por setor (Censo 2022, agregados) | [IBGE — Agregados por Setores Censitários](https://biblioteca.ibge.gov.br/index.php/biblioteca-catalogo?view=detalhes&id=2102136) | CSV | `populacao_ibge/` |
| Escolas (Catálogo de Escolas / Censo Escolar) | [INEP — Dados abertos](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/inep-data/catalogo-de-escolas) | CSV | `escolas_inep/` |
| Unidades de saúde (UBS, postos, hospitais) | [CNES / DataSUS](https://cnes2.datasus.gov.br/Listar_Mantidas.asp?VCnpj=46634044000174&VEstado=35&VNome=MUNICIPIO+DE+SOROCABA) | Web/CSV | `saude_cnes/` |
| Ônibus, vias, mercados, farmácias, parques | OpenStreetMap via Overpass API | GeoJSON/API | gerado pelo `step02_*` |

> Não existe hoje portal de dados abertos geoespaciais da Prefeitura de Sorocaba
> nem GTFS público da URBES. Não inventar essas fontes.

## Dica de download (setores + população)

- **Malha:** na página do IBGE, baixe os setores de **SP** (ou do Brasil) do
  **Censo 2022**. Descompacte em `setores_ibge/` mantendo `.shp/.dbf/.shx/.prj`.
- **População:** baixe os *Agregados por Setores Censitários* e coloque o CSV em
  `populacao_ibge/`. Rode `step01` com `--coluna-pop NOME` se o nome da coluna de
  população no seu arquivo for diferente do detectado automaticamente.
