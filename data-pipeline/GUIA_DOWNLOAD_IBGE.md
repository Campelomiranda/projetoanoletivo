# Guia de download — dados do IBGE (Censo 2022)

Passo a passo para baixar as **duas** fontes do IBGE que o passo 1 do pipeline
usa: a **malha de setores censitários** (geometria) e a **população por setor**.

> O IBGE às vezes reorganiza as pastas de download. Se um link mudar, use a busca
> do próprio site pelo nome em **negrito** e confira pela descrição do arquivo.
> Na dúvida, baixe e rode o `step01` — ele lista as colunas e avisa o que falta,
> em vez de inventar dado.

---

## Parte A — Malha de setores censitários (geometria)

**O que é:** o desenho (shapefile) de cada setor censitário. É a base para
recortar as regiões-piloto.

### Caminho pelo site

1. Abra a página das malhas:
   <https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/26565-malhas-de-setores-censitarios-divisoes-intramunicipais.html>
2. Procure a seção de **Downloads** / acesso ao FTP (geralmente um link
   "Acesse os arquivos" ou o ícone de FTP no fim da página).
3. Navegue até: **censo 2022 → setores → formato `shp` (Shapefile) → UF `SP`**.
4. Baixe o `.zip` de **São Paulo (SP)** — ele contém os setores de todos os
   municípios de SP (Sorocaba está dentro; o script filtra pelo código `3552205`).

### Atalho pelo FTP (costuma ser mais rápido)

Raiz do FTP das malhas de setores 2022:
<https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_de_setores_censitarios__divisoes_intramunicipais/censo_2022/setores/>

→ entre em `shp/UF/SP/` e baixe o `.zip` de SP.

### Como reconhecer o arquivo certo

- É um **`.zip`** que, ao descompactar, tem **`.shp` + `.dbf` + `.shx` + `.prj`**
  com o mesmo nome (os quatro juntos formam o shapefile).
- Deve ter uma coluna de município (`CD_MUN` ou similar) e uma de setor
  (`CD_SETOR`, 15 dígitos).

### Onde colocar

Descompacte de forma que os arquivos fiquem em:

```
data/raw/setores_ibge/
    <nome>.shp
    <nome>.dbf
    <nome>.shx
    <nome>.prj
```

---

## Parte B — População por setor (agregados)

**O que é:** o número de habitantes de cada setor. É o **denominador** dos
indicadores "por habitante".

### Caminho pelo site

1. Abra o catálogo dos Agregados por Setor:
   <https://biblioteca.ibge.gov.br/index.php/biblioteca-catalogo?view=detalhes&id=2102136>
2. Vá para os arquivos de download (FTP) dos **Agregados por Setores Censitários
   — Censo 2022**.
3. Baixe o agregado **Básico** (é o que traz a população total). Formato **CSV**.

### Atalho pelo FTP

Raiz do FTP dos agregados 2022:
<https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/>

→ procure o pacote de **agregados básicos** em CSV (nome costuma conter
`basico`). Baixe o do **Brasil** ou, se houver recorte por UF, o de **SP**.

### Como reconhecer o arquivo certo

- É um **`.csv`** (separador `;`, normalmente codificação `latin-1`).
- Tem uma coluna com o **código do setor** (`CD_SETOR` / `CD_GEOCODI`) e a
  **população total**. No agregado Básico, a população costuma estar na coluna
  **`V0001`**.
- Se você abrir e a população estiver em outra coluna, anote o nome dela — você
  passa para o script com `--coluna-pop NOME`.

### Onde colocar

```
data/raw/populacao_ibge/
    <nome>.csv
```

---

## Conferindo

Com as duas pastas preenchidas, rode:

```bash
python data-pipeline/src/step01_setores_populacao.py
```

Você deve ver algo como:

```
✓ Setores de Sorocaba (cód. 3552205): 1.xxx
✓ População juntada: 1.xxx/1.xxx setores com valor (coluna 'V0001')
✓ Mapa de conferência salvo em: data/processed/step01_setores_sorocaba.png
```

Se o script não achar a coluna de população automaticamente, ele **lista as
colunas do CSV** — escolha a da população e rode de novo com
`--coluna-pop NOME`.

---

## Atalho opcional (Python, sem baixar manualmente)

Existe o pacote **`geobr`**, que baixa malhas do IBGE direto pelo Python
(`pip install geobr`). Se preferir esse caminho em vez do download manual, me
avise que eu adapto o `step01` para usá-lo — a fonte continua sendo o IBGE.
