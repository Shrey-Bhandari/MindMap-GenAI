EXTRACTION_PROMPT = """
You are a knowledge extraction system for academic content.

INPUT:
Slide text with prev/next context.

TASK:
Extract multiple atomic knowledge chunks from the slide.

RULES:
- Extract 1-5 chunks per slide based on distinct concepts
- Each chunk must be independently understandable
- Do NOT merge concepts across slides
- Preserve repetition if present
- Use prev/next context to enhance extraction

OUTPUT FORMAT (STRICT JSON ARRAY):
[
  {
    "anchor": "snake_case_identifier",
    "compressed_text": "minimal exam-oriented statement",
    "attributes": {
      "type": "definition | theorem | example | algorithm | property | explanation",
      "domain": "cryptography"
    },
    "exam_signals": {
      "definition": true/false,
      "formula": true/false,
      "example_present": true/false,
      "proof_hint": true/false
    },
    "confidence": 0.95,
    "provenance": {
      "prev_context_used": true/false,
      "next_context_used": true/false
    }
  }
]
"""
