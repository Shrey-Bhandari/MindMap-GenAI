#!/usr/bin/env python3
"""
Phase-4 Output Validator for RecallGraph
Validates that merged_chunks.jsonl meets all Phase-4 requirements
"""

import json
import sys
from pathlib import Path

def validate_phase4_output(file_path):
    print('🔍 Validating Phase-4 output...')
    print()

    if not Path(file_path).exists():
        print(f'❌ File not found: {file_path}')
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            chunks = [json.loads(line.strip()) for line in f if line.strip()]
    except Exception as e:
        print(f'❌ Error reading file: {e}')
        return False

    print(f'📊 Total chunks: {len(chunks)}')
    print()

    # Check 1: Required fields
    required_fields = ['unit_id', 'anchor', 'compressed_text', 'attributes', 'exam_signals', 'confidence', 'provenance', 'slide_ids']
    missing_fields = []
    for i, chunk in enumerate(chunks):
        for field in required_fields:
            if field not in chunk:
                missing_fields.append(f'Chunk {i} ({chunk.get("anchor", "unknown")}) missing {field}')

    if missing_fields:
        print('❌ Missing required fields:')
        for msg in missing_fields[:5]:  # Show first 5
            print(f'  - {msg}')
        return False
    else:
        print('✅ All required fields present')

    # Check 2: One record per anchor
    anchors = [chunk['anchor'] for chunk in chunks]
    duplicates = [anchor for anchor in set(anchors) if anchors.count(anchor) > 1]
    if duplicates:
        print(f'❌ Duplicate anchors: {duplicates}')
        return False
    else:
        print('✅ One record per anchor')

    # Check 3: No ppt at root
    has_ppt_root = any('ppt' in chunk for chunk in chunks)
    if has_ppt_root:
        print('❌ Found ppt at root level')
        return False
    else:
        print('✅ No ppt at root level')

    # Check 4: Provenance structure
    invalid_provenance = []
    for chunk in chunks:
        prov = chunk.get('provenance', {})
        if 'sources' not in prov:
            invalid_provenance.append(chunk['anchor'])
            continue
        sources = prov['sources']
        if not isinstance(sources, list):
            invalid_provenance.append(chunk['anchor'])
            continue
        for source in sources:
            if not isinstance(source, dict) or 'ppt' not in source or 'slide_id' not in source:
                invalid_provenance.append(chunk['anchor'])
                break

    if invalid_provenance:
        print(f'❌ Invalid provenance structure: {invalid_provenance[:3]}')
        return False
    else:
        print('✅ Provenance has sources array with ppt/slide_id')

    # Check 5: No Phase-2 provenance fields
    has_old_provenance = any(
        'prev_context_used' in str(chunk.get('provenance', {})) or
        'next_context_used' in str(chunk.get('provenance', {}))
        for chunk in chunks
    )
    if has_old_provenance:
        print('❌ Found Phase-2 provenance fields (prev_context_used/next_context_used)')
        return False
    else:
        print('✅ No Phase-2 provenance fields')

    # Check 6: Generic anchors suppressed
    generic_anchors = ['general_concept', 'mathematical_concept', 'cryptographic_primitives']
    found_generic = [anchor for anchor in anchors if anchor in generic_anchors]
    if found_generic:
        print(f'❌ Found generic anchors: {found_generic}')
        return False
    else:
        print('✅ Generic anchors suppressed')

    # Check 7: Confidence values reasonable
    invalid_confidence = [chunk['anchor'] for chunk in chunks if not (0.0 <= chunk['confidence'] <= 1.0)]
    if invalid_confidence:
        print(f'❌ Invalid confidence values: {invalid_confidence}')
        return False
    else:
        print('✅ Confidence values in valid range [0.0, 1.0]')

    # Check 8: Sources deduplicated
    duplicate_sources = []
    for chunk in chunks:
        sources = chunk['provenance']['sources']
        seen = set()
        for source in sources:
            key = (source['ppt'], source['slide_id'])
            if key in seen:
                duplicate_sources.append(chunk['anchor'])
                break
            seen.add(key)

    if duplicate_sources:
        print(f'❌ Duplicate sources found: {duplicate_sources[:3]}')
        return False
    else:
        print('✅ Sources deduplicated')

    print()
    print('🎉 Phase-4 output is VALID!')
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python validate_phase4.py <path_to_merged_chunks.jsonl>')
        sys.exit(1)

    file_path = sys.argv[1]
    success = validate_phase4_output(file_path)
    sys.exit(0 if success else 1)