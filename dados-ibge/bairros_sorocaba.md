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
- **Centro** — Centro, Vila Hortência, Vila Assis, Vila Leão, Vila Trujillo, Vila Gabriel, Vila Augusta, Vila Independência, Vila Jardini, Vila Fiori
- **Zona Sul** — Campolim, Parque Campolim, Jardim Vergueiro, Jardim Europa, Jardim Simus, Cajuru do Sul, Jardim Saira, Jardim Portal da Colina, Central Parque Sorocaba, Jardim dos Estados, Jardim Ibiti do Paço
- **Zona Norte** — Éden, Aparecidinha, Brigadeiro Tobias, Parque São Bento, Habiteto, Vila Helena, Jardim Abaeté, Jardim São Guilherme, Jardim Nova Esperança, Jardim São Conrado, Vila Santana, Jardim Maria Eugênia, Nova Sorocaba, Itavuvu
- **Zona Leste** — Além Ponte, Jardim Santa Rosália, Vila Sabiá, Morros, Vila João Romão, Parada do Alto, Vila Colorau, Vila Zacarias, Ipiranga, Vila Haro, Jardim Zulmira
- **Zona Oeste** — Wanel Ville (I, II, IV), Cerrado, Júlio de Mesquita Filho, Jardim Bandeirantes, Jardim Ipanema, Jardim Nova Ipanema, Jardim Maria do Carmo, Jardim Guadalajara

Para trocar pela divisão oficial: ajuste as arrays `bairros:[...]` de cada zona
em `mockups/radiografia-sorocaba.html`. No pipeline final, o ideal é mapear cada
setor censitário do IBGE para uma zona e derivar tudo dos dados.
