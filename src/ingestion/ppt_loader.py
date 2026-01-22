from pathlib import Path

def list_ppts(unit_dir: Path) -> list[Path]:
    ppt_files = sorted(unit_dir.glob("*.pptx"))
    return ppt_files
