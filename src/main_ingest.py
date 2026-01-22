from pathlib import Path
from tqdm import tqdm

from pathlib import Path
from tqdm import tqdm

from src.utils.config import RAW_PPTS_DIR, SLIDES_JSON_DIR
from src.utils.io import write_jsonl
from src.utils.logger import get_logger

from src.ingestion.ppt_loader import list_ppts
from src.ingestion.slide_extractor import extract_slide_text
from src.ingestion.context_window import build_context_windows



logger = get_logger("phase1_ingestion")

def ingest_unit(unit_id: str):
    unit_path = RAW_PPTS_DIR / unit_id
    if not unit_path.exists():
        raise FileNotFoundError(f"Unit folder not found: {unit_path}")

    ppt_files = list_ppts(unit_path)
    if not ppt_files:
        raise ValueError(f"No PPTX files found in: {unit_path}")

    all_records = []
    for ppt_path in tqdm(ppt_files, desc=f"Ingesting {unit_id}"):
        logger.info(f"Processing: {ppt_path.name}")

        slides = extract_slide_text(str(ppt_path))
        slides_ctx = build_context_windows(slides)

        for s in slides_ctx:
            all_records.append({
                "unit_id": unit_id,
                "ppt": ppt_path.name,
                "slide_id": s["slide_id"],
                "text": s["text"],
                "prev_context": s["prev_context"],
                "next_context": s["next_context"]
            })

    out_path = SLIDES_JSON_DIR / f"{unit_id}_slides.jsonl"
    write_jsonl(out_path, all_records)

    logger.info(f"Saved: {out_path}")
    logger.info(f"Total slides extracted: {len(all_records)}")

def main():
    # Example: process all UNIT folders automatically
    unit_dirs = sorted([p for p in RAW_PPTS_DIR.iterdir() if p.is_dir()])
    if not unit_dirs:
        raise ValueError("No UNIT directories found under data/raw_ppts/")

    for u in unit_dirs:
        ingest_unit(u.name)

if __name__ == "__main__":
    main()
