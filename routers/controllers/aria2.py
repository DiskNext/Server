from fastapi import APIRouter, Depends
from middleware.auth import SignRequired
from models.response import ResponseModel

aria2_router = APIRouter(
    prefix="/aria2",
    tags=["aria2"]
)

@aria2_router.post(
    path='/url',
    summary='创建URL下载任务',
    description='Create a URL download task endpoint.',
    dependencies=[Depends(SignRequired)]
)
def router_aria2_url() -> ResponseModel:
    """
    Create a URL download task endpoint.
    
    Returns:
        ResponseModel: A model containing the response data for the URL download task.
    """
    ...

@aria2_router.post(
    path='/torrent/{id}',
    summary='创建种子下载任务',
    description='Create a torrent download task endpoint.',
    dependencies=[Depends(SignRequired)]
)
def router_aria2_torrent(id: str) -> ResponseModel:
    """
    Create a torrent download task endpoint.
    
    Args:
        id (str): The ID of the torrent to download.
    
    Returns:
        ResponseModel: A model containing the response data for the torrent download task.
    """
    ...

@aria2_router.put(
    path='/select/{gid}',
    summary='重新选择要下载的文件',
    description='Re-select files to download endpoint.',
    dependencies=[Depends(SignRequired)]
)
def router_aria2_select(gid: str) -> ResponseModel:
    """
    Re-select files to download endpoint.
    
    Args:
        gid (str): The GID of the download task.
    
    Returns:
        ResponseModel: A model containing the response data for the re-selection of files.
    """
    ...

@aria2_router.delete(
    path='/task/{gid}',
    summary='取消或删除下载任务',
    description='Delete a download task endpoint.',
    dependencies=[Depends(SignRequired)]
)
def router_aria2_delete(gid: str) -> ResponseModel:
    """
    Delete a download task endpoint.
    
    Args:
        gid (str): The GID of the download task to delete.
    
    Returns:
        ResponseModel: A model containing the response data for the deletion of the download task.
    """
    ...

@aria2_router.get(
    '/downloading',
    summary='获取正在下载中的任务',
    description='Get currently downloading tasks endpoint.',
    dependencies=[Depends(SignRequired)]
)
def router_aria2_downloading() -> ResponseModel:
    """
    Get currently downloading tasks endpoint.
    
    Returns:
        ResponseModel: A model containing the response data for currently downloading tasks.
    """
    ...

@aria2_router.get(
    path='/finished',
    summary='获取已完成的任务',
    description='Get finished tasks endpoint.',
    dependencies=[Depends(SignRequired)]
)
def router_aria2_finished() -> ResponseModel:
    """
    Get finished tasks endpoint.
    
    Returns:
        ResponseModel: A model containing the response data for finished tasks.
    """
    ...