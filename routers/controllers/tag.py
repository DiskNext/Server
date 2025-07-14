from fastapi import APIRouter, Depends
from middleware.auth import SignRequired
from models.response import ResponseModel

tag_router = APIRouter(
    prefix='/tag',
    tags=["tag"],
)

@tag_router.post(
    path='/filter',
    summary='创建文件分类标签',
    description='Create a file classification tag.',
    dependencies=[Depends(SignRequired)],
)
def router_tag_create_filter() -> ResponseModel:
    """
    Create a file classification tag.
    
    Returns:
        ResponseModel: A model containing the response data for the created tag.
    """
    pass

@tag_router.post(
    path='/link',
    summary='创建目录快捷方式标签',
    description='Create a directory shortcut tag.',
    dependencies=[Depends(SignRequired)],
)
def router_tag_create_link() -> ResponseModel:
    """
    Create a directory shortcut tag.
    
    Returns:
        ResponseModel: A model containing the response data for the created tag.
    """
    pass

@tag_router.delete(
    path='/{id}',
    summary='删除标签',
    description='Delete a tag by its ID.',
    dependencies=[Depends(SignRequired)],
)
def router_tag_delete(id: str) -> ResponseModel:
    """
    Delete a tag by its ID.
    
    Args:
        id (str): The ID of the tag to be deleted.
    
    Returns:
        ResponseModel: A model containing the response data for the deletion operation.
    """
    pass