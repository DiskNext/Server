# my_project/models/user.py

from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, Relationship, Column, func, DateTime
from .base import BaseModel
from .database import get_session
from sqlmodel import select

# TYPE_CHECKING 用于解决循环导入问题，只在类型检查时导入
if TYPE_CHECKING:
    from .group import Group
    from .download import Download
    from .file import File
    from .folder import Folder
    from .order import Order
    from .share import Share
    from .storage_pack import StoragePack
    from .tag import Tag
    from .task import Task
    from .webdav import WebDAV

class User(BaseModel, table=True):
    __tablename__ = 'users'

    email: str = Field(max_length=100, unique=True, index=True, description="用户邮箱，唯一")
    nick: Optional[str] = Field(default=None, max_length=50, description="用户昵称")
    password: str = Field(max_length=255, description="用户密码（加密后）")
    status: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="用户状态: 0=正常, 1=未激活, 2=封禁")
    storage: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="已用存储空间（字节）")
    two_factor: Optional[str] = Field(default=None, max_length=255, description="两步验证密钥")
    avatar: Optional[str] = Field(default=None, max_length=255, description="头像地址")
    options: Optional[str] = Field(default=None, description="用户个人设置 (JSON格式)")
    authn: Optional[str] = Field(default=None, description="WebAuthn 凭证")
    open_id: Optional[str] = Field(default=None, max_length=255, unique=True, index=True, description="第三方登录OpenID")
    score: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="用户积分")
    group_expires: Optional[datetime] = Field(default=None, description="当前用户组过期时间")
    phone: Optional[str] = Field(default=None, max_length=255, unique=True, index=True, description="手机号")

    # 外键
    group_id: int = Field(foreign_key="groups.id", index=True, description="所属用户组ID")
    previous_group_id: Optional[int] = Field(default=None, foreign_key="groups.id", description="之前的用户组ID（用于过期后恢复）")
    
    # 关系
    group: "Group" = Relationship(
        back_populates="users",
        sa_relationship_kwargs={"foreign_keys": "User.group_id"}
    )
    previous_group: Optional["Group"] = Relationship(
        back_populates="previous_users",
        sa_relationship_kwargs={"foreign_keys": "User.previous_group_id"}
    )
    
    downloads: list["Download"] = Relationship(back_populates="user")
    files: list["File"] = Relationship(back_populates="user")
    folders: list["Folder"] = Relationship(back_populates="owner")
    orders: list["Order"] = Relationship(back_populates="user")
    shares: list["Share"] = Relationship(back_populates="user")
    storage_packs: list["StoragePack"] = Relationship(back_populates="user")
    tags: list["Tag"] = Relationship(back_populates="user")
    tasks: list["Task"] = Relationship(back_populates="user")
    webdavs: list["WebDAV"] = Relationship(back_populates="user")
    
    @staticmethod
    async def create(
        user: Optional["User"] = None,
        email: str = None,
        nick: Optional[str] = None,
        password: str = None,
        status: int = 0,
        two_factor: Optional[str] = None,
        avatar: Optional[str] = None,
        options: Optional[str] = None,
        authn: Optional[str] = None,
        open_id: Optional[str] = None,
        score: int = 0,
        phone: Optional[str] = None
    ):
        """
        向数据库内添加用户。
        
        :param user: User 实例
        :type user: User
        """
        if not user:
            user = User(
                email=email,
                nick=nick,
                password=password,
                status=status,
                two_factor=two_factor,
                avatar=avatar,
                options=options,
                authn=authn,
                open_id=open_id,
                score=score,
                phone=phone
            )
        
        from .database import get_session
        
        async for session in get_session():
            try:
                session.add(user)
                await session.commit()
                await session.refresh(user)
            except Exception as e:
                await session.rollback()
                raise e
        return user
    
    @staticmethod
    async def get(
        id: int = None,
        email: str = None
    ) -> Optional["User"]:
        """
        获取用户信息。
        
        :param id: 用户ID，默认为 None
        :type id: int
        :param email: 用户邮箱，默认为 None
        :type email: str
        :return: 用户对象或 None
        :rtype: Optional[User]
        """
        session = get_session()
        
        if id is None and email is None:
            return None
        
        async for session in get_session():
            query = select(User)
            if id is not None:
                query = query.where(User.id == id)
            if email is not None:
                query = query.where(User.email == email)
            
            result = await session.exec(query)
            user = result.one_or_none()
        
        return user
    
    @staticmethod
    async def update(
        id: int,
        email: Optional[str] = None,
        nick: Optional[str] = None,
        password: Optional[str] = None,
        status: Optional[int] = None,
        storage: Optional[int] = None,
        two_factor: Optional[str] = None,
        avatar: Optional[str] = None,
        options: Optional[str] = None,
        authn: Optional[str] = None,
        open_id: Optional[str] = None,
        score: Optional[int] = None,
        group_id: Optional[int] = None
    ) -> "User":
        """
        更新用户信息。
        
        :return: 更新后的用户对象
        :rtype: User
        """
        async for session in get_session():
            try:
                statement = select(User).where(User.id == id)
                result = await session.exec(statement)
                user = result.first()
                
                if user is None:
                    raise ValueError(f"User with id {id} not found.")
                
                if email is not None:
                    user.email = email
                if nick is not None:
                    user.nick = nick
                if password is not None:
                    user.password = password
                if status is not None:
                    user.status = status
                if storage is not None:
                    user.storage = storage
                if two_factor is not None:
                    user.two_factor = two_factor
                if avatar is not None:
                    user.avatar = avatar
                if options is not None:
                    user.options = options
                if authn is not None:
                    user.authn = authn
                if open_id is not None:
                    user.open_id = open_id
                if score is not None:
                    user.score = score
                if group_id is not None:
                    user.group_id = group_id

                await session.commit()
                await session.refresh(user)
                return user
            except Exception as e:
                await session.rollback()
                raise e
    
    @staticmethod
    async def delete(
        id: int
    ) -> None:
        """
        删除用户。
        
        :param id: 用户ID
        :type id: int
        """
        if id == 1:
            raise ValueError("Cannot delete the default admin user with id 1.")
        
        async for session in get_session():
            try:
                statement = select(User).where(User.id == id)
                result = await session.exec(statement)
                user = result.one_or_none()
                
                if user is None:
                    raise ValueError(f"User with id {id} not found.")
                
                await session.delete(user)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e