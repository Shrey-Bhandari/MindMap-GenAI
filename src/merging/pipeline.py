import json
from pathlib import Path
from collections import defaultdict
import math

from src.merging.merger import merge_chunks


def main():

    unit = "UNIT_3"

    units_path = Path(f"data/processed/units_{unit}.jsonl")
    out_dir = Path(f"data/merged/{unit}")
    out_dir.mkdir(parents=True, exist_ok=True)

    chunks = [json.loads(l) for l in units_path.open()]

    # Group by anchor
    anchor_groups = defaultdict(list)
    for chunk in chunks:
        anchor_groups[chunk["anchor"]].append(chunk)

    # Calculate suppression threshold (25% of slides)
    total_slides = 78  # From earlier calculation
    suppression_threshold = total_slides * 0.25  # 19.5

    merged_chunks = []
    for anchor, group in anchor_groups.items():
        # Suppress specific generic anchors entirely
        if anchor in ["general_concept", "mathematical_concept", "cryptographic_primitives"]:
            continue

        # Suppress other anchors that appear in >25% of slides
        if len(group) > suppression_threshold:
            # For over-used anchors, keep but reduce confidence
            for chunk in group:
                chunk["confidence"] = min(chunk["confidence"], 0.4)

        if len(group) == 1:
            merged_chunk = group[0]
        else:
            # Merge all in group
            base = group[0]
            for other in group[1:]:
                base = merge_chunks(base, other)
            merged_chunk = base

        # Fix confidence scaling with bounded curve
        merge_count = len(group)
        base_confidence = merged_chunk["confidence"]
        merged_chunk["confidence"] = min(
            base_confidence + math.log(1 + merge_count) * 0.05,
            0.95
        )

        # Build proper provenance with sources
        sources = []
        for chunk in group:
            ppt = chunk.get("ppt", "unknown")
            slide_ids = chunk.get("slide_ids", [chunk.get("slide_id", 0)])
            for slide_id in slide_ids:
                sources.append({"ppt": ppt, "slide_id": slide_id})

        # Deduplicate sources
        seen = set()
        unique_sources = []
        for source in sources:
            key = (source["ppt"], source["slide_id"])
            if key not in seen:
                seen.add(key)
                unique_sources.append(source)

        merged_chunk["provenance"] = {"sources": unique_sources}

        # Remove ppt from root level
        if "ppt" in merged_chunk:
            del merged_chunk["ppt"]

        merged_chunks.append(merged_chunk)

    with (out_dir / "merged_chunks.jsonl").open("w") as f:
        for c in merged_chunks:
            f.write(json.dumps(c) + "\n")

    print("✅ Phase-4 merging completed.")

if __name__ == "__main__":
    main()
