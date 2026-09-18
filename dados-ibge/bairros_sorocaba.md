# Bairros de Sorocaba por zona (classificação aproximada)

**Fontes usadas:**
- Wikipédia — *Lista de bairros de Sorocaba* (lista dos nomes).
- Guias locais que agrupam por zona (Sorocaba Comércio / AE Patrimônio) — para
  decidir a zona de cada bairro.
- Mapas oficiais do Plano Diretor 2025 no repositório (`mapa-01-macrozoneamento.pdf`,
  `mapa-02-zoneamento.pdf`, `mapa-03-sistema-viario.pdf`, `mapa_zoneamento.pdf`).

⚠️ **Aviso:** o IBGE **não** tem bairros para Sorocaba, e a Prefeitura divide a
cidade por **zonas de uso do solo** (os PDFs acima), não em Norte/Sul/Leste/Oeste.
A divisão Norte/Sul/Leste/Oeste/Centro é **informal** — os próprios guias locais
se contradizem em alguns bairros. A classificação abaixo é a **melhor
aproximação** para o protótipo e pode ser corrigida.

## Fronteiras (segundo os guias locais)
- **Centro** — entre Além Linha (N), Campolim-Vergueiro (S), Além Ponte (L), Cerrado (O).
- **Zona Sul** — eixo Campolim–Vergueiro (mais estruturada/valorizada).
- **Zona Norte** — a mais populosa; corredores Av. Itavuvu e Av. Ipanema; aeroporto.
- **Zona Leste** — Além Ponte, Zoológico, Uniso, Av. São Paulo; faz divisa com Brigadeiro Tobias.
- **Zona Oeste** — Wanel Ville (5 subdivisões) e Cerrado.

## Zonas usadas no CityLens (5)

> Síntese a partir dos guias locais que o grupo consolidou. Quando um bairro
> aparecia em mais de uma zona (ex.: Parque Campolim e Jardim Simus surgiram em
> Sul e Oeste; Jardim Santa Rosália em Leste e Sul), ficou na zona citada com
> mais força pela última consolidação. Continua sendo **aproximação, não oficial**.

- **Centro** — Centro, Além Linha, Vila Leão, Vila Trujillo, Vila Gabriel, Vila Augusta, Vila Independência, Vila Jardini, Vila Boa Vista, Vila Santa Rita
- **Zona Sul** — Campolim, Parque Campolim, Jardim Vergueiro, Jardim Santa Rosália, Vila Assis, Jardim Simus, Jardim Europa, Jardim Saira, Jardim Portal da Colina, Central Parque Sorocaba
- **Zona Norte** — Éden, Aparecidinha, Brigadeiro Tobias, Parque São Bento, Habiteto, Vila Helena, Jardim Abaeté, Jardim São Guilherme, Vila Progresso, Vila Santana, Vila Hortência, Vila Fiori, Vila Angélica, Itavuvu
- **Zona Leste** — Além Ponte, Jardim Faculdade, Jardim Santa Cecília, Vila Haro, Vila Sabiá, Morros, Vila João Romão, Parada do Alto, Vila Zacarias, Ipiranga, Jardim Zulmira
- **Zona Oeste** — Wanel Ville (I, II, IV), Cerrado, Júlio de Mesquita Filho, Jardim Bandeirantes, Jardim Emília, Jardim Ipanema, Jardim Nova Ipanema, Jardim Maria do Carmo

Para trocar pela divisão oficial: ajuste as arrays `bairros:[...]` de cada zona
em `mockups/radiografia-sorocaba.html`. No pipeline final, o ideal é mapear cada
setor censitário do IBGE para uma zona e derivar tudo dos dados.
