# RAG Service

A FastAPI-based Retrieval Augmented Generation (RAG) service for Torva. This service provides endpoints for document ingestion and intelligent querying using OpenAI's GPT-4 and ChromaDB as the vector store.

## Features

- Document ingestion with metadata support
- Semantic search using OpenAI embedding
- RAG-powered question answering
- ChromaDB vector store for efficient similarity search
- FastAPI for high-performance async API endpoints

## Setup

1. Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies using uv:

```bash
uv pip install -r requirements.txt
```

3. Copy the `.env.example` to `.env` and fill in your configuration:

```bash
cp .env.example .env
# Edit .env with your settings, especially the OPENAI_API_KEY
```

4. Create the data directory for ChromaDB:

```bash
mkdir -p data/chroma
```

## Running the Service

Start the development server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the service is running, you can access:

- Interactive API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## API Endpoints

### Health Check

- `GET /` - Service health check

### Documents

- `POST /documents` - Add a document to the RAG system

### Queries

- `POST /query` - Query the RAG system with a question

## Project Structure

```
app/
├── api/           # API route handlers
├── core/          # Core functionality and config
├── models/        # Pydantic models
├── services/      # Business logic
└── utils/         # Utility functions
```

## Development

1. Install development dependencies:

```bash
uv pip install -r requirements-dev.txt  # Coming soon
```

2. Run tests:

```bash
pytest  # Coming soon
```
