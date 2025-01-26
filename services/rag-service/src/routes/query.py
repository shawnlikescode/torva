from fastapi import APIRouter, HTTPException, Depends
from ..models.query import QueryRequest, QueryResponse, ScoredDocument
from ..models.document import DocumentMetadata
from ..services.vector_store import VectorStoreService


router = APIRouter(tags=["search"])


def get_vector_store_service():
    try:
        return VectorStoreService()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize service: {str(e)}"
        )


@router.post("/query", response_model=QueryResponse)
async def query_documents(
    request: QueryRequest,
    vector_store: VectorStoreService = Depends(get_vector_store_service)
) -> QueryResponse:
    try:
        results = await vector_store.similarity_search(
            request.query,
            k=request.max_results
        )
        
        matches = []
        for doc, score in results:
            # Convert the metadata dict back to our DocumentMetadata model
            metadata = DocumentMetadata(**doc.metadata)
            matches.append(
                ScoredDocument(
                    content=doc.page_content,
                    metadata=metadata,
                    score=score
                )
            )
        
        return QueryResponse(
            matches=matches,
            query=request.query
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Query failed: {str(e)}"
        )