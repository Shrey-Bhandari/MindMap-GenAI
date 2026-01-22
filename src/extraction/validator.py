from src.extraction.schema import KnowledgeChunk

def validate(chunk: KnowledgeChunk) -> bool:
    if not chunk.unit_id.strip():
        return False
    if not chunk.ppt.strip():
        return False
    if chunk.slide_id < 1:
        return False
    if not chunk.anchor.strip():
        return False
    if not chunk.compressed_text.strip():
        return False
    if len(chunk.compressed_text.split()) < 3:
        return False
    if not chunk.attributes.get("type") or not chunk.attributes.get("domain"):
        return False
    if not isinstance(chunk.exam_signals, dict):
        return False
    if not (0 <= chunk.confidence <= 1):
        return False
    if not isinstance(chunk.provenance, dict):
        return False
    return True
