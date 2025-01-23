from fastapi import APIRouter, HTTPException, Depends
from ..models.query import QueryRequest, QueryResponse, Document
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
):
    
    return QueryResponse(
        matches=[],
        query=request.query
    )