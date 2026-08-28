"""Caminhos centrais do pipeline.

Mantém todos os diretórios num único lugar, para os scripts não repetirem
lógica de path. Assume a estrutura de pastas descrita no README do projeto.
"""
from pathlib import Path

# .../data-pipeline/src/paths.py  ->  raiz do repositório
ROOT = Path(__file__).resolve().parents[2]

DATA_PIPELINE = ROOT / "data-pipeline"
CONFIG_DIR = DATA_PIPELINE / "config"
REGIONS_YAML = CONFIG_DIR / "regions.yaml"

DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"

# Subpastas esperadas dentro de data/raw (você cria ao baixar cada fonte)
RAW_SETORES = DATA_RAW / "setores_ibge"      # shapefile da malha de setores
RAW_POPULACAO = DATA_RAW / "populacao_ibge"  # CSV de população por setor


def garantir_pastas() -> None:
    """Cria as pastas de saída se não existirem."""
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
