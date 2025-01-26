from pydantic import BaseModel
from typing import List, Optional
from .document import Document, DocumentMetadata


class QueryRequest(BaseModel):
    query: str
    max_results: Optional[int] = 3


class ScoredDocument(Document):
    """Extends the base Document model to include a similarity score."""
    score: float


class QueryResponse(BaseModel):
    matches: List[ScoredDocument]
    query: str 