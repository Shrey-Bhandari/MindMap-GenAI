from src.extraction.extractor import KnowledgeExtractor
from src.extraction.validator import validate
from src.storage.jsonl_reader import read_jsonl
from src.storage.jsonl_writer import write_jsonl
from src.llm.local_runtime import LocalLLM
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m src.extraction.pipeline <unit_id>")
        sys.exit(1)
    
    unit_id = sys.argv[1]
    slides_path = f"data/processed/slides_json/{unit_id}_slides.jsonl"
    output_path = f"data/processed/units_{unit_id}.jsonl"

    llm = LocalLLM()
    extractor = KnowledgeExtractor(llm)

    all_chunks = []
    for slide in read_jsonl(slides_path):
        chunks = extractor.extract(slide)
        valid_chunks = [chunk.__dict__ for chunk in chunks if validate(chunk)]
        all_chunks.extend(valid_chunks)

    write_jsonl(output_path, all_chunks)


if __name__ == "__main__":
    main()
