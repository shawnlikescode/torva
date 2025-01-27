from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class DocumentType(str, Enum):
    TEXT = "text"
    PDF = "pdf"
    MARKDOWN = "markdown"


class DocumentMetadata(BaseModel):
    source: str
    author: str
    created_at: str
    document_type: DocumentType
    page_number: int


class Document(BaseModel):
    content: str
    metadata: DocumentMetadata


class DocumentResponse(BaseModel):
    id: str
    status: str = "success"
    message: Optional[str] = None


class DocumentBatchResponse(BaseModel):
    successful_count: int
    failed_count: int
    errors: Optional[List[str]] = None 