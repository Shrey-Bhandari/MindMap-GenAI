from src.llm.interface import LLMInterface
import json


class LocalLLM(LLMInterface):
    def generate(self, prompt: str) -> str:
        # Mock implementation: return multiple knowledge chunks per slide
        chunks = [
            {
                "anchor": "fermat_little_theorem",
                "compressed_text": "If p is prime and a not divisible by p, then a^(p-1) ≡ 1 (mod p).",
                "attributes": {
                    "type": "theorem",
                    "domain": "number theory"
                },
                "exam_signals": {
                    "definition": False,
                    "formula": True,
                    "example_present": False,
                    "proof_hint": False
                },
                "confidence": 0.95,
                "provenance": {
                    "prev_context_used": True,
                    "next_context_used": False
                }
            },
            {
                "anchor": "pseudoprime_definition",
                "compressed_text": "Composite numbers satisfying Fermat's test are pseudoprimes.",
                "attributes": {
                    "type": "definition",
                    "domain": "number theory"
                },
                "exam_signals": {
                    "definition": True,
                    "formula": False,
                    "example_present": False,
                    "proof_hint": False
                },
                "confidence": 0.90,
                "provenance": {
                    "prev_context_used": False,
                    "next_context_used": True
                }
            }
        ]
        return json.dumps(chunks)
