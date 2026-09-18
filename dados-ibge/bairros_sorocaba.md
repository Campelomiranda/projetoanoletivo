# Bairros de Sorocaba por zona (mapa oficial de zoneamento)

**Fonte principal (nova):** mapa **oficial de zoneamento da Prefeitura de
Sorocaba / Urbes** — o desenho que a própria cidade usa para dividir o
território em zonas. Os bairros abaixo foram **transcritos região por região**
a partir do PDF (zoom alto), expandindo as abreviações do mapa (`Jd.` = Jardim,
`Pq.` = Parque, `V.` = Vila).

⚠️ **Ressalva honesta:** o mapa é um recorte de desenho técnico (CAD) com
centenas de rótulos minúsculos. A maioria foi lida com certeza, mas alguns
ficaram pequenos demais mesmo com zoom máximo — então esta lista cobre a
**grande maioria** dos rótulos, mas **não necessariamente 100%**. Ainda assim é
**muito mais confiável** que as listas anteriores (Wikipédia / sites de
imobiliária), porque vem direto da fonte oficial de zoneamento.

Isto **substitui** a divisão informal Norte/Sul/Leste/Oeste que usávamos antes
(baseada em guias locais que se contradiziam). Agora são as **6 zonas oficiais**
que a Sorocaba usa administrativamente.

## 6 zonas oficiais usadas no CityLens

- **Centro** — Centro (bairro único da zona). *Referências no mapa:* Catedral,
  Mercado Municipal, Museu Ferroviário, Rodoviária, Estação Ferroviária, PUC,
  FADI, UNISO.
- **Zona Norte** — Jardim Botucatu, Jardim Maria Eugênia, Parque Laranjeiras,
  Jardim Guaíba, Jardim São Guilherme, Jardim Santa Marina, Parque São Bento,
  Jardim Novo Horizonte, Jardim Maria Antônia Prado, Jardim Guadalupe, Vila Nova
  Sorocaba, Vila Angélica, Jardim Húngaros, Jardim Brasilândia, Vila Fiori,
  Jardim Maria do Carmo, Vila Gabriel, Vila Progresso, Vila Porto, Vila Rica,
  Parque Vitória Régia, Retiro São João, Jardim Iguatemi, Jardim Morumbi, Jardim
  Leocádia, Vila Cardoso, Vila Barão, Vila Nova Esperança, Jardim Zulmira, Jardim
  Simus, Jardim Vera Cruz, Santa Terezinha, Vila Trujillo, Vila Carvalho, Vila
  Santana, Jardim Santa Rosália. *Referências:* Fazenda Ipanema, Aeroporto.
- **Zona Oeste** — Jardim Santa Bárbara, Júlio de Mesquita Filho, Jardim Wanel
  Ville, Parque Esmeralda, Jardim Ouro Fino, Parque Ouro Fino, Parque Manchester,
  Central Parque, Largo do Divino, Jardim São Paulo. *Referências:* região do
  Cerqueira, Aeroclube de Itupararanga (margens da represa).
- **Zona Sul** — Vila Jardini, Jardim Magnólia, Jardim Paulistano, Jardim Europa,
  Jardim dos Estados, Jardim América, Jardim Portal da Colina, Jardim Emília,
  Jardim Sandra, Parque da Biquinha, Vila Assis, Parque Água Vermelha, Jardim
  Guadalajara, Jardim São Carlos, Parque Campolim. *Referências:* região do Mangal.
- **Zona Leste** — Jardim Gonçalves, Jardim Sol, Jardim Bandeirantes, Jardim
  Piratininga, Jardim Granja, Vila Haro, Parque Três Meninos, Vila Hortência,
  Jardim Gutierres, Jardim Prestes de Barros, Vila Colorau, Vila Barcelona,
  Jardim Parada do Alto. *Referências:* Zoológico Municipal, Senac.
- **Zona Industrial** — Aparecidinha, Brigadeiro Tobias, Alto da Boa Vista,
  Parque Chico Mendes. *Referências (prédios públicos concentrados):* Paço
  Municipal (Prefeitura), Câmara Municipal, Fórum Cível e Criminal, Fórum do
  Trabalho, Tribunal de Contas, Teatro Municipal, Biblioteca Municipal, Receita
  Federal, UNIP, SEST SENAT.

## Mapas oficiais no repositório

- `mapa-01-macrozoneamento.pdf`, `mapa-02-zoneamento.pdf`,
  `mapa-03-sistema-viario.pdf`, `mapa_zoneamento.pdf` — Plano Diretor / zoneamento
  da Prefeitura, de onde os bairros foram transcritos.

## Como ajustar

Para corrigir/completar um bairro, edite as arrays `bairros:[...]` (e, se for um
ponto de referência, `refs:[...]`) de cada zona em
`mockups/radiografia-sorocaba.html`. No pipeline final, o ideal é mapear cada
setor censitário do IBGE para uma dessas 6 zonas e derivar os indicadores dos
dados — em vez de digitar bairro a bairro.
