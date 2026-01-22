def merge_chunks(base, other):
    merged = dict(base)

    # Combine slide_ids into a list
    if "slide_id" in base:
        base_ids = [base["slide_id"]]
    elif "slide_ids" in base:
        base_ids = base["slide_ids"]
    else:
        base_ids = []

    if "slide_id" in other:
        other_ids = [other["slide_id"]]
    elif "slide_ids" in other:
        other_ids = other["slide_ids"]
    else:
        other_ids = []

    merged["slide_ids"] = sorted(set(base_ids + other_ids))

    # Remove old slide_id if present
    if "slide_id" in merged:
        del merged["slide_id"]

    # Boost confidence
    merged["confidence"] = min(
        1.0,
        base["confidence"] + 0.1 * other["confidence"]
    )

    # Merge provenance
    merged["provenance"] = {
        "prev_context_used": base["provenance"]["prev_context_used"] or other["provenance"]["prev_context_used"],
        "next_context_used": base["provenance"]["next_context_used"] or other["provenance"]["next_context_used"]
    }

    # Merge exam_signals (take max)
    merged["exam_signals"] = {
        k: base["exam_signals"][k] or other["exam_signals"][k]
        for k in base["exam_signals"]
    }

    return merged
