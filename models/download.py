from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, UniqueConstraint
from .base import SQLModelBase, UUIDTableBase

if TYPE_CHECKING:
    from .user import User
    from .task import Task
    from .node import Node

class DownloadBase(SQLModelBase):
    pass

class Download(DownloadBase, UUIDTableBase, table=True):
    __tablename__ = 'downloads'
    __table_args__ = (
        UniqueConstraint("node_id", "g_id", name="uq_download_node_gid"),
    )

    status: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="下载状态: 0=进行中, 1=完成, 2=错误")
    type: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="任务类型")
    source: str = Field(description="来源URL或标识")
    total_size: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="总大小（字节）")
    downloaded_size: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="已下载大小（字节）")
    g_id: Optional[str] = Field(default=None, index=True, description="Aria2 GID")
    speed: int = Field(default=0, sa_column_kwargs={"server_default": "0"}, description="下载速度 (bytes/s)")
    parent: Optional[str] = Field(default=None, description="父任务标识")
    attrs: Optional[str] = Field(default=None, description="额外属性 (JSON格式)")
    # attrs 示例: {"gid":"65c5faf38374cc63","status":"removed","totalLength":"0","completedLength":"0","uploadLength":"0","bitfield":"","downloadSpeed":"0","uploadSpeed":"0","infoHash":"ca159db2b1e78f6e95fd972be72251f967f639d4","numSeeders":"0","seeder":"","pieceLength":"16384","numPieces":"0","connections":"0","errorCode":"31","errorMessage":"","followedBy":null,"belongsTo":"","dir":"/data/ccaaDown/aria2/7a208304-9126-46d2-ba47-a6959f236a07","files":[{"index":"1","path":"[METADATA]zh-cn_windows_11_consumer_editions_version_21h2_updated_aug_2022_x64_dvd_a29983d5.iso","length":"0","completedLength":"0","selected":"true","uris":[]}],"bittorrent":{"announceList":[["udp://tracker.opentrackr.org:1337/announce"],["udp://9.rarbg.com:2810/announce"],["udp://tracker.openbittorrent.com:6969/announce"],["https://opentracker.i2p.rocks:443/announce"],["http://tracker.openbittorrent.com:80/announce"],["udp://open.stealth.si:80/announce"],["udp://tracker.torrent.eu.org:451/announce"],["udp://exodus.desync.com:6969/announce"],["udp://tracker.tiny-vps.com:6969/announce"],["udp://tracker.pomf.se:80/announce"],["udp://tracker.moeking.me:6969/announce"],["udp://tracker.dler.org:6969/announce"],["udp://open.demonii.com:1337/announce"],["udp://explodie.org:6969/announce"],["udp://chouchou.top:8080/announce"],["udp://bt.oiyo.tk:6969/announce"],["https://tracker.nanoha.org:443/announce"],["https://tracker.lilithraws.org:443/announce"],["http://tracker3.ctix.cn:8080/announce"],["http://tracker.nucozer-tracker.ml:2710/announce"]],"comment":"","creationDate":0,"mode":"","info":{"name":""}}}
    error: Optional[str] = Field(default=None, description="错误信息")
    dst: str = Field(description="目标存储路径")
    
    # 外键
    user_id: int = Field(foreign_key="users.id", index=True, description="所属用户ID")
    task_id: Optional[int] = Field(default=None, foreign_key="tasks.id", index=True, description="关联的任务ID")
    node_id: int = Field(foreign_key="nodes.id", index=True, description="执行下载的节点ID")
    
    # 关系
    user: "User" = Relationship(back_populates="downloads")
    task: Optional["Task"] = Relationship(back_populates="downloads")
    node: "Node" = Relationship(back_populates="downloads")
    
    