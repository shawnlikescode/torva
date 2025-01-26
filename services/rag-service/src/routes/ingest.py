from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Depends
from typing import List, Optional
import uuid
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from ..models.document import Document, DocumentType, DocumentMetadata, DocumentResponse, DocumentBatchResponse
from ..services.document_processor import DocumentProcessor

router = APIRouter(prefix="/ingest", tags=["ingestion"])
document_processor = DocumentProcessor()


class TextIngestRequest(BaseModel):
    """Request model for text ingestion."""
    content: str
    metadata: DocumentMetadata

class FileUrlRequest(BaseModel):
    """Request model for file URL ingestion."""
    file_url: HttpUrl
    filename: str
    metadata: DocumentMetadata

class BatchFileRequest(BaseModel):
    """Request model for batch file ingestion."""
    file_url: HttpUrl
    filename: str
    metadata: DocumentMetadata


@router.post("/text", response_model=DocumentResponse)
async def ingest_text(request: TextIngestRequest) -> DocumentResponse:
    try:
        metadata = DocumentMetadata(
            source=request.metadata.source,
            document_type=request.metadata.document_type,
            author=request.metadata.author if request.metadata.author else "",
            created_at=datetime.now().isoformat(),
            page_number=request.metadata.page_number if request.metadata.page_number else 1
        )

        chunks = await document_processor.process_text(request.content, metadata)
        await document_processor.ingest_documents(chunks)
        
        return DocumentResponse(
            id=str(uuid.uuid4()),
            status="success",
            message=f"Successfully processed and ingested text from {request.metadata.source}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/file/url", response_model=DocumentResponse)
async def ingest_file_url(request: FileUrlRequest) -> DocumentResponse:
    """Ingest a file from a URL (triggered by QStash after UploadThing completion)."""
    document_type = request.metadata.document_type

    if document_type is None:
        # Infer document type from filename
        if request.filename.endswith(".pdf"):
            document_type = DocumentType.PDF
        elif request.filename.endswith(".md"):
            document_type = DocumentType.MARKDOWN
        elif request.filename.endswith(".txt"):
            document_type = DocumentType.TEXT
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please provide a PDF, Markdown, or text file."
            )

    try:
        chunks = await document_processor.process_file_from_url(
            str(request.file_url),
            request.filename,
            document_type
        )
        await document_processor.ingest_documents(chunks)

        return DocumentResponse(
            id=str(uuid.uuid4()),
            status="success",
            message=f"Successfully processed and ingested file: {request.filename}"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch/files", response_model=DocumentBatchResponse)
async def ingest_batch_files(files: List[BatchFileRequest]) -> DocumentBatchResponse:
    """
    Batch ingest files from URLs.
    Each file will be downloaded, processed according to its type, and split into chunks.
    """
    successful_count = 0
    failed_count = 0
    errors = []
    processed_chunks = []

    for file_request in files:
        document_type = file_request.document_type

        # Infer document type if not provided
        if document_type is None:
            if file_request.filename.endswith(".pdf"):
                document_type = DocumentType.PDF
            elif file_request.filename.endswith(".md"):
                document_type = DocumentType.MARKDOWN
            elif file_request.filename.endswith(".txt"):
                document_type = DocumentType.TEXT
            else:
                failed_count += 1
                errors.append(f"Unsupported file type for {file_request.filename}")
                continue

        try:
            # Process file from URL
            chunks = await document_processor.process_file_from_url(
                str(file_request.file_url),
                file_request.filename,
                document_type
            )
            
            # Update metadata if provided
            if file_request.metadata:
                for chunk in chunks:
                    chunk.metadata = DocumentMetadata(
                        **{**chunk.metadata.model_dump(), **file_request.metadata}
                    )
            
            processed_chunks.extend(chunks)
            successful_count += 1
        except Exception as e:
            failed_count += 1
            errors.append(f"Failed to process file {file_request.filename}: {str(e)}")

    if processed_chunks:
        try:
            # Ingest all successfully processed chunks
            await document_processor.ingest_documents(processed_chunks)
        except Exception as e:
            # If ingestion fails, count all documents as failed
            return DocumentBatchResponse(
                successful_count=0,
                failed_count=len(files),
                errors=[f"Ingestion failed: {str(e)}"]
            )

    return DocumentBatchResponse(
        successful_count=successful_count,
        failed_count=failed_count,
        errors=errors if errors else None
    )


@router.post("/batch/text", response_model=DocumentBatchResponse)
async def ingest_batch_text(documents: List[Document]) -> DocumentBatchResponse:
    """
    Batch ingest text documents.
    Each document will be split into chunks before ingestion.
    """
    successful_count = 0
    failed_count = 0
    errors = []
    processed_chunks = []

    for doc in documents:
        try:
            # Process each document into chunks
            chunks = await document_processor.process_text(
                content=doc.content,
                metadata=doc.metadata
            )
            processed_chunks.extend(chunks)
            successful_count += 1
        except Exception as e:
            failed_count += 1
            errors.append(f"Failed to process document {doc.metadata.source}: {str(e)}")

    if processed_chunks:
        try:
            # Ingest all successfully processed chunks
            await document_processor.ingest_documents(processed_chunks)
        except Exception as e:
            # If ingestion fails, count all documents as failed
            return DocumentBatchResponse(
                successful_count=0,
                failed_count=len(documents),
                errors=[f"Ingestion failed: {str(e)}"]
            )

    return DocumentBatchResponse(
        successful_count=successful_count,
        failed_count=failed_count,
        errors=errors if errors else None
    ) 