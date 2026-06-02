from pathlib import Path
import yaml

from .vector_store import SearchResult


def load_controls(path: str | Path) -> list[dict]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return data["controls"]


def assess_control(control: dict, evidence: list[SearchResult]) -> dict:
    best_score = max((item.score for item in evidence), default=0.0)
    status = "Pass" if best_score >= 0.10 else "Needs Review"
    rationale = "Relevant evidence was found in the transcript." if status == "Pass" else "Evidence was weak or missing."
    return {
        "control_id": control["id"],
        "framework": control["framework"],
        "title": control["title"],
        "status": status,
        "score": round(best_score, 3),
        "rationale": rationale,
        "citations": [
            {
                "source": result.chunk.source,
                "time": result.chunk.start_time,
                "text": result.chunk.text,
                "score": round(result.score, 3),
            }
            for result in evidence
        ],
    }


def render_markdown_report(results: list[dict]) -> str:
    lines = ["# Compliance Audit Report", ""]
    for result in results:
        lines.extend(
            [
                f"## {result['control_id']} - {result['title']}",
                f"- Framework: {result['framework']}",
                f"- Status: {result['status']}",
                f"- Confidence Score: {result['score']}",
                f"- Rationale: {result['rationale']}",
                "- Evidence:",
            ]
        )
        for citation in result["citations"]:
            time = citation["time"] or "n/a"
            lines.append(f"  - `{citation['source']}` at `{time}`: {citation['text']}")
        lines.append("")
    return "\n".join(lines)
