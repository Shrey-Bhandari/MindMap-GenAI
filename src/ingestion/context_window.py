from src.ingestion.normalize_text import normalize_text

def build_context_windows(slides: list[dict]) -> list[dict]:
    out = []

    for i in range(len(slides)):
        prev_text = slides[i-1]["text"] if i-1 >= 0 else ""
        next_text = slides[i+1]["text"] if i+1 < len(slides) else ""

        out.append({
            "slide_id": i+1,
            "text": slides[i]["text"],
            "prev_context": normalize_text(prev_text),
            "next_context": normalize_text(next_text),
        })

    return out
