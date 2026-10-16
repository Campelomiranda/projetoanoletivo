# Pesquisa de campo CityLens — versão rápida (~2 min)

São **8 perguntas** de percepção/autodeclarado, pensadas para serem curtas e
ainda assim **separar bem as regiões**. É percepção, não medição oficial.

## Jeito mais fácil (celular): montar no Google Forms na mão
Abra forms.google.com → formulário em branco → digite as 8 perguntas abaixo.

1. **Qual a sua ZONA em Sorocaba?** — *Lista suspensa · obrigatória*
   Centro · Zona Norte · Zona Oeste · Zona Sul · Zona Leste · Zona Industrial · Não sei / outra
2. **Bairro (opcional)** — *Resposta curta*
3. **Tempo a pé até o ponto de ônibus mais próximo** — *Múltipla escolha · obrigatória*
   Menos de 5 min · 5 a 10 min · 10 a 20 min · Mais de 20 min · Não dá a pé · Não sei
4. **Tempo a pé até a UBS / posto de saúde** — *Múltipla escolha · obrigatória* (mesmas opções da 3)
5. **As esquinas têm rampas de acessibilidade?** — *Múltipla · obrigatória*
   Sim, na maioria · Em algumas · Quase nenhuma · Não sei
6. **Na sua região, como é o acesso a:** — *Grade de múltipla escolha*
   Linhas: Saúde · Escolas · Ônibus · Comércio · Praças/áreas verdes · Segurança
   Colunas: Muito ruim · Ruim · Regular · Bom · Muito bom
7. **O que MAIS falta? (até 2)** — *Caixas de seleção*
   Saúde · Escolas · Transporte/ônibus · Comércio · Praças · Calçadas/acessibilidade · Iluminação · Segurança
8. **Deficiência/mobilidade reduzida em casa?** — *Múltipla*
   Sim · Não · Prefiro não dizer

## Jeito automático (computador): o script
`criar_forms.gs` cria tudo sozinho: script.google.com → Novo projeto → cola → Executar.

## Para separar bem as regiões
- Zona obrigatória + tempo a pé em faixas são o que mais diferencia Centro x periferia.
- **Meta: ~10 respostas por zona** (mínimo ~60 no total). Sem equilíbrio por zona,
  a comparação fica enviesada.

## Depois de coletar
Baixe a planilha em CSV e me mande — eu agrego por zona (faixas de tempo → nota
0–100, médias por zona + nº de respostas) e integro na aba *Pesquisa*, sem inventar
dado e sem afirmar diferença onde o nº de respostas não permitir.
