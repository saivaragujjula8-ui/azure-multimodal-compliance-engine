# Azure Multi-Modal Compliance Engine

LangGraph-style RAG pipeline for ingesting videos, creating searchable evidence, and automating compliance audits against SOC 2 and GDPR controls.

This repo is GitHub-ready and designed to run in two modes:

- **Local demo mode:** deterministic embeddings and mock LLM output, no cloud credentials required.
- **Azure mode:** Azure OpenAI, Azure AI Search, and Blob Storage can be wired through environment variables.

## Features

- Video transcript ingestion from `.txt`, `.vtt`, or `.srt` transcript files
- Chunking, metadata enrichment, and embedding generation
- Vector search over compliance evidence
- Audit report generation with citations
- SOC 2 and GDPR control mapping
- CLI entry points, tests, Dockerfile, and GitHub Actions CI

## Architecture

```text
Video/Transcript -> Chunker -> Embeddings -> Vector Store -> Retriever -> Compliance Auditor -> Report
```

The production design maps to Azure services:

- Azure Blob Storage for raw videos and transcript artifacts
- Azure AI Search for vector indexing
- Azure OpenAI for embeddings and audit generation
- Azure Container Apps or AKS for deployment

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.pipeline --input data/sample_transcript.txt --output reports/sample_audit.md
```

Run tests:

```bash
pytest
```

## Configuration

Copy `.env.example` to `.env` and fill values when using Azure services.

```text
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o-mini
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_API_KEY=
AZURE_SEARCH_INDEX=compliance-evidence
```

## Repository Structure

```text
src/
  auditor.py        # compliance answer and report generation
  chunking.py       # transcript chunking
  config.py         # environment settings
  embeddings.py     # local and Azure embedding adapters
  pipeline.py       # CLI orchestration
  vector_store.py   # in-memory vector index demo
controls/
  controls.yaml     # SOC 2 and GDPR controls
data/
  sample_transcript.txt
reports/
tests/
```

