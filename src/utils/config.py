from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_PPTS_DIR = PROJECT_ROOT / "data" / "raw_ppts"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

SLIDES_JSON_DIR = PROCESSED_DIR / "slides_json"
LOGS_DIR = PROCESSED_DIR / "logs"

for p in [SLIDES_JSON_DIR, LOGS_DIR]:
    p.mkdir(parents=True, exist_ok=True)
