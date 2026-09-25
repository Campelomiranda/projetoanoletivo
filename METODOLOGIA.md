# Metodologia — CityLens · Radiografia Urbana de Sorocaba

Como cada nota do CityLens é calculada, com quais fontes e quais limites.
Princípio inegociável: **não inventar dado**. Todo número tem fonte pública,
fórmula e data; o que não dá para medir fica marcado como *indisponível*.

> Situação atual dos dados: **set/2026**. Saúde vem do **CNES** (abr/2026) e
> escolas do **INEP** (2025); ônibus, comércio e praças vêm do OpenStreetMap.

## 1. Unidade de análise

- A menor unidade é o **setor censitário do IBGE** (Censo 2022) — há ~1.150 em
  Sorocaba. Os setores são desenhados pelo IBGE para ter **população parecida**
  entre si, então tratá-los como iguais equivale, na prática, a uma média
  **por morador**.
- Cada setor é atribuído a uma das **6 zonas oficiais** de Sorocaba (Centro,
  Norte, Oeste, Sul, Leste, Industrial), definidas pelo mapa de zoneamento da
  **Prefeitura/Urbes**. A atribuição setor→zona é feita por **proximidade ao
  bairro** (método `nearest_bairro`): o setor recebe a zona do bairro
  geocodificado mais próximo do seu centro. É um recorte **aproximado e
  documentado** (ver *Limitações*).

## 2. Fontes de dados

| O quê | Fonte | Como é obtido |
|---|---|---|
| Malha de setores censitários | **IBGE** — Censo 2022 | pacote `geobr` |
| Estabelecimentos de saúde | **CNES** (abr/2026) | `geobr.read_health_facilities` |
| Escolas | **INEP** — Censo Escolar 2025 | `geobr.read_schools` |
| Ônibus, comércio, praças/parques, ruas | **OpenStreetMap** | `osmnx` / Overpass |
| Divisão em 6 zonas | **Prefeitura de Sorocaba / Urbes** | transcrição do mapa oficial de zoneamento |

**Recorte da saúde (CNES):** dos 2.073 estabelecimentos, 1.408 são consultórios
particulares isolados; ficam de fora. Usamos os tipos de unidade (`tp_unidade`)
{1, 2, 4, 5, 7, 15, 20, 21, 36, 62, 70, 71, 73} — postos, UBS, policlínicas,
hospitais, pronto-socorros, UPAs, CAPS e clínicas de especialidade (411 em
Sorocaba). **Escolas (INEP):** só as em atividade, sem as localizadas apenas por
cidade/bairro (451 escolas). Essa escolha de tipos muda bastante a nota de saúde.

## 3. Como cada eixo é medido

A ideia central: para cada setor, medimos a **distância a pé pela rua** (não em
linha reta) do centro do setor até o equipamento mais próximo de cada tipo. A
distância a pé usa a **malha de ruas e caminhos de pedestre** do OpenStreetMap
(grafo `walk`), calculada com caminho mínimo (Dijkstra multi-origem).

Cada distância vira uma **nota de 0 a 100** por faixas fixas: até `D0` metros a
nota é **100** (bem perto); a partir de `D1` metros a nota é **0** (longe
demais); entre os dois, cai em linha reta. É uma **escala absoluta** — não
depende de comparar as zonas entre si.

| Item | D0 (nota 100) | D1 (nota 0) |
|---|---|---|
| Ponto de ônibus | 200 m | 800 m |
| Mercado / farmácia / padaria | 250 m | 1000 m |
| Saúde (posto/clínica/hospital) | 500 m | 2000 m |
| Escola | 500 m | 1500 m |
| Praça / parque | 250 m | 1000 m |

Os quatro eixos do índice:

- **Serviços essenciais** = média das notas de **saúde**, **escolas** e
  **comércio** (mercado/farmácia/padaria).
- **Mobilidade** = nota de **ponto de ônibus**.
- **Meio ambiente** = nota de **praça/parque** (a distância é medida até a borda
  do parque; reservas naturais e "jardins" privados do OSM não contam).
- **Acesso urbano / caminhabilidade** = média de dois componentes:
  - **conectividade**: cruzamentos de rua (3+ vias) por km² num raio de 500 m do
    setor — quarteirões curtos = mais fácil andar (20 cruz./km² = 0 · 120 = 100);
  - **cidade de 10 minutos**: quantos dos 5 itens acima estão a **≤ 800 m a pé**
    (≈ 10 minutos) do setor.

## 4. Da nota do setor à nota da zona

- A nota de cada eixo na **zona** é a **média dos seus setores**. Como os setores
  têm população parecida, é quase uma **média por morador**, e **não depende do
  tamanho** da zona (uma zona grande com muito vazio não é penalizada).
- O **Índice de Infraestrutura Urbana (0–100)** da zona é a **média dos 4 eixos**.
- O **selo de confiabilidade** mostra quantos eixos foram efetivamente calculados
  (dos 4 esperados). Eixo sem fonte carregada aparece como *indisponível* — nunca
  preenchido com chute.

## 5. Limitações (o que a nota NÃO diz)

- **A pé, mas sem calçada, iluminação ou declive**: a distância segue o traçado
  das ruas, mas o OpenStreetMap não diz se a calçada existe/é boa, se há
  iluminação, nem quanto a rua sobe.
- **Setores sem caminho a pé** até um serviço (50 dos 1.148, a maioria na Zona
  Industrial; 38 no caso da saúde) ficam com **nota 0** naquele eixo — o serviço
  existe, mas não há rota de pedestre até ele na malha do OSM.
- **A escolha dos tipos de saúde (CNES) afeta a nota**: incluir/excluir tipos de
  unidade muda bastante o resultado das zonas afastadas. O recorte usado está na
  seção 2 e pode ser revisto.
- **Recorte setor→zona é aproximado** (proximidade ao bairro), até existir a
  geometria vetorial oficial das zonas.
- É uma **radiografia de acesso**, não um ranking de "bairro bom ou ruim": mede
  distância a serviços, não qualidade deles, segurança ou preço.

## 6. Reprodutibilidade

Tudo é gerado pelo notebook **`CityLens_rodar_no_colab.ipynb`** (na raiz),
rodável no Google Colab sem instalar nada. Ele baixa as fontes, calcula as notas
por setor e por zona, e exporta os arquivos de resultado
(`indice_final_4eixos.csv`, `caminhabilidade_por_setor.csv`,
`setores_sorocaba.geojson`). Qualquer pessoa pode rodar e conferir os números.

## 7. Próximos passos de dados

- [x] **Saúde** a partir do **CNES** e **escolas** a partir do **INEP**.
- [x] **Mapa por setor** no site (choropleth a partir do `setores_sorocaba.geojson`).
- [ ] **População por setor** (Agregados do Censo 2022) para ponderar as médias
  por habitante de forma exata (hoje: setor ≈ mesma população).
- [ ] Revisar a lista de **tipos de unidade do CNES** que contam como acesso.
