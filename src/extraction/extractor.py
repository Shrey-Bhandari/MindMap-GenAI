import json
from typing import List

from src.extraction.schema import KnowledgeChunk
from src.extraction.prompt import EXTRACTION_PROMPT
from src.llm.interface import LLMInterface


class KnowledgeExtractor:
    def __init__(self, llm: LLMInterface):
        self.llm = llm

    def extract(self, slide_record: dict) -> List[KnowledgeChunk]:
        prompt = (
            EXTRACTION_PROMPT
            + "\n\nSLIDE TEXT:\n"
            + slide_record["text"]
            + "\n\nPREV CONTEXT:\n"
            + slide_record.get("prev_context", "")
            + "\n\nNEXT CONTEXT:\n"
            + slide_record.get("next_context", "")
        )

        raw = self.llm.generate(prompt)
        parsed = json.loads(raw)

        chunks = []
        for obj in parsed:
            chunks.append(
                KnowledgeChunk(
                    unit_id=slide_record["unit_id"],
                    ppt=slide_record["ppt"],
                    slide_id=slide_record["slide_id"],
                    anchor=obj["anchor"],
                    compressed_text=obj["compressed_text"],
                    attributes=obj["attributes"],
                    exam_signals=obj["exam_signals"],
                    confidence=obj["confidence"],
                    provenance=obj["provenance"],
                )
            )
        return chunks
