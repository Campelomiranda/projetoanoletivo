# Pesquisa de campo CityLens — Google Forms

Objetivo: coletar **dados mais reais** (percepção + distâncias autodeclaradas) por
**região**, para a aba *Pesquisa* do site e para fortalecer o eixo de
**acessibilidade (PCD)**, que hoje não tem dado objetivo.

> Regra do projeto: é **percepção/autodeclarado**, não medição oficial. Os
> resultados complementam os dados de distância a pé — não os substituem.

## Como criar o formulário (automático, ~2 min)
1. Abra <https://script.google.com> → **Novo projeto**.
2. Cole o conteúdo de [`criar_forms.gs`](criar_forms.gs).
3. Clique em **Executar** (▶) na função `criarFormularioCityLens`. Autorize na 1ª vez.
4. No log aparecem 3 links: **responder**, **editar** e a **planilha de respostas**.

Prefere montar na mão? As perguntas estão todas no `.gs` — é só recriar no
forms.google.com.

## Por que este formulário separa melhor as regiões
A pesquisa anterior (57 respostas) usava quase só "bom/ruim", que varia pouco
entre zonas. Aqui a diferença vem de:
- **Zona obrigatória** (lista) + bairro → dá para agrupar e comparar por zona.
- **Tempo a pé em faixas** (ônibus, saúde, escola, comércio, praça) → varia muito
  mais entre Centro e periferia do que uma nota genérica.
- **Perguntas objetivas de acessibilidade** (rampas, piso tátil, sinal sonoro) →
  discriminam regiões e cobrem o tema que falta no site.
- **Escala Likert 1–5 igual para todos os eixos** → comparação justa entre zonas.

## Meta de coleta (o que mais importa)
- **Pelo menos ~10 respostas por zona** (6 zonas → mínimo ~60; ideal 100+).
  Sem equilíbrio por zona, a comparação fica enviesada para a zona mais respondida.
- Divulgue por zona (grupos de bairro, escolas, comércios locais de cada região).
- Anote quantas respostas vieram de cada zona antes de concluir qualquer diferença.

## Como transformar em dados do site (depois de coletar)
1. Baixe a planilha de respostas em **CSV** (Arquivo → Fazer download → .csv).
2. No Colab (notebook do projeto), agregue por zona:
   - converta as faixas de tempo em pontos (ex.: <5 min = 100 … +20 min = 0);
   - calcule **médias/medianas por zona** e a **cobertura** (nº de respostas/zona);
   - exporte os números por zona para a aba *Pesquisa*.
3. Me mande o CSV ou os números agregados que eu integro no site, deixando
   explícito que é percepção e mostrando **quantas respostas** sustentam cada zona.

## Honestidade (não inventar dado)
- Se uma zona tiver poucas respostas, **mostre isso** e não a classifique.
- Acessibilidade PCD segue como **percepção** — não vira medição de rampas.
- Diferença entre zonas só é afirmada quando o nº de respostas por zona permitir.
