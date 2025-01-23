from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
import os
from typing import List, Tuple
from langchain.docstore.document import Document
from fastapi import HTTPException


class VectorStoreService:
    def __init__(self):
        # Debug: Print all environment variables
        print("Environment variables:")
        print(f"OPENAI_API_KEY exists: {'OPENAI_API_KEY' in os.environ}")
        print(f"OPENAI_API_KEY from getenv: {os.getenv('OPENAI_API_KEY')}")
        print(f"PINECONE_API_KEY exists: {'PINECONE_API_KEY' in os.environ}")
        print(f"PINECONE_ENVIRONMENT exists: {'PINECONE_ENVIRONMENT' in os.environ}")
        
        # Check for required environment variables
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise HTTPException(
                status_code=500,
                detail="OPENAI_API_KEY environment variable is not set"
            )

        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        if not pinecone_api_key:
            raise HTTPException(
                status_code=500,
                detail="PINECONE_API_KEY not set"
            )

        # Initialize services
        try:
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=openai_api_key,
                model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
            )
            
            # Initialize new Pinecone client
            pc = Pinecone(api_key=pinecone_api_key)
            
            index_name = os.getenv("PINECONE_INDEX_NAME", "knowledgebase")
            self.vectorstore = pc.Index(index_name)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize vector store: {str(e)}"
            )
    
    async def query_similar_documents(self, query: str, k: int = 3) -> List[Tuple[Document, float]]:
        """
        Query the vector store for similar documents.
        
        Args:
            query: The query string to search for
            k: Number of results to return
            
        Returns:
            List of tuples containing (Document, score)
        """
        try:
            return self.vectorstore.similarity_search_with_score(query, k=k)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error querying vector store: {str(e)}"
            ) 