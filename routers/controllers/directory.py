from fastapi import APIRouter, Depends
from middleware.auth import SignRequired
from models import response

directory_router = APIRouter(
    prefix="/directory",
    tags=["directory"]
)

@directory_router.put(
    path='/',
    summary='创建目录',
    description='Create a directory endpoint.',
    dependencies=[Depends(SignRequired)]
)
def router_directory_create() -> response.ResponseModel:
    """
    Create a directory endpoint.
    
    Returns:
        ResponseModel: A model containing the response data for the directory creation.
    """
    pass

@directory_router.get(
    path='/{path:path}',
    summary='获取目录内容',
    description='Get directory contents endpoint.',
    dependencies=[Depends(SignRequired)]
)
def router_directory_get(path: str) -> response.ResponseModel:
    """
    Get directory contents endpoint.
    
    Args:
        path (str): The path of the directory to retrieve contents from.
    
    Returns:
        ResponseModel: A model containing the response data for the directory contents.
    """
    return response.ResponseModel(
        data=response.DirectoryModel(
            
        )
    )