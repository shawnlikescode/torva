from langchain_openai import OpenAIEmbeddings
from typing import List, Tuple
from langchain.docstore.document import Document
from fastapi import HTTPException
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
import os
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()


class VectorStoreService:
    def __init__(self):
        # Check for required environment variables
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        if not self.pinecone_api_key:
            raise ValueError("PINECONE_API_KEY environment variable is not set")

        self.pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
        if not self.pinecone_env:
            raise ValueError("PINECONE_ENVIRONMENT environment variable is not set")

        self.index_name = os.getenv("PINECONE_INDEX_NAME", "knowledgebase")
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
            openai_api_key=self.openai_api_key
        )

        # Initialize Pinecone client
        self.pinecone = Pinecone(
            api_key=self.pinecone_api_key,
            environment=self.pinecone_env
        )
        
        self.vector_store = None
        self._initialize_store()

    def _initialize_store(self):
        """Initialize connection to Pinecone through LangChain."""
        try:
            # Get or create index
            if self.index_name not in self.pinecone.list_indexes().names():
                self.pinecone.create_index(
                    name=self.index_name,
                    dimension=1536,  # OpenAI embedding dimension
                    metric="cosine"
                )

            # Initialize LangChain's Pinecone wrapper
            self.vector_store = PineconeVectorStore(
                embedding=self.embeddings,
                index=self.pinecone.Index(self.index_name)
            )

        except Exception as e:
            raise ValueError(f"Failed to initialize vector store: {str(e)}")

    async def add_texts(self, texts: List[str], metadatas: List[dict]) -> List[str]:
        """Add texts to the vector store."""
        try:
            return self.vector_store.add_texts(texts=texts, metadatas=metadatas)
        except Exception as e:
            raise ValueError(f"Failed to add texts to vector store: {str(e)}")

    async def similarity_search(
        self,
        query: str,
        k: int = 3
    ) -> List[Tuple[Document, float]]:
        """
        Search for similar documents.
        Returns list of tuples (document, score).
        """
        try:
            results_with_scores = self.vector_store.similarity_search_with_score(
                query,
                k=k
            )
            return results_with_scores
        except Exception as e:
            raise ValueError(f"Failed to search vector store: {str(e)}")


# Singleton instance
_vector_store_service = None


async def get_vector_store() -> VectorStoreService:
    """Get or create vector store service instance."""
    global _vector_store_service
    if _vector_store_service is None:
        _vector_store_service = VectorStoreService()
    return _vector_store_service 