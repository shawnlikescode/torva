from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    query: str
    max_results: Optional[int] = 3


class Document(BaseModel):
    content: str
    metadata: dict
    score: float


class QueryResponse(BaseModel):
    matches: List[Document]
    query: str 