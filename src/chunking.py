from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class EvidenceChunk:
    chunk_id: str
    text: str
    source: str
    start_time: str | None = None


TIMESTAMP_RE = re.compile(r"^(\d{1,2}:\d{2}(?::\d{2})?)\s+(.*)$")


def load_transcript(path: str | Path) -> list[EvidenceChunk]:
    source = Path(path)
    chunks: list[EvidenceChunk] = []
    for index, raw_line in enumerate(source.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        match = TIMESTAMP_RE.match(line)
        start_time, text = (match.group(1), match.group(2)) if match else (None, line)
        chunks.append(EvidenceChunk(f"{source.stem}-{index}", text, source.name, start_time))
    return chunks


def combine_short_chunks(chunks: list[EvidenceChunk], min_words: int = 18) -> list[EvidenceChunk]:
    combined: list[EvidenceChunk] = []
    buffer: list[EvidenceChunk] = []

    def flush() -> None:
        if not buffer:
            return
        first = buffer[0]
        text = " ".join(item.text for item in buffer)
        combined.append(EvidenceChunk(first.chunk_id, text, first.source, first.start_time))
        buffer.clear()

    for chunk in chunks:
        buffer.append(chunk)
        if len(" ".join(item.text for item in buffer).split()) >= min_words:
            flush()
    flush()
    return combined
