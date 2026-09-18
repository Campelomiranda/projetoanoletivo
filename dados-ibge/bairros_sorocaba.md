# Bairros de Sorocaba por zona (classificação aproximada)

**Fonte da lista:** Wikipédia — *Lista de bairros de Sorocaba*
(https://pt.wikipedia.org/wiki/Lista_de_bairros_de_Sorocaba). Sorocaba tem
~250 nomes na lista (muitos são loteamentos/condomínios e variações do mesmo
bairro).

⚠️ **Aviso:** a Wikipédia lista os bairros mas **não** os agrupa por zona. O
IBGE **não** tem divisão de bairros para Sorocaba (só 58 municípios de SP
têm). A divisão por zona abaixo é **aproximada e não oficial**, feita a partir
de guias locais + geografia, só para o protótipo. A divisão oficial da
Prefeitura pode diferir — quando houver, é só substituir esta lista.

## Zonas usadas no CityLens (5)

- **Centro** — Centro, Vila Hortência, Vila Assis, Vila Leão, Vila Trujillo,
  Vila Gabriel, Vila Santana, Jardim Vergueiro, Vila Augusta, Vila
  Independência, Vila Amélia
- **Zona Sul** — Campolim, Parque Campolim, Jardim Europa, Jardim Simus,
  Cajuru do Sul, Jardim Saira, Jardim Portal da Colina, Central Parque
  Sorocaba, Jardim dos Estados, Jardim Novo Mundo, Jardim Ibiti do Paço
- **Zona Norte** — Éden, Aparecidinha, Brigadeiro Tobias, Jardim Abaeté,
  Jardim São Guilherme, Vila Angélica, Habiteto, Inhayba, Caputera, Itavuvu,
  Parque Manchester
- **Zona Leste** — Além Ponte, Jardim Santa Rosália, Vila Sabiá, Morros, Vila
  João Romão, Parada do Alto, Vila Colorau, Vila Zacarias, Ipiranga, Vila
  Haro, Jardim Zulmira
- **Zona Oeste** — Wanel Ville, Wanel Ville IV, Cerrado, Júlio de Mesquita
  Filho, Vila Helena, Parque São Bento, Jardim Bandeirantes, Jardim Ipanema,
  Jardim Nova Ipanema, Jardim Maria do Carmo, Jardim Guadalajara

## Como corrigir/completar

Para usar a divisão oficial: pegue o mapa/lei de bairros da Prefeitura de
Sorocaba, ajuste as listas acima (e as arrays `bairros:[...]` de cada zona em
`mockups/radiografia-sorocaba.html`). No pipeline final, o ideal é mapear cada
**setor censitário** do IBGE para uma zona e derivar tudo dos dados.
