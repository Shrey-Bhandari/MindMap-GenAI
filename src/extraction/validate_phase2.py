import json
import sys
from pathlib import Path

REQUIRED_TOP_LEVEL_KEYS = {
    "unit_id",
    "ppt",
    "slide_id",
    "anchor",
    "compressed_text",
    "attributes",
    "exam_signals",
    "confidence",
    "provenance"
}

REQUIRED_ATTRIBUTE_KEYS = {"type", "domain"}
REQUIRED_EXAM_SIGNAL_KEYS = {
    "definition",
    "formula",
    "example_present",
    "proof_hint"
}
REQUIRED_PROVENANCE_KEYS = {
    "prev_context_used",
    "next_context_used"
}


def validate_chunk(chunk, line_no):
    errors = []

    # Top-level keys
    missing = REQUIRED_TOP_LEVEL_KEYS - chunk.keys()
    if missing:
        errors.append(f"Missing top-level keys: {missing}")

    # anchor
    if "anchor" in chunk and not chunk["anchor"].islower():
        errors.append("anchor must be lowercase snake_case")

    # compressed_text
    if "compressed_text" in chunk and len(chunk["compressed_text"].strip()) == 0:
        errors.append("compressed_text is empty")

    # confidence
    if "confidence" in chunk:
        c = chunk["confidence"]
        if not isinstance(c, (float, int)) or not (0.0 <= c <= 1.0):
            errors.append("confidence must be float between 0 and 1")

    # attributes
    attrs = chunk.get("attributes", {})
    if set(attrs.keys()) != REQUIRED_ATTRIBUTE_KEYS:
        errors.append("attributes must contain exactly: type, domain")

    # exam_signals
    exam = chunk.get("exam_signals", {})
    if set(exam.keys()) != REQUIRED_EXAM_SIGNAL_KEYS:
        errors.append(
            "exam_signals must contain exactly: "
            "definition, formula, example_present, proof_hint"
        )

    # provenance
    prov = chunk.get("provenance", {})
    if set(prov.keys()) != REQUIRED_PROVENANCE_KEYS:
        errors.append(
            "provenance must contain exactly: "
            "prev_context_used, next_context_used"
        )

    if errors:
        raise ValueError(
            f"\n❌ Validation failed at line {line_no}:\n- "
            + "\n- ".join(errors)
        )


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m src.extraction.validate_phase2 <units_jsonl>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        raise FileNotFoundError(path)

    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            chunk = json.loads(line)
            validate_chunk(chunk, i)

    print("✅ Phase-2 validation PASSED. Output is compliant.")


if __name__ == "__main__":
    main()
