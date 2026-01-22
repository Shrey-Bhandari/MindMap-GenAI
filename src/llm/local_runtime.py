from src.llm.interface import LLMInterface
import json


class LocalLLM(LLMInterface):
    def generate(self, prompt: str) -> str:
        # Mock implementation: return multiple knowledge chunks per slide
        if "MERGE_DECISION_PROMPT" in prompt:
            # For merge decisions, check if anchors are the same
            if "Anchor:" in prompt:
                lines = prompt.split('\n')
                anchor_a = None
                anchor_b = None
                for line in lines:
                    if line.startswith("Anchor:"):
                        if anchor_a is None:
                            anchor_a = line.split("Anchor: ")[1]
                        else:
                            anchor_b = line.split("Anchor: ")[1]
                            break
                if anchor_a == anchor_b:
                    return '{"merge": true, "reason": "same anchor"}'
                else:
                    return '{"merge": false, "reason": "different anchors"}'
            return '{"merge": false, "reason": "no anchors found"}'
        else:
            # Mock extraction: return varied knowledge chunks based on slide content
            slide_text = ""
            if "SLIDE TEXT:\n" in prompt:
                slide_text = prompt.split("SLIDE TEXT:\n", 1)[1].split("\n\nPREV CONTEXT:")[0].strip()

            chunks = []

            if "Fermat" in slide_text:
                chunks.append({
                    "anchor": "fermat_little_theorem",
                    "compressed_text": "If p is prime and a not divisible by p, then a^(p-1) ≡ 1 (mod p).",
                    "attributes": {"type": "theorem", "domain": "number theory"},
                    "exam_signals": {"definition": False, "formula": True, "example_present": False, "proof_hint": False},
                    "confidence": 0.95,
                    "provenance": {"prev_context_used": True, "next_context_used": False}
                })

            if "Pseudoprime" in slide_text:
                chunks.append({
                    "anchor": "pseudoprime_definition",
                    "compressed_text": "Composite numbers satisfying Fermat's test are pseudoprimes.",
                    "attributes": {"type": "definition", "domain": "number theory"},
                    "exam_signals": {"definition": True, "formula": False, "example_present": False, "proof_hint": False},
                    "confidence": 0.90,
                    "provenance": {"prev_context_used": False, "next_context_used": True}
                })

            if "Euler" in slide_text:
                chunks.append({
                    "anchor": "euler_theorem",
                    "compressed_text": "Generalization of Fermat's theorem for any modulus.",
                    "attributes": {"type": "theorem", "domain": "number theory"},
                    "exam_signals": {"definition": False, "formula": True, "example_present": False, "proof_hint": False},
                    "confidence": 0.92,
                    "provenance": {"prev_context_used": True, "next_context_used": False}
                })

            if "Euclidean" in slide_text:
                chunks.append({
                    "anchor": "euclidean_algorithm",
                    "compressed_text": "Method for computing greatest common divisor.",
                    "attributes": {"type": "algorithm", "domain": "number theory"},
                    "exam_signals": {"definition": False, "formula": False, "example_present": True, "proof_hint": False},
                    "confidence": 0.88,
                    "provenance": {"prev_context_used": False, "next_context_used": True}
                })

            if "Chinese Remainder" in slide_text:
                chunks.append({
                    "anchor": "chinese_remainder_theorem",
                    "compressed_text": "Solves systems of simultaneous congruences with coprime moduli.",
                    "attributes": {"type": "theorem", "domain": "number theory"},
                    "exam_signals": {"definition": True, "formula": True, "example_present": True, "proof_hint": False},
                    "confidence": 0.94,
                    "provenance": {"prev_context_used": True, "next_context_used": True}
                })

            if "Diffie-Hellman" in slide_text:
                chunks.append({
                    "anchor": "diffie_hellman_key_exchange",
                    "compressed_text": "Key exchange algorithm using discrete logarithms.",
                    "attributes": {"type": "algorithm", "domain": "cryptography"},
                    "exam_signals": {"definition": True, "formula": False, "example_present": True, "proof_hint": False},
                    "confidence": 0.91,
                    "provenance": {"prev_context_used": False, "next_context_used": False}
                })

            if "RSA" in slide_text:
                chunks.append({
                    "anchor": "rsa_algorithm",
                    "compressed_text": "Public-key cryptosystem using prime factorization.",
                    "attributes": {"type": "algorithm", "domain": "cryptography"},
                    "exam_signals": {"definition": True, "formula": True, "example_present": False, "proof_hint": False},
                    "confidence": 0.96,
                    "provenance": {"prev_context_used": True, "next_context_used": False}
                })

            if "Elliptic Curve" in slide_text:
                chunks.append({
                    "anchor": "elliptic_curve_cryptography",
                    "compressed_text": "Cryptography based on elliptic curve mathematics.",
                    "attributes": {"type": "algorithm", "domain": "cryptography"},
                    "exam_signals": {"definition": True, "formula": False, "example_present": False, "proof_hint": False},
                    "confidence": 0.89,
                    "provenance": {"prev_context_used": False, "next_context_used": True}
                })

            # If no specific chunks, add a general one
            if not chunks:
                chunks.append({
                    "anchor": "general_concept",
                    "compressed_text": "Basic concept in cryptography and number theory.",
                    "attributes": {"type": "definition", "domain": "cryptography"},
                    "exam_signals": {"definition": True, "formula": False, "example_present": False, "proof_hint": False},
                    "confidence": 0.80,
                    "provenance": {"prev_context_used": False, "next_context_used": False}
                })

            # Add a second chunk for variety (similar to original behavior)
            if len(chunks) == 1:
                # Add a complementary chunk based on the first one
                first_anchor = chunks[0]["anchor"]
                if first_anchor == "fermat_little_theorem":
                    chunks.append({
                        "anchor": "number_theory_fundamentals",
                        "compressed_text": "Core principles of modular arithmetic and primality testing.",
                        "attributes": {"type": "definition", "domain": "number theory"},
                        "exam_signals": {"definition": True, "formula": False, "example_present": False, "proof_hint": False},
                        "confidence": 0.85,
                        "provenance": {"prev_context_used": True, "next_context_used": False}
                    })
                elif first_anchor in ["rsa_algorithm", "diffie_hellman_key_exchange", "elliptic_curve_cryptography"]:
                    chunks.append({
                        "anchor": "cryptographic_primitives",
                        "compressed_text": "Fundamental building blocks of modern cryptography.",
                        "attributes": {"type": "definition", "domain": "cryptography"},
                        "exam_signals": {"definition": True, "formula": False, "example_present": False, "proof_hint": False},
                        "confidence": 0.82,
                        "provenance": {"prev_context_used": False, "next_context_used": True}
                    })
                else:
                    chunks.append({
                        "anchor": "mathematical_concept",
                        "compressed_text": "Key mathematical concept with applications in computer science.",
                        "attributes": {"type": "definition", "domain": "mathematics"},
                        "exam_signals": {"definition": True, "formula": False, "example_present": False, "proof_hint": False},
                        "confidence": 0.78,
                        "provenance": {"prev_context_used": False, "next_context_used": False}
                    })

            return json.dumps(chunks)
