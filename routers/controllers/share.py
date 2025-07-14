from fastapi import APIRouter, Depends
from middleware.auth import SignRequired
from models.response import ResponseModel

share_router = APIRouter(
    prefix='/share',
    tags=["share"],
)

@share_router.get(
    path='/{info}/{id}',
    summary='获取分享',
    description='Get shared content by info type and ID.',
)
def router_share_get(info: str, id: str) -> ResponseModel:
    """
    Get shared content by info type and ID.
    
    Args:
        info (str): The type of information being shared.
        id (str): The ID of the shared content.
    
    Returns:
        dict: A dictionary containing shared content information.
    """
    pass

@share_router.put(
    path='/download/{id}',
    summary='创建文件下载会话',
    description='Create a file download session by ID.',
)
def router_share_download(id: str) -> ResponseModel:
    """
    Create a file download session by ID.
    
    Args:
        id (str): The ID of the file to be downloaded.
    
    Returns:
        dict: A dictionary containing download session information.
    """
    pass

@share_router.get(
    path='preview/{id}',
    summary='预览分享文件',
    description='Preview shared file by ID.',
)
def router_share_preview(id: str) -> ResponseModel:
    """
    Preview shared file by ID.
    
    Args:
        id (str): The ID of the file to be previewed.
    
    Returns:
        dict: A dictionary containing preview information.
    """
    pass

@share_router.get(
    path='/doc/{id}',
    summary='取得Office文档预览地址',
    description='Get Office document preview URL by ID.',
)
def router_share_doc(id: str) -> ResponseModel:
    """
    Get Office document preview URL by ID.
    
    Args:
        id (str): The ID of the Office document.
    
    Returns:
        dict: A dictionary containing the document preview URL.
    """
    pass

@share_router.get(
    path='/content/{id}',
    summary='获取文本文件内容',
    description='Get text file content by ID.',
)
def router_share_content(id: str) -> ResponseModel:
    """
    Get text file content by ID.
    
    Args:
        id (str): The ID of the text file.
    
    Returns:
        str: The content of the text file.
    """
    pass

@share_router.get(
    path='/list/{id}/{path:path}',
    summary='获取目录列文件',
    description='Get directory listing by ID and path.',
)
def router_share_list(id: str, path: str = '') -> ResponseModel:
    """
    Get directory listing by ID and path.
    
    Args:
        id (str): The ID of the directory.
        path (str): The path within the directory.
    
    Returns:
        dict: A dictionary containing directory listing information.
    """
    pass

@share_router.get(
    path='/search/{id}/{type}/{keywords}',
    summary='分享目录搜索',
    description='Search within a shared directory by ID, type, and keywords.',
)
def router_share_search(id: str, type: str, keywords: str) -> ResponseModel:
    """
    Search within a shared directory by ID, type, and keywords.
    
    Args:
        id (str): The ID of the shared directory.
        type (str): The type of search (e.g., file, folder).
        keywords (str): The keywords to search for.
    
    Returns:
        dict: A dictionary containing search results.
    """
    pass

@share_router.post(
    path='/archive/{id}',
    summary='归档打包下载',
    description='Archive and download shared content by ID.',
)
def router_share_archive(id: str) -> ResponseModel:
    """
    Archive and download shared content by ID.
    
    Args:
        id (str): The ID of the content to be archived.
    
    Returns:
        dict: A dictionary containing archive download information.
    """
    pass

@share_router.get(
    path='/readme/{id}',
    summary='获取README文本文件内容',
    description='Get README text file content by ID.',
)
def router_share_readme(id: str) -> ResponseModel:
    """
    Get README text file content by ID.
    
    Args:
        id (str): The ID of the README file.
    
    Returns:
        str: The content of the README file.
    """
    pass

@share_router.get(
    path='/thumb/{id}/{file}',
    summary='获取缩略图',
    description='Get thumbnail image by ID and file name.',
)
def router_share_thumb(id: str, file: str) -> ResponseModel:
    """
    Get thumbnail image by ID and file name.
    
    Args:
        id (str): The ID of the shared content.
        file (str): The name of the file for which to get the thumbnail.
    
    Returns:
        str: A Base64 encoded string of the thumbnail image.
    """
    pass

@share_router.post(
    path='/report/{id}',
    summary='举报分享',
    description='Report shared content by ID.',
)
def router_share_report(id: str) -> ResponseModel:
    """
    Report shared content by ID.
    
    Args:
        id (str): The ID of the shared content to report.
    
    Returns:
        dict: A dictionary containing report submission information.
    """
    pass

@share_router.get(
    path='/search',
    summary='搜索公共分享',
    description='Search public shares by keywords and type.',
)
def router_share_search_public(keywords: str, type: str = 'all') -> ResponseModel:
    """
    Search public shares by keywords and type.
    
    Args:
        keywords (str): The keywords to search for.
        type (str): The type of search (e.g., all, file, folder).
    
    Returns:
        dict: A dictionary containing search results for public shares.
    """
    pass

#####################
# 需要登录的接口
#####################

@share_router.post(
    path='/',
    summary='创建新分享',
    description='Create a new share endpoint.',
    dependencies=[Depends(SignRequired)]
)
def router_share_create() -> ResponseModel:
    """
    Create a new share endpoint.
    
    Returns:
        ResponseModel: A model containing the response data for the new share creation.
    """
    pass

@share_router.get(
    path='/',
    summary='列出我的分享',
    description='Get a list of shares.',
    dependencies=[Depends(SignRequired)]
)
def router_share_list() -> ResponseModel:
    """
    Get a list of shares.
    
    Returns:
        ResponseModel: A model containing the response data for the list of shares.
    """
    pass

@share_router.post(
    path='/save/{id}',
    summary='转存他人分享',
    description='Save another user\'s share by ID.',
    dependencies=[Depends(SignRequired)]
)
def router_share_save(id: str) -> ResponseModel:
    """
    Save another user's share by ID.
    
    Args:
        id (str): The ID of the share to be saved.
    
    Returns:
        ResponseModel: A model containing the response data for the saved share.
    """
    pass

@share_router.patch(
    path='/{id}',
    summary='更新分享信息',
    description='Update share information by ID.',
    dependencies=[Depends(SignRequired)]
)
def router_share_update(id: str) -> ResponseModel:
    """
    Update share information by ID.
    
    Args:
        id (str): The ID of the share to be updated.
    
    Returns:
        ResponseModel: A model containing the response data for the updated share.
    """
    pass

@share_router.delete(
    path='/{id}',
    summary='删除分享',
    description='Delete a share by ID.',
    dependencies=[Depends(SignRequired)]
)
def router_share_delete(id: str) -> ResponseModel:
    """
    Delete a share by ID.
    
    Args:
        id (str): The ID of the share to be deleted.
    
    Returns:
        ResponseModel: A model containing the response data for the deleted share.
    """
    pass