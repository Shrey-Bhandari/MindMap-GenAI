MERGE_DECISION_PROMPT = """
You are deciding whether two knowledge chunks represent the SAME concept.

Rules:
- Do NOT merge if one is definition and the other is example
- Do NOT merge if scopes differ
- Merge only if meaning is equivalent for exam revision

Return JSON ONLY:

{
  "merge": true | false,
  "reason": "short explanation"
}
"""
