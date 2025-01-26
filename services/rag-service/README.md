# RAG Service

A FastAPI-based Retrieval Augmented Generation (RAG) service for Torva. This service provides endpoints for semantic search and document retrieval using OpenAI and Pinecone as the vector store.

## Features

- Semantic search using OpenAI's text-embedding-3-small model (configurable)
- Pinecone vector store integration for efficient similarity search
- Configurable number of search results
- FastAPI for high-performance async API endpoints
- CORS middleware support for cross-origin requests
- Health check endpoint
- Structured response models using Pydantic
- Environment-based configuration

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
```

Required environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: OpenAI model to use (optional)
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_ENVIRONMENT`: Pinecone environment
- `PINECONE_INDEX_NAME`: Name of your Pinecone index (defaults to "knowledgebase")
- `EMBEDDING_MODEL`: OpenAI embedding model (defaults to "text-embedding-3-small")
- `BACKEND_CORS_ORIGINS`: Allowed CORS origins (JSON array)

## Running the Service

Start the development server:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the service is running, you can access:

- Interactive API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## API Endpoints

### Health Check

- `GET /health` - Service health check
  - Returns service status and name

### Queries

- `POST /query` - Query the vector store for similar documents
  - Request body:
    ```json
    {
      "query": "Your search query",
      "max_results": 3 // Optional, defaults to 3
    }
    ```
  - Returns matching documents with similarity scores

## Project Structure

```
src/
├── main.py              # FastAPI app initialization and configuration
├── models/              # Pydantic data models
├── routes/              # API route handlers
└── services/            # Business logic
```

## Error Handling

The service includes comprehensive error handling for:

- Missing environment variables
- Vector store initialization failures
- Query processing errors
- Invalid requests

## Development

The service is built with modern Python async features and follows FastAPI best practices. Future improvements and features will be documented here.
