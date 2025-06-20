from sqlalchemy import (
    Column, Integer, String, Text, BigInteger, Boolean, DateTime,
    ForeignKey, func, text, UniqueConstraint
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, comment="主键ID")

    created_at = Column(
        DateTime, 
        server_default=func.now(), 
        comment="创建时间"
    )
    
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=func.now(),
        comment="更新时间"
    )
    
    deleted_at = Column(DateTime, nullable=True, comment="软删除时间")

class Download(BaseModel):
    __tablename__ = 'downloads'
    
    status = Column(Integer, nullable=False, server_default='0', comment="下载状态: 0=进行中, 1=完成, 2=错误")
    type = Column(Integer, nullable=False, server_default='0', comment="任务类型")
    source = Column(Text, nullable=False, comment="来源URL或标识")
    total_size = Column(BigInteger, nullable=False, server_default='0', comment="总大小（字节）")
    downloaded_size = Column(BigInteger, nullable=False, server_default='0', comment="已下载大小（字节）")
    g_id = Column(Text, index=True, comment="Aria2 GID") # GID经常用于查询，建议索引
    speed = Column(Integer, nullable=False, server_default='0', comment="下载速度 (bytes/s)")
    parent = Column(Text, comment="父任务标识")
    attrs = Column(Text, comment="额外属性 (JSON格式)")
    error = Column(Text, comment="错误信息")
    dst = Column(Text, nullable=False, comment="目标存储路径")
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True, comment="所属用户ID")
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=True, index=True, comment="关联的任务ID")
    node_id = Column(Integer, ForeignKey('nodes.id'), nullable=False, index=True, comment="执行下载的节点ID")

class File(BaseModel):
    __tablename__ = 'files'
    
    name = Column(String(255), nullable=False, comment="文件名")
    source_name = Column(Text, comment="源文件名")
    size = Column(BigInteger, nullable=False, server_default='0', comment="文件大小（字节）")
    pic_info = Column(String(255), comment="图片信息（如尺寸）")
    upload_session_id = Column(String(255), unique=True, index=True, comment="分块上传会话ID")
    metadata = Column(Text, comment="文件元数据 (JSON格式)")
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True, comment="所属用户ID")
    folder_id = Column(Integer, ForeignKey('folders.id'), nullable=False, index=True, comment="所在目录ID")
    policy_id = Column(Integer, ForeignKey('policies.id'), nullable=False, index=True, comment="所属存储策略ID")

class Folder(BaseModel):
    __tablename__ = 'folders'
    
    name = Column(String(255), nullable=False, comment="目录名")
    
    parent_id = Column(Integer, ForeignKey('folders.id'), nullable=True, index=True, comment="父目录ID")
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True, comment="所有者用户ID")
    policy_id = Column(Integer, ForeignKey('policies.id'), nullable=False, index=True, comment="所属存储策略ID")
    
    __table_args__ = (
        UniqueConstraint('name', 'parent_id', name='uq_folder_name_parent'),
    )

class Group(BaseModel):
    __tablename__ = 'groups'
    
    name = Column(String(255), nullable=False, unique=True, comment="用户组名")
    policies = Column(String(255), comment="允许的策略ID列表，逗号分隔")
    max_storage = Column(BigInteger, nullable=False, server_default='0', comment="最大存储空间（字节）")
    
    share_enabled = Column(Boolean, nullable=False, server_default=text('false'), comment="是否允许创建分享")
    web_dav_enabled = Column(Boolean, nullable=False, server_default=text('false'), comment="是否允许使用WebDAV")
    
    speed_limit = Column(Integer, nullable=False, server_default='0', comment="速度限制 (KB/s), 0为不限制")
    options = Column(Text, comment="其他选项 (JSON格式)")

class Node(BaseModel):
    __tablename__ = 'nodes'
    
    status = Column(Integer, nullable=False, server_default='0', comment="节点状态: 0=正常, 1=离线")
    name = Column(String(255), nullable=False, unique=True, comment="节点名称")
    type = Column(Integer, nullable=False, server_default='0', comment="节点类型")
    server = Column(String(255), nullable=False, comment="节点地址（IP或域名）")
    slave_key = Column(Text, comment="从机通讯密钥")
    master_key = Column(Text, comment="主机通讯密钥")
    aria2_enabled = Column(Boolean, nullable=False, server_default=text('false'), comment="是否启用Aria2")
    aria2_options = Column(Text, comment="Aria2配置 (JSON格式)")
    rank = Column(Integer, nullable=False, server_default='0', comment="节点排序权重")

class Order(BaseModel):
    __tablename__ = 'orders'
    
    order_no = Column(String(255), nullable=False, unique=True, index=True, comment="订单号，唯一")
    type = Column(Integer, nullable=False, comment="订单类型")
    method = Column(String(255), comment="支付方式")
    product_id = Column(BigInteger, comment="商品ID")
    num = Column(Integer, nullable=False, server_default='1', comment="购买数量")
    name = Column(String(255), nullable=False, comment="商品名称")
    price = Column(Integer, nullable=False, server_default='0', comment="订单价格（分）")
    status = Column(Integer, nullable=False, server_default='0', comment="订单状态: 0=待支付, 1=已完成, 2=已取消")
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True, comment="所属用户ID")

class Policy(BaseModel):
    __tablename__ = 'policies'
    
    name = Column(String(255), nullable=False, unique=True, comment="策略名称")
    type = Column(String(255), nullable=False, comment="存储类型 (e.g. 'local', 's3')")
    server = Column(String(255), comment="服务器地址（本地策略为路径）")
    bucket_name = Column(String(255), comment="存储桶名称")
    is_private = Column(Boolean, nullable=False, server_default=text('true'), comment="是否为私有空间")
    base_url = Column(String(255), comment="访问文件的基础URL")
    access_key = Column(Text, comment="Access Key")
    secret_key = Column(Text, comment="Secret Key")
    max_size = Column(BigInteger, nullable=False, server_default='0', comment="允许上传的最大文件尺寸（字节）")
    auto_rename = Column(Boolean, nullable=False, server_default=text('false'), comment="是否自动重命名")
    dir_name_rule = Column(String(255), comment="目录命名规则")
    file_name_rule = Column(String(255), comment="文件命名规则")
    is_origin_link_enable = Column(Boolean, nullable=False, server_default=text('false'), comment="是否开启源链接访问")
    options = Column(Text, comment="其他选项 (JSON格式)")

class Setting(BaseModel):
    __tablename__ = 'settings'
    
    # 优化点: type和name的组合应该是唯一的
    type = Column(String(255), nullable=False, comment="设置类型/分组")
    name = Column(String(255), nullable=False, comment="设置项名称")
    value = Column(Text, comment="设置值")
    
    __table_args__ = (
        UniqueConstraint('type', 'name', name='uq_setting_type_name'),
    )

class Share(BaseModel):
    __tablename__ = 'shares'
    
    password = Column(String(255), comment="分享密码（加密后）")
    is_dir = Column(Boolean, nullable=False, server_default=text('false'), comment="是否为目录分享")
    source_id = Column(Integer, nullable=False, comment="源文件或目录的ID")
    views = Column(Integer, nullable=False, server_default='0', comment="浏览次数")
    downloads = Column(Integer, nullable=False, server_default='0', comment="下载次数")
    remain_downloads = Column(Integer, comment="剩余下载次数 (NULL为不限制)")
    expires = Column(DateTime, comment="过期时间 (NULL为永不过期)")
    preview_enabled = Column(Boolean, nullable=False, server_default=text('true'), comment="是否允许预览")
    source_name = Column(String(255), index=True, comment="源名称（冗余字段，便于展示）")
    score = Column(Integer, nullable=False, server_default='0', comment="分享评分/权重")
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True, comment="创建分享的用户ID")

class Task(BaseModel):
    __tablename__ = 'tasks'
    
    status = Column(Integer, nullable=False, server_default='0', comment="任务状态: 0=排队中, 1=处理中, 2=完成, 3=错误")
    type = Column(Integer, nullable=False, comment="任务类型")
    progress = Column(Integer, nullable=False, server_default='0', comment="任务进度 (0-100)")
    error = Column(Text, comment="错误信息")
    props = Column(Text, comment="任务属性 (JSON格式)")
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True, comment="所属用户ID")

class User(BaseModel):
    __tablename__ = 'users'
    
    email = Column(String(100), nullable=False, unique=True, index=True, comment="用户邮箱，唯一")
    nick = Column(String(50), comment="用户昵称")
    password = Column(String(255), nullable=False, comment="用户密码（加密后）")
    status = Column(Integer, nullable=False, server_default='0', comment="用户状态: 0=正常, 1=未激活, 2=封禁")
    storage = Column(BigInteger, nullable=False, server_default='0', comment="已用存储空间（字节）")
    two_factor = Column(String(255), comment="两步验证密钥")
    avatar = Column(String(255), comment="头像地址")
    options = Column(Text, comment="用户个人设置 (JSON格式)")
    authn = Column(Text, comment="WebAuthn 凭证")
    open_id = Column(String(255), unique=True, index=True, nullable=True, comment="第三方登录OpenID")
    score = Column(Integer, nullable=False, server_default='0', comment="用户积分")
    group_expires = Column(DateTime, comment="当前用户组过期时间")
    phone = Column(String(255), unique=True, nullable=True, index=True, comment="手机号")
    
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False, index=True, comment="所属用户组ID")
    previous_group_id = Column(Integer, ForeignKey('groups.id'), nullable=True, comment="之前的用户组ID（用于过期后恢复）")

class Redeem(BaseModel):
    __tablename__ = 'redeems'
    
    type = Column(Integer, nullable=False, comment="兑换码类型")
    product_id = Column(BigInteger, comment="关联的商品/权益ID")
    num = Column(Integer, nullable=False, server_default='1', comment="可兑换数量/时长等")
    code = Column(Text, nullable=False, unique=True, index=True, comment="兑换码，唯一")
    used = Column(Boolean, nullable=False, server_default=text('false'), comment="是否已使用")

class Report(BaseModel):
    __tablename__ = 'reports'
    
    share_id = Column(Integer, ForeignKey('shares.id'), index=True, nullable=False, comment="被举报的分享ID")
    reason = Column(Integer, nullable=False, comment="举报原因代码")
    description = Column(String(255), comment="补充描述")

class SourceLink(BaseModel):
    __tablename__ = 'source_links'
    
    file_id = Column(Integer, ForeignKey('files.id'), nullable=False, index=True, comment="关联的文件ID")
    name = Column(String(255), nullable=False, comment="链接名称")
    downloads = Column(Integer, nullable=False, server_default='0', comment="通过此链接的下载次数")

class StoragePack(BaseModel):
    __tablename__ = 'storage_packs'
    
    name = Column(String(255), nullable=False, comment="容量包名称")
    active_time = Column(DateTime, comment="激活时间")
    expired_time = Column(DateTime, index=True, comment="过期时间")
    size = Column(BigInteger, nullable=False, comment="容量包大小（字节）")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True, comment="所属用户ID")

class Tag(BaseModel):
    __tablename__ = 'tags'
    
    name = Column(String(255), nullable=False, comment="标签名称")
    icon = Column(String(255), comment="标签图标")
    color = Column(String(255), comment="标签颜色")
    type = Column(Integer, nullable=False, server_default='0', comment="标签类型: 0=手动, 1=自动")
    expression = Column(Text, comment="自动标签的匹配表达式")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True, comment="所属用户ID")
    
    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='uq_tag_name_user'),
    )

class WebDAV(BaseModel):
    __tablename__ = 'webdavs'
    
    name = Column(String(255), nullable=False, comment="WebDAV账户名")
    password = Column(String(255), nullable=False, comment="WebDAV密码（加密后）")
    root = Column(Text, nullable=False, server_default="'/'", comment="根目录路径")
    readonly = Column(Boolean, nullable=False, server_default=text('false'), comment="是否只读")
    use_proxy = Column(Boolean, nullable=False, server_default=text('false'), comment="是否使用代理下载")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True, comment="所属用户ID")
    
    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='uq_webdav_name_user'),
    )