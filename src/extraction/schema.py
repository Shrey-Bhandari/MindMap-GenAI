from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class KnowledgeChunk:
    unit_id: str
    ppt: str
    slide_id: int
    anchor: str
    compressed_text: str
    attributes: Dict[str, Any]
    exam_signals: Dict[str, bool]
    confidence: float
    provenance: Dict[str, bool]
