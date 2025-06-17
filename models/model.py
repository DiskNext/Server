from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, BigInteger, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)

class Download(BaseModel):
    __tablename__ = 'downloads'
    
    status = Column(Integer, nullable=True)
    type = Column(Integer, nullable=True)
    source = Column(Text, nullable=True)
    total_size = Column(BigInteger, nullable=True)
    downloaded_size = Column(BigInteger, nullable=True)
    g_id = Column(Text, nullable=True)
    speed = Column(Integer, nullable=True)
    parent = Column(Text, nullable=True)
    attrs = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    dst = Column(Text, nullable=True)
    user_id = Column(Integer, nullable=True)
    task_id = Column(Integer, nullable=True)
    node_id = Column(Integer, nullable=True)

class File(BaseModel):
    __tablename__ = 'files'
    
    name = Column(String(255), nullable=True)
    source_name = Column(Text, nullable=True)
    user_id = Column(Integer, nullable=True)
    size = Column(BigInteger, nullable=True)
    pic_info = Column(String(255), nullable=True)
    folder_id = Column(Integer, nullable=True)
    policy_id = Column(Integer, nullable=True)
    upload_session_id = Column(String(255), nullable=True, unique=True)
    metadata = Column(Text, nullable=True)

class Folder(BaseModel):
    __tablename__ = 'folders'
    
    name = Column(String(255), nullable=True)
    parent_id = Column(Integer, nullable=True, index=True)
    owner_id = Column(Integer, nullable=True, index=True)
    policy_id = Column(Integer, nullable=True)
    
    __table_args__ = {'uniqueConstraints': [('name', 'parent_id')]}

class Group(BaseModel):
    __tablename__ = 'groups'
    
    name = Column(String(255), nullable=True)
    policies = Column(String(255), nullable=True)
    max_storage = Column(BigInteger, nullable=True)
    share_enabled = Column(Boolean, nullable=True)
    web_dav_enabled = Column(Boolean, nullable=True)
    speed_limit = Column(Integer, nullable=True)
    options = Column(String(255), nullable=True)

class Node(BaseModel):
    __tablename__ = 'nodes'
    
    status = Column(Integer, nullable=True)
    name = Column(String(255), nullable=True)
    type = Column(Integer, nullable=True)
    server = Column(String(255), nullable=True)
    slave_key = Column(Text, nullable=True)
    master_key = Column(Text, nullable=True)
    aria2_enabled = Column(Boolean, nullable=True)
    aria2_options = Column(Text, nullable=True)
    rank = Column(Integer, nullable=True)

class Order(BaseModel):
    __tablename__ = 'orders'
    
    user_id = Column(Integer, nullable=True)
    order_no = Column(String(255), nullable=True, index=True)
    type = Column(Integer, nullable=True)
    method = Column(String(255), nullable=True)
    product_id = Column(BigInteger, nullable=True)
    num = Column(Integer, nullable=True)
    name = Column(String(255), nullable=True)
    price = Column(Integer, nullable=True)
    status = Column(Integer, nullable=True)

class Policy(BaseModel):
    __tablename__ = 'policies'
    
    name = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    server = Column(String(255), nullable=True)
    bucket_name = Column(String(255), nullable=True)
    is_private = Column(Boolean, nullable=True)
    base_url = Column(String(255), nullable=True)
    access_key = Column(Text, nullable=True)
    secret_key = Column(Text, nullable=True)
    max_size = Column(BigInteger, nullable=True)
    auto_rename = Column(Boolean, nullable=True)
    dir_name_rule = Column(String(255), nullable=True)
    file_name_rule = Column(String(255), nullable=True)
    is_origin_link_enable = Column(Boolean, nullable=True)
    options = Column(Text, nullable=True)

class Redeem(BaseModel):
    __tablename__ = 'redeems'
    
    type = Column(Integer, nullable=True)
    product_id = Column(BigInteger, nullable=True)
    num = Column(Integer, nullable=True)
    code = Column(Text, nullable=True)
    used = Column(Boolean, nullable=True)

class Report(BaseModel):
    __tablename__ = 'reports'
    
    share_id = Column(Integer, nullable=True, index=True)
    reason = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)

class Setting(BaseModel):
    __tablename__ = 'settings'
    
    type = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False, unique=True, index=True)
    value = Column(Text, nullable=True)

class Share(BaseModel):
    __tablename__ = 'shares'
    
    password = Column(String(255), nullable=True)
    is_dir = Column(Boolean, nullable=True)
    user_id = Column(Integer, nullable=True)
    source_id = Column(Integer, nullable=True)
    views = Column(Integer, nullable=True)
    downloads = Column(Integer, nullable=True)
    remain_downloads = Column(Integer, nullable=True)
    expires = Column(DateTime, nullable=True)
    preview_enabled = Column(Boolean, nullable=True)
    source_name = Column(String(255), nullable=True, index=True)
    score = Column(Integer, nullable=True)

class SourceLink(BaseModel):
    __tablename__ = 'source_links'
    
    file_id = Column(Integer, nullable=True)
    name = Column(String(255), nullable=True)
    downloads = Column(Integer, nullable=True)

class StoragePack(BaseModel):
    __tablename__ = 'storage_packs'
    
    name = Column(String(255), nullable=True)
    user_id = Column(Integer, nullable=True)
    active_time = Column(DateTime, nullable=True)
    expired_time = Column(DateTime, nullable=True, index=True)
    size = Column(BigInteger, nullable=True)

class Tag(BaseModel):
    __tablename__ = 'tags'
    
    name = Column(String(255), nullable=True)
    icon = Column(String(255), nullable=True)
    color = Column(String(255), nullable=True)
    type = Column(Integer, nullable=True)
    expression = Column(Text, nullable=True)
    user_id = Column(Integer, nullable=True)

class Task(BaseModel):
    __tablename__ = 'tasks'
    
    status = Column(Integer, nullable=True)
    type = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    progress = Column(Integer, nullable=True)
    error = Column(Text, nullable=True)
    props = Column(Text, nullable=True)

class User(BaseModel):
    __tablename__ = 'users'
    
    email = Column(String(100), nullable=True, unique=True)
    nick = Column(String(50), nullable=True)
    password = Column(String(255), nullable=True)
    status = Column(Integer, nullable=True)
    group_id = Column(Integer, nullable=True)
    storage = Column(BigInteger, nullable=True)
    two_factor = Column(String(255), nullable=True)
    avatar = Column(String(255), nullable=True)
    options = Column(Text, nullable=True)
    authn = Column(Text, nullable=True)
    open_id = Column(String(255), nullable=True)
    score = Column(Integer, nullable=True)
    previous_group_id = Column(Integer, nullable=True)
    group_expires = Column(DateTime, nullable=True)
    notify_date = Column(DateTime, nullable=True)
    phone = Column(String(255), nullable=True)

class WebDAV(BaseModel):
    __tablename__ = 'webdavs'
    
    name = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)
    user_id = Column(Integer, nullable=True)
    root = Column(Text, nullable=True)
    readonly = Column(Boolean, nullable=True)
    use_proxy = Column(Boolean, nullable=True)
    
    __table_args__ = {'uniqueConstraints': [('password', 'user_id')]}
