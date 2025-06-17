from fastapi import APIRouter, Depends
from middleware.auth import SignRequired
from models.response import ResponseModel

object_router = APIRouter(
    prefix="/object",
    tags=["object"]
)

@object_router.delete(
    path='/',
    summary='删除对象',
    description='Delete an object endpoint.',
    dependencies=[Depends(SignRequired)]
)
def router_object_delete() -> ResponseModel:
    """
    Delete an object endpoint.
    
    Returns:
        ResponseModel: A model containing the response data for the object deletion.
    """
    ...

@object_router.patch(
    path='/',
    summary='移动对象',
    description='Move an object endpoint.',
    dependencies=[Depends(SignRequired)]
)
def router_object_move() -> ResponseModel:
    """
    Move an object endpoint.
    
    Returns:
        ResponseModel: A model containing the response data for the object move.
    """
    ...

@object_router.post(
    path='/copy',
    summary='复制对象',
    description='Copy an object endpoint.',
    dependencies=[Depends(SignRequired)]
)
def router_object_copy() -> ResponseModel:
    """
    Copy an object endpoint.
    
    Returns:
        ResponseModel: A model containing the response data for the object copy.
    """
    ...

@object_router.post(
    path='/rename',
    summary='重命名对象',
    description='Rename an object endpoint.',
    dependencies=[Depends(SignRequired)]
)
def router_object_rename() -> ResponseModel:
    """
    Rename an object endpoint.
    
    Returns:
        ResponseModel: A model containing the response data for the object rename.
    """
    ...

@object_router.get(
    path='/property/{id}',
    summary='获取对象属性',
    description='Get object properties endpoint.',
    dependencies=[Depends(SignRequired)]
)
def router_object_property(id: str) -> ResponseModel:
    """
    Get object properties endpoint.
    
    Args:
        id (str): The ID of the object to retrieve properties for.
    
    Returns:
        ResponseModel: A model containing the response data for the object properties.
    """
    ...