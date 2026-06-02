FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "-m", "src.pipeline", "--input", "data/sample_transcript.txt", "--output", "reports/sample_audit.md"]
