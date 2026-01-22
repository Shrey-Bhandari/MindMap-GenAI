import json
from src.merging.merge_prompt import MERGE_DECISION_PROMPT


def build_merge_prompt(chunk_a, chunk_b):
    return f"""
{MERGE_DECISION_PROMPT}

Chunk A:
Anchor: {chunk_a['anchor']}
Text: {chunk_a['compressed_text']}
Type: {chunk_a['attributes']['type']}
Domain: {chunk_a['attributes']['domain']}

Chunk B:
Anchor: {chunk_b['anchor']}
Text: {chunk_b['compressed_text']}
Type: {chunk_b['attributes']['type']}
Domain: {chunk_b['attributes']['domain']}
"""


def should_merge(llm, chunk_a, chunk_b):
    prompt = build_merge_prompt(chunk_a, chunk_b)
    response = llm.generate(prompt)

    try:
        decision = json.loads(response)
        return decision["merge"], decision["reason"]
    except Exception:
        return False, "invalid_llm_output"
