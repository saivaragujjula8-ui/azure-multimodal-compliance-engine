import argparse
from pathlib import Path

from .auditor import assess_control, load_controls, render_markdown_report
from .chunking import combine_short_chunks, load_transcript
from .embeddings import get_embedding_model
from .vector_store import InMemoryVectorStore


def run_pipeline(input_path: str, controls_path: str, output_path: str) -> str:
    embedding_model = get_embedding_model()
    store = InMemoryVectorStore()

    chunks = combine_short_chunks(load_transcript(input_path))
    for chunk in chunks:
        store.add(chunk, embedding_model.embed(chunk.text))

    results = []
    for control in load_controls(controls_path):
        query = f"{control['title']} {control['requirement']}"
        evidence = store.search(embedding_model.embed(query), top_k=3)
        results.append(assess_control(control, evidence))

    report = render_markdown_report(results)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run compliance audit RAG pipeline.")
    parser.add_argument("--input", required=True, help="Transcript path")
    parser.add_argument("--controls", default="controls/controls.yaml")
    parser.add_argument("--output", default="reports/audit_report.md")
    args = parser.parse_args()
    run_pipeline(args.input, args.controls, args.output)


if __name__ == "__main__":
    main()
