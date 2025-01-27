from datetime import datetime
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from typing import List, Optional
import tempfile
import os
import httpx

from ..models.document import Document, DocumentType, DocumentMetadata
from .vector_store import get_vector_store


class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.embeddings = OpenAIEmbeddings(
            model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        )
        self.http_client = httpx.AsyncClient()

    async def process_text(self, content: str, metadata: DocumentMetadata) -> List[Document]:
        texts = self.text_splitter.split_text(content)
        return [
            Document(content=text, metadata=metadata)
            for text in texts
        ]

    async def download_file(self, url: str) -> bytes:
        """Download file from URL."""
        try:
            response = await self.http_client.get(url)
            response.raise_for_status()
            return response.content
        except httpx.HTTPError as e:
            raise ValueError(f"Failed to download file from {url}: {str(e)}")

    async def process_file_from_url(self, file_url: str, filename: str, document_type: DocumentType) -> List[Document]:
        """Process a file from a URL."""
        file_content = await self.download_file(file_url)
        return await self.process_file(file_content, filename, document_type)

    async def process_file(self, file_content: bytes, filename: str, document_type: DocumentType) -> List[Document]:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file.flush()

            try:
                if document_type == DocumentType.PDF:
                    loader = PyPDFLoader(temp_file.name)
                elif document_type == DocumentType.MARKDOWN:
                    loader = UnstructuredMarkdownLoader(temp_file.name)
                elif document_type == DocumentType.TEXT:
                    loader = TextLoader(temp_file.name)
                else:
                    raise ValueError(f"Unsupported document type: {document_type}")

                documents = loader.load()
                processed_docs = []

                for doc in documents:
                    metadata = DocumentMetadata(
                        source=filename,
                        document_type=document_type,
                        author=doc.metadata.get("author") if "author" in doc.metadata else "",
                        created_at=doc.metadata.get("created_at") if "created_at" in doc.metadata else datetime.now().isoformat(),
                        page_number=doc.metadata.get("page") if "page" in doc.metadata else 1
                    )
                    chunks = await self.process_text(doc.page_content, metadata)
                    processed_docs.extend(chunks)

                return processed_docs
            finally:
                os.unlink(temp_file.name)

    async def ingest_documents(self, documents: List[Document]) -> None:
        vector_store = await get_vector_store()
        
        # Convert documents to the format expected by the vector store
        texts = [doc.content for doc in documents]
        metadatas = [doc.metadata.dict() for doc in documents]
        
        # Add documents to the vector store
        await vector_store.add_texts(texts=texts, metadatas=metadatas)

    async def close(self):
        """Close the HTTP client."""
        await self.http_client.aclose() 