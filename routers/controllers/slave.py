from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from middleware.auth import SignRequired
from models.response import ResponseModel

slave_router = APIRouter(
    prefix="/slave",
    tags=["slave"],
)

slave_aria2_router = APIRouter(
    prefix="/aria2",
    tags=["slave_aria2"],
)

@slave_router.get(
    path='/ping',
    summary='测试用路由',
    description='Test route for checking connectivity.',
)
def router_slave_ping() -> ResponseModel:
    """
    Test route for checking connectivity.
    
    Returns:
        ResponseModel: A response model indicating success.
    """
    from pkg.conf.appmeta import BackendVersion
    return ResponseModel(data=BackendVersion)

@slave_router.post(
    path='/post',
    summary='上传',
    description='Upload data to the server.',
    dependencies=[Depends(SignRequired)],
)
def router_slave_post(data: str) -> ResponseModel:
    """
    Upload data to the server.
    
    Args:
        data (str): The data to be uploaded.
    
    Returns:
        ResponseModel: A response model indicating success.
    """
    pass

@slave_router.get(
    path='/get/{speed}/{path}/{name}',
    summary='获取下载',
)
def router_slave_download(speed: int, path: str, name: str) -> ResponseModel:
    """
    Get download information.
    
    Args:
        speed (int): The speed of the download.
        path (str): The path where the file is located.
        name (str): The name of the file to be downloaded.
    
    Returns:
        ResponseModel: A response model containing download information.
    """
    pass

@slave_router.get(
    path='/download/{sign}',
    summary='根据签名下载文件',
    description='Download a file based on its signature.',
    dependencies=[Depends(SignRequired)],
)
def router_slave_download_by_sign(sign: str) -> FileResponse:
    """
    Download a file based on its signature.
    
    Args:
        sign (str): The signature of the file to be downloaded.
    
    Returns:
        FileResponse: A response containing the file to be downloaded.
    """
    pass

@slave_router.get(
    path='/source/{speed}/{path}/{name}',
    summary='获取文件外链',
    description='Get the external link for a file based on its signature.',
    dependencies=[Depends(SignRequired)],
)
def router_slave_source(speed: int, path: str, name: str) -> ResponseModel:
    """
    Get the external link for a file based on its signature.
    
    Args:
        speed (int): The speed of the download.
        path (str): The path where the file is located.
        name (str): The name of the file to be linked.
    
    Returns:
        ResponseModel: A response model containing the external link for the file.
    """
    pass

@slave_router.get(
    path='/source/{sign}',
    summary='根据签名获取文件',
    description='Get a file based on its signature.',
    dependencies=[Depends(SignRequired)],
)
def router_slave_source_by_sign(sign: str) -> FileResponse:
    """
    Get a file based on its signature.
    
    Args:
        sign (str): The signature of the file to be retrieved.
    
    Returns:
        FileResponse: A response containing the file to be retrieved.
    """
    pass

@slave_router.get(
    path='/thumb/{id}',
    summary='获取缩略图',
    description='Get a thumbnail image based on its ID.',
    dependencies=[Depends(SignRequired)],
)
def router_slave_thumb(id: str) -> ResponseModel:
    """
    Get a thumbnail image based on its ID.
    
    Args:
        id (str): The ID of the thumbnail image.
    
    Returns:
        ResponseModel: A response model containing the Base64 encoded thumbnail image.
    """
    pass

@slave_router.delete(
    path='/delete',
    summary='删除文件',
    description='Delete a file from the server.',
    dependencies=[Depends(SignRequired)],
)
def router_slave_delete(path: str) -> ResponseModel:
    """
    Delete a file from the server.
    
    Args:
        path (str): The path of the file to be deleted.
    
    Returns:
        ResponseModel: A response model indicating success or failure of the deletion.
    """
    pass

@slave_aria2_router.post(
    path='/test',
    summary='测试从机连接Aria2服务',
    description='Test the connection to the Aria2 service from the slave.',
    dependencies=[Depends(SignRequired)],
)
def router_slave_aria2_test() -> ResponseModel:
    """
    Test the connection to the Aria2 service from the slave.
    """
    pass

@slave_aria2_router.get(
    path='/get/{gid}',
    summary='获取Aria2任务信息',
    description='Get information about an Aria2 task by its GID.',
    dependencies=[Depends(SignRequired)],
)
def router_slave_aria2_get(gid: str = None) -> ResponseModel:
    """
    Get information about an Aria2 task by its GID.
    
    Args:
        gid (str): The GID of the Aria2 task.
    
    Returns:
        ResponseModel: A response model containing the task information.
    """
    pass

@slave_aria2_router.post(
    path='/add',
    summary='添加Aria2任务',
    description='Add a new Aria2 task.',
    dependencies=[Depends(SignRequired)],
)
def router_slave_aria2_add(gid: str, url: str, options: dict = None) -> ResponseModel:
    """
    Add a new Aria2 task.
    
    Args:
        gid (str): The GID for the new task.
        url (str): The URL of the file to be downloaded.
        options (dict, optional): Additional options for the task.
    
    Returns:
        ResponseModel: A response model indicating success or failure of the task addition.
    """
    pass

@slave_aria2_router.delete(
    path='/remove/{gid}',
    summary='删除Aria2任务',
    description='Remove an Aria2 task by its GID.',
    dependencies=[Depends(SignRequired)],
)
def router_slave_aria2_remove(gid: str) -> ResponseModel:
    """
    Remove an Aria2 task by its GID.
    
    Args:
        gid (str): The GID of the Aria2 task to be removed.
    
    Returns:
        ResponseModel: A response model indicating success or failure of the task removal.
    """
    pass