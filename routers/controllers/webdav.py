from fastapi import APIRouter, Depends, Request
from middleware.auth import SignRequired
from models.response import ResponseModel

# WebDAV 管理路由
webdav_router = APIRouter(
    prefix='/webdav',
    tags=["webdav"],
)

@webdav_router.get(
    path='/accounts',
    summary='获取账号信息',
    description='Get account information for WebDAV.',
    dependencies=[Depends(SignRequired)],
)
def router_webdav_accounts() -> ResponseModel:
    """
    Get account information for WebDAV.
    
    Returns:
        ResponseModel: A model containing the response data for the account information.
    """
    ...

@webdav_router.post(
    path='/accounts',
    summary='新建账号',
    description='Create a new WebDAV account.',
    dependencies=[Depends(SignRequired)],
)
def router_webdav_create_account() -> ResponseModel:
    """
    Create a new WebDAV account.
    
    Returns:
        ResponseModel: A model containing the response data for the created account.
    """
    ...

@webdav_router.delete(
    path='/accounts/{id}',
    summary='删除账号',
    description='Delete a WebDAV account by its ID.',
    dependencies=[Depends(SignRequired)],
)
def router_webdav_delete_account(id: str) -> ResponseModel:
    """
    Delete a WebDAV account by its ID.
    
    Args:
        id (str): The ID of the account to be deleted.
    
    Returns:
        ResponseModel: A model containing the response data for the deletion operation.
    """
    ...

@webdav_router.post(
    path='/mount',
    summary='新建目录挂载',
    description='Create a new WebDAV mount point.',
    dependencies=[Depends(SignRequired)],
)
def router_webdav_create_mount() -> ResponseModel:
    """
    Create a new WebDAV mount point.
    
    Returns:
        ResponseModel: A model containing the response data for the created mount point.
    """
    ...

@webdav_router.delete(
    path='/mount/{id}',
    summary='删除目录挂载',
    description='Delete a WebDAV mount point by its ID.',
    dependencies=[Depends(SignRequired)],
)
def router_webdav_delete_mount(id: str) -> ResponseModel:
    """
    Delete a WebDAV mount point by its ID.
    
    Args:
        id (str): The ID of the mount point to be deleted.
    
    Returns:
        ResponseModel: A model containing the response data for the deletion operation.
    """
    ...

@webdav_router.patch(
    path='accounts/{id}',
    summary='更新账号信息',
    description='Update WebDAV account information by ID.',
    dependencies=[Depends(SignRequired)],
)
def router_webdav_update_account(id: str) -> ResponseModel:
    """
    Update WebDAV account information by ID.
    
    Args:
        id (str): The ID of the account to be updated.
    
    Returns:
        ResponseModel: A model containing the response data for the updated account.
    """
    ...