# web — aplicação (a construir)

App **React + Leaflet** que consome os arquivos estáticos (`GeoJSON`/`JSON`)
gerados pelo pipeline. Sem backend dinâmico no MVP.

Ainda não iniciado. Enquanto isso, o **protótipo visual navegável** das 4 telas
está em [`../mockups/radiografia-sorocaba.html`](../mockups/radiografia-sorocaba.html)
— é a referência de interface (Mapa, Região, Comparação, Metodologia).

## Sobre o mapa "vivo" (imagens reais)

No app React, o mapa usará **tiles reais do OpenStreetMap** via Leaflet (ruas,
áreas verdes, satélite se quisermos) — algo que roda direto no navegador, sem
chave de API. O protótipo em `mockups/` não carrega tiles ao vivo (é um HTML
isolado), por isso usa uma base cartográfica real embutida (contorno do IBGE +
municípios vizinhos). No produto final, o basemap é o mapa de verdade.
