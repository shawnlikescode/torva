from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class DocumentType(str, Enum):
    TEXT = "text"
    PDF = "pdf"
    MARKDOWN = "markdown"


class DocumentMetadata(BaseModel):
    source: str
    author: Optional[str] = None
    created_at: Optional[str] = None
    document_type: DocumentType
    page_number: Optional[int] = None


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