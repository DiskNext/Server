# DiskNext Server 开发规范

## 设计哲学

本项目遵循以下核心设计原则，所有代码实现都应符合这些哲学思想：

### 1. 严格的类型安全与显式优于隐式

- 拒绝泛型（dict/list），必须具体类型（dict[str, str]）
- 拒绝 Any 类型，除非真的无法确定（需要 TODO 标记）
- Python 3.10+ 语法强制（int | None 而非 Optional[int]）
- 所有参数、返回值、变量都必须有类型注解
- **引用任何属性前必须先查看类实现确认存在**

**原因**：编译时发现错误比运行时发现好，显式类型让 IDE 和人都能理解代码

### 2. 充血模型与运行时状态管理

- **充血模型**：SQLModel实例同时包含数据库字段和业务方法（如Character.handle_message()）
- **运行时状态**：使用 `model_post_init()`初始化运行时属性（以 `_`开头），不存储到数据库
- **ClassVar管理跨实例状态**：如MQTTManager._client、MQTTManager._message_task，用于全局单例或共享状态管理
- **严禁动态添加属性**：所有实例属性必须在 `model_post_init()`或类定义中声明，避免SQLAlchemy冲突
- **会话参数化**：运行时方法接收 `session: AsyncSession`参数，不存储session引用

**原因**：充血模型让业务逻辑内聚，所有相关行为都在实体类中。运行时状态通过 `model_post_init()`明确声明，保持类型安全

### 3. 单一真相来源（Single Source of Truth）

- 代码规范只有本文档（AGENTS.md），删除所有其他会造成混淆的规范文档
- SQLModelBase 定义了 model_config，子类不要重复定义
- ServerConfig 直接存属性（port），而非嵌套结构（server.port）
- 配置从数据库读取，而非 YAML 文件

**原因**：多个数据源会导致不一致，维护地狱。一个权威来源，其他地方引用它

### 4. 异步优先，IO绝不阻塞

- 所有 IO 操作必须是 async/await
- 禁止创建新的事件循环（使用 FastAPI 管理的）
- 同步库必须用 to_thread 或 Celery Worker 隔离
- 数据库、HTTP、文件操作都是异步（AsyncSession, aiohttp, aiofiles）

**原因**：现代 Python 服务器必须能处理高并发，阻塞 IO 是性能杀手

### 5. 组合优于继承，聚合优于散布

- **使用组合而非继承**：Character组合LLM/TTS/RVA，而非继承它们
- **Mixin模式用于横切关注点**：如AioHttpClientSessionMixin添加HTTP客户端能力
- **联表继承仅在数据库多态时使用**：OpenAICompatibleLLM → DouBaoLLM（数据库层面的多态）
- **相关逻辑聚合在实体类中**：避免分散到多个辅助类，保持业务逻辑内聚

**原因**：继承是强耦合，组合给你灵活性。充血模型让相关行为聚合在一起，易于理解和维护

### 6. 目录结构即 API 结构

- URL 路径 /api/v1/ota 必须对应 root_endpoint/api/v1/ota/__init__.py
- 禁止独立 .py 文件，只允许 __init__.py 和子目录
- 每个目录的 __init__.py 负责定义该层级的路由

**原因**：代码组织和 URL 结构一致，降低认知负担。看 URL 就知道文件在哪

### 7. 错误快速失败，而非隐藏

- 禁止返回 None 来表示错误（会隐藏问题）
- 必须抛出异常，让 FastAPI 捕获并统一返回 500
- 端点不要自己处理异常（除非有特殊逻辑）

**原因**：隐藏的错误比显式的崩溃更可怕。让系统在问题发生时立即暴露

### 8. 模块内聚，跨模块松耦合

- 一个模块的文件合并（character.py 合并了 5 个文件）
- 通过 __init__.py 明确导出 API，隐藏内部实现
- 依赖注入而非全局变量（SessionDep, ServerConfigDep）

**原因**：相关代码应该在一起（减少跳转），但模块间通过接口通信（降低耦合）

### 9. 约定优于配置

- SQLModelBase 自动配置 use_attribute_docstrings
- TableBase 自动设置 table=True
- 字段用 docstring 描述，而非 Field(description=...)

**原因**：95% 的情况都用默认配置，特殊情况再覆盖。减少样板代码

### 10. 清晰的所有权和生命周期

- **传输层独立管理**（MQTT连接、UDP套接字由transport模块管理，HTTP端点由root_endpoint管理）
- **ClientDevice 拥有业务逻辑状态**（输入输出队列、Character运行时实例）
- **Character 在 model_post_init 中初始化运行时属性**（会话历史、内存引用、消息队列）
- **ClassVar 管理全局单例和共享状态**（如 MQTTManager._client 存储全局MQTT连接实例、VerificationCode._verification_codes 存储TTL缓存）
- **使用 `@asynccontextmanager` 管理资源生命周期**（如 Character.init()、ClientDevice.init()）
- **断开连接时明确清理所有相关资源**（取消任务、关闭连接、保存状态）

**原因**：谁创建谁负责销毁。资源泄漏是难以调试的问题，必须有清晰的生命周期管理。传输层与业务层解耦，降低系统复杂度

### 11. 文档即代码

- Docstring 不是可选的，复杂逻辑必须写
- 类型注解本身就是文档
- 字段描述用 docstring（自动生成 API 文档）

**原因**：好的代码自己会说话，但复杂的逻辑需要解释。文档和代码在一起，不会过时

### 12. 渐进式重构，保留历史参考

- deprecated/ 目录保留旧代码
- REFACTOR_DOCUMENTATION.md 详细记录变更
- 数据库迁移用 Alembic，可回滚

**原因**：大重构不能一步到位。保留旧代码作为参考，记录设计决策，允许回退

---

## 代码规范

### 基础格式规范

- 所有的代码文件必须使用UTF-8编码
- 所有的代码文件必须使用4个空格缩进，不允许使用Tab缩进
- PR/commit时不要有任何语法错误（红线）
- 文件末尾必须有一个换行符
- 使用PyCharm默认的代码规范（变量命名，类命名，换行，空格，注释）（在默认情况下不要出现黄线，明显是linter的错误的除外）

### 类型注解规范

- 所有的类型注解都必须使用Python 3.10+的简化语法
  - 例如：使用 `dict[str, Any] | None` 而不是 `Optional[Dict[str, Any]]`
  - 用字符串表示可空的类型标注时，不能用 `"TypeName" | None`（这是语法错误），必须使用 `'TypeName | None'`（用单引号包裹整体类型）
- **使用内置类型而非typing模块**：
  - 使用 `type[ClassName]` 而不是 `Type[ClassName]`
  - 使用 `list[int]` 而不是 `List[int]`
  - 使用 `dict[str, Any]` 而不是 `Dict[str, Any]`
  - 使用 `tuple[int, str]` 而不是 `Tuple[int, str]`
  - 使用 `set[str]` 而不是 `Set[str]`
  - Python 3.9+ 支持直接使用内置类型作为泛型，无需从typing导入
- 参数、类变量、实例变量等必须有类型注解，函数返回必须要注明类型
- 所有的类型注解都必须是明确的类型，不能使用 `Any` 或 `object`，除非确实无法确定类型，需要明确使用todo标注，以便后期研究类型
- 所有的类型注解都必须是具体的类型，不能使用泛型（如 `List`、`Dict`、`Tuple`、`Set`、`Union` 等），必须使用具体的类型（如 `list[int]`、`dict[str, Any]`、`tuple[int, str]`、`set[str]`、`int | str` 等）
- 所有的类型注解都必须是导入的类型，不能使用字符串表示类型（如 `def func(param: 'CustomType') -> 'ReturnType':`），除非是**前向引用**（即类型在当前作用域中还未定义）

### 异步编程规范

- 使用FastAPI管理的事件循环，不要再新建任何事件循环，不论是在任何线程或任何子进程中
- IO操作必须使用协程，不涉及任何CPU密集或IO的操作必须不使用协程，按需使用to_thread线程或Celery Worker
- 所有的数据库操作必须使用异步数据库驱动（如SQLModel的AsyncSession），不允许使用同步数据库驱动
- 所有的HTTP请求必须使用异步HTTP客户端（如aiohttp），不允许使用同步HTTP客户端
- 所有的文件操作必须使用异步文件操作库（如aiofiles），不允许使用同步文件操作
- 所有的子进程操作必须使用异步子进程库（如anyio），不允许使用同步子进程库
- 所有的第三方库调用必须使用异步版本，不允许使用同步版本，如果没有同步版本，视cpu负载情况使用to_thread线程或Celery Worker
- 所有的高cpu阻塞操作必须使用to_thread线程或Celery Worker，不允许在协程中直接调用高cpu阻塞操作

### 函数与参数规范

- 一个方法最多五个参数，多了考虑拆分方法或合并参数（SQLModel），不要简单的用tuple或dict

### 代码格式规范

- **容器类型定义**：元组、字典、列表定义时，若定义只用了一行，则最后一个元素后面一律不加逗号，否则一律加逗号
- **括号换行**：括号要么不换行，要么换行且用下面的形式写（一行最多一个变量，以逗号和换行分割）

#### 示例代码

```python
from loguru import logger as l

from api_client_models import (
    AgentModelsRequest,
    ReportRequest,
    SaveMemoryRequest,
    UserInfoResponse,
)

async def lookup_user_info(
        session: AsyncSession,
        user_id: int,
        short_name: str,
        data_1_with_a_long_name: dict[str, Any] | None,
        data_2_with_a_even_longer_name: CustomType
) -> UserInfoResponse:
    user = await User.get(session, User.id == user_id)
    new_dict = { user_id, short_name }
    l.debug(f"查到的数据: {new_dict}")
    result = UserInfoResponse(
        user.id,
        user.a_long_attribute,
        data_1_with_a_long_name,
        data_2_with_a_even_longer_name,
    )

    return result
```

### 文档与注释规范

- 复杂的类或函数（无法从名字推断明确的操作，如 `handle_connection()`）一律要写docstring，采用reStructuredText风格

### 字符串处理规范

- **引号使用**：单引号 `'` 用于给电脑看的文本（字典的键），双引号 `"` 用于给人看的文本（面向用户的提示，面向开发者的注释、log信息等）
- **字符串格式化**：所有的字符串都用f-string格式化，不要使用 `%` 或 `.format()`
- **多行字符串**：多行字符串使用"""或'''，"""给人看(如docstring)，'''给电脑看（如SQL语句或HTML内容）

### 命名规范

- 除非专有名词，代码中不要出现任何拼音变量名，所有变量名必须是英文
- 所有的变量名、函数名、方法名、参数名都必须使用蛇形命名法（snake_case）
- 所有的类名都必须使用帕斯卡命名法（PascalCase）
- 所有的常量名都必须使用全大写蛇形命名法（UPPER_SNAKE_CASE）
- 所有的私有变量、私有方法都必须使用单下划线前缀（_private_var）
- 所有的非常私有变量、非常私有方法都必须使用双下划线前缀（__very_private_var）
- 所有的布尔变量都必须使用is_、has_、can_、should_等前缀命名，且变量名必须是形容词或动词短语（如 is_valid, has_data, can_execute, should_retry）

### 异常处理规范

- 所有的异常都必须被捕获，且要有明确的处理逻辑
- 如果出现错误，不要return None，这样会造成隐藏的不易发现的错误，必须明确抛出异常

### 日志处理规范

- 所有的日志都必须用 `from loguru import logger as l` 处理，不要使用print
- 所有的日志都必须有明确的上下文，且要有明确的日志级别

### 框架使用规范

- 使用SQLModel，而不是Pydantic或SQLAlchemy。
- 使用SQLModel时禁止从future导入annotations
- 使用SQLModel时禁止从future导入annotations
- 使用SQLModel时禁止从future导入annotations
- 使用FastAPI，而不是Flask或Django
- 使用Aiohttp，而不是Requests
- 使用Aiofiles，而不是内置的open

```python
import os as sync_os
from aiofiles import os, open
...
async with open('file.txt', 'r') as f:
    content = await f.read()
...
path = sync_os.path(...)
```

- 使用Anyio，而不是内置的subprocess
- 使用Loguru，而不是内置的logging：`from loguru import logger as l`
- 使用Celery，而不是内置的multiprocessing
- 使用GitHub Desktop，而不是直接在文件系统操作
- 使用PyCharm，而不是其他IDE

### JSON处理规范

**永远使用SQLModel/Pydantic的内置序列化方法**，不要手动调用json库：

#### 1. 模型序列化（推荐）

```python
# ✅ 正确：使用 model_dump_json()
from sqlmodels.character.messages import TextEchoMessage

message = TextEchoMessage(text="你好", msg_id="123")
json_str: str = message.model_dump_json()  # 直接返回JSON字符串

# ✅ 正确：如果需要字典
message_dict: dict = message.model_dump()
```

#### 2. 原始JSON处理（仅在必要时）

如果需要处理不是SQLModel/Pydantic的原始JSON数据：

```python
# ✅ 正确：使用 orjson
import orjson

# 解析JSON
data: dict = orjson.loads(json_bytes)  # 接受 bytes 或 str

# 生成JSON
json_bytes: bytes = orjson.dumps(data)  # 返回 bytes
json_str: str = orjson.dumps(data).decode('utf-8')  # 需要str时decode
```

#### 3. 错误示例

```python
# ❌ 错误：使用标准库json
import json
json_str = json.dumps(message.model_dump())

# ❌ 错误：手动调用orjson序列化模型
import orjson
json_str = orjson.dumps(message.model_dump()).decode('utf-8')

# ✅ 正确：直接用模型方法
json_str = message.model_dump_json()
```

#### 4. 消息序列化示例

```python
# ✅ 正确：使用模型内置序列化
json_str: str = message.model_dump_json()
# 通过MQTT或HTTP发送
await mqtt_client.publish(topic, json_str)

# ❌ 错误：手动序列化
json_str = orjson.dumps(message.model_dump()).decode('utf-8')
```

**配置说明**：

- SQLModel/Pydantic v2 内部可配置使用 orjson 作为序列化器
- `model_dump_json()` 比手动序列化更快且类型安全
- 标准库 json 已被项目全面禁用

### 安全规范

- **禁止硬编码敏感信息**：API密钥、数据库密码、JWT密钥等必须使用环境变量或安全配置管理
- **使用环境变量**：通过 `os.getenv()` 或配置文件读取敏感信息
- **SQL注入防护**：使用SQLModel/SQLAlchemy的参数化查询，禁止字符串拼接SQL
- **JWT认证**：WebSocket和敏感端点必须验证JWT token
- **CORS配置**：生产环境必须配置正确的CORS策略

**错误示例**：

```python
# ❌ 严重错误：硬编码API密钥
api_key: str = "bce-v3/ALTAK-xcRfCL5sLloSNKpU3z9xX/..."
```

**正确示例**：

```python
# ✅ 正确：从环境变量读取
import os
api_key: str = os.getenv("BAIDU_API_KEY")
if not api_key:
    raise ValueError("BAIDU_API_KEY environment variable not set")
```

### AI编码规范

- 如果有条件，inline completion插件使用GitHub Copilot，而不是JetBrains自带的
- 如果让AI直接编码，使用Gemini 2.5 Pro及以上, Claude 3.7 Sonnet Thinking及以上，而不是GPT系列模型，DeepSeek，豆包，文心一言等
- 使用AI生成代码时，提示词必须带上这个代码规范
- 在实现任何功能前，必须先看看有没有现成的解决方案，比如pypi包，不要重复造轮子

### SQLModel规范

- 使用字段后面的"""..."""（docstring）而不是参数description="..."来写字段描述

**示例**：

```python
class User(SQLModel, table=True):
    model_config = ConfigDict(use_attribute_docstrings=True)

    id: int = Field(default=None, primary_key=True, description="用户ID")  # 错误示范
    name: str = Field(description="用户名")  # 错误示范
    email: str = Field(unique=True)  # 正确示范
    """用户邮箱"""
```

- **Field使用原则**：
  - **只有default参数时**：直接赋值，不使用Field
  - **有其他参数时**（如ge, le, foreign_key, unique等）：必须使用Field

```python
# 错误示范
class CharacterConfig(SQLModelBase):
    vad_frame_ms: int = Field(default=20)  # 只有default，不应该用Field
    """VAD帧大小（毫秒）"""

    vad_aggressiveness: int = Field(default=2, ge=0, le=3)  # 正确，有ge/le约束
    """VAD激进程度（0-3）"""

# 正确示范
class CharacterConfig(SQLModelBase):
    vad_frame_ms: int = 20  # 只有default，直接赋值
    """VAD帧大小（毫秒）"""

    vad_aggressiveness: int = Field(default=2, ge=0, le=3)  # 有约束，使用Field
    """VAD激进程度（0-3）"""

    llm_id: UUID = Field(..., foreign_key='llm.id')  # 有foreign_key，使用Field
    """LLM配置ID"""
```

- **不要重复定义model_config**：SQLModelBase已经定义了 `model_config = ConfigDict(use_attribute_docstrings=True, validate_by_name=True)`，所有继承自SQLModelBase的类都会自动继承这个配置，**不需要重复定义**

```python
# 错误示范
class OTARequest(SQLModelBase):
    model_config = ConfigDict(use_attribute_docstrings=True)  # 不必要的重复

    application: OTAApplicationInfo
    """应用信息"""

# 正确示范
class OTARequest(SQLModelBase):
    application: OTAApplicationInfo
    """应用信息"""
```

- 请一律使用TableBase系列类提供的crud，不要试图直接操作session
- 所有的SQLModel类都必须继承自SQLModelBase或其子类，请不要直接继承SQLModel
- 所有的存数据库的类必须继承自TableBase的子类，并且table=True
- 所有的不存数据库的类必须继承自SQLModelBase
- 定义枚举类请使用 `StrEnum` 而不是 `(str, Enum)`
- **TableBase CRUD方法返回值规范**：

  - **必须使用返回值**：`save()` 和 `update()` 方法调用后，session中的所有对象都会过期（expired），必须使用返回值，而不是继续使用原对象

```python
# ✅ 正确：使用返回值
device = ClientDevice(...)
device = await device.save(session)
return device

# ❌ 错误：不使用返回值（device对象已过期）
device = ClientDevice(...)
await device.save(session)
return device  # 此时device已过期，访问属性会报错

# ✅ 正确：update也要使用返回值
device = await device.update(session, update_data)
return device

# ❌ 错误：不使用返回值
await device.update(session, update_data)
return device  # 此时device已过期
```

**原因**：`save()` 和 `update()` 内部调用了 `session.commit()`，commit后SQLAlchemy会让所有对象过期以确保数据一致性。这些方法内部会调用 `session.refresh(self)` 来刷新对象，并返回刷新后的实例。

### 队列驱动架构规范

**使用场景**：需要解耦生产者和消费者时使用 `asyncio.Queue`

**设计原则**：

- 队列在 `model_post_init()` 中初始化（运行时属性）
- 提供清晰的 put/get 接口供外部调用
- 后台任务持续处理队列（使用循环）
- 使用 `asyncio.CancelledError` 优雅退出

**示例 - Character消息处理**：

```python
import asyncio
from sqlmodel import Field
from sqlmodels.base import UUIDTableBase, SQLModelBase

class CharacterBase(SQLModelBase):
    name: str
    """角色名称"""

class Character(CharacterBase, UUIDTableBase):
    """充血模型：包含数据和业务逻辑"""

    # ==================== 运行时属性（在model_post_init初始化） ====================
    _input_queue: asyncio.Queue
    """消息输入队列（由ClientDevice写入）"""

    _output_queue: asyncio.Queue
    """消息输出队列（由ClientDevice读取）"""

    _processor_task: asyncio.Task | None
    """后台处理任务"""

    def model_post_init(self, __context) -> None:
        """初始化运行时属性"""
        self._input_queue = asyncio.Queue()
        self._output_queue = asyncio.Queue()
        self._processor_task = None

    # ==================== 公共接口 ====================
    async def put_input_message(self, msg: str | bytes) -> None:
        """写入输入队列（由ClientDevice调用）"""
        await self._input_queue.put(msg)

    async def get_output_message(self) -> str | bytes:
        """读取输出队列（由ClientDevice调用）"""
        return await self._output_queue.get()

    # ==================== 后台任务 ====================
    async def _message_processor_loop(self, session: AsyncSession) -> None:
        """后台任务：持续处理输入队列"""
        try:
            while True:
                msg = await self._input_queue.get()

                # 处理消息
                response = await self._process_message(msg, session)

                # 输出结果
                await self._output_queue.put(response)
        except asyncio.CancelledError:
            # 优雅退出
            pass
        finally:
            # 清理资源
            pass

    async def _process_message(self, msg: str | bytes, session: AsyncSession) -> str:
        """处理单条消息"""
        # 业务逻辑
        return f"处理结果: {msg}"

    # ==================== 生命周期管理 ====================
    @asynccontextmanager
    async def init(self, session: AsyncSession):
        """初始化并启动后台任务"""
        # 启动后台任务
        self._processor_task = asyncio.create_task(
            self._message_processor_loop(session)
        )

        try:
            yield
        finally:
            # 取消后台任务
            if self._processor_task:
                self._processor_task.cancel()
                try:
                    await self._processor_task
                except asyncio.CancelledError:
                    pass
```

**使用示例**：

```python
# 在ClientDevice中使用
async with character.init(session):
    # 发送消息
    await character.put_input_message("你好")

    # 接收响应
    response = await character.get_output_message()
    # 通过MQTT或UDP发送（具体取决于消息类型）
    if isinstance(response, bytes):
        await udp_client.send(response)  # 音频数据
    else:
        await mqtt_client.publish(topic, response)  # 控制消息
```

**关键点**：

- ✅ 队列明确标记为 `_` 开头（私有属性）
- ✅ 提供公共的 put/get 方法（封装队列操作）
- ✅ 后台任务使用 `asyncio.create_task()` 启动
- ✅ 使用 `@asynccontextmanager` 确保资源清理
- ✅ 捕获 `CancelledError` 优雅退出

### 联表继承（Joined Table Inheritance）规范

当需要实现多态的数据库模型时（如ASR、TTS、Tool等），使用联表继承模式。项目提供了通用工具简化实现：

**基本结构**：

1. **Base类**：只包含字段，不继承TableBase（无表）
2. **抽象父类**：继承Base + UUIDTableBase + ABC，有自己的表
3. **SubclassIdMixin**：为子类提供外键指向父表的主键
4. **AutoPolymorphicIdentityMixin**：自动生成polymorphic_identity

**完整示例**：

```python
from abc import ABC, abstractmethod
from uuid import UUID
from sqlmodel import Field
from sqlmodels.base import (
    SQLModelBase,
    UUIDTableBase,
    create_subclass_id_mixin,
    AutoPolymorphicIdentityMixin
)

# 1. 定义Base类（只有字段，无表）
class ASRBase(SQLModelBase):
    name: str
    """配置名称"""

    base_url: str
    """服务地址"""

    language: str = "zh"
    """语言代码：'zh' | 'en' | 'auto'"""

# 2. 定义抽象父类（有表）
class ASR(
    ASRBase,
    UUIDTableBase,
    ABC,
    polymorphic_on='__polymorphic_name',
    polymorphic_abstract=True
):
    """ASR配置的抽象基类"""

    __polymorphic_name: str
    """多态类型鉴别器，用于区分不同的ASR子类"""

    @abstractmethod
    async def transcribe(self, pcm_data: bytes) -> str:
        """转录音频为文本"""
        pass

# 3. 为第二层子类创建ID Mixin
ASRSubclassIdMixin = create_subclass_id_mixin('asr')

# 4. 创建第二层抽象类（如果需要多级继承）
class FunASR(
    ASRSubclassIdMixin,
    ASR,
    AutoPolymorphicIdentityMixin,
    polymorphic_abstract=True
):
    """FunASR的抽象基类"""
    # polymorphic_identity 会自动设置为 'funasr'

    model_size: str = "medium"
    """模型大小"""

# 5. 创建具体实现类
class FunASRLocal(FunASR, table=True):
    """FunASR本地部署版本"""
    # polymorphic_identity 会自动设置为 'funasr.funasrlocal'

    model_path: str
    """本地模型路径"""

    async def transcribe(self, pcm_data: bytes) -> str:
        # 具体实现
        pass

class FunASRCloud(FunASR, table=True):
    """FunASR云端版本"""
    # polymorphic_identity 会自动设置为 'funasr.funasrcloud'

    api_key: str
    """云端API密钥"""

    async def transcribe(self, pcm_data: bytes) -> str:
        # 具体实现
        pass
```

**工具说明**：

1. **`create_subclass_id_mixin(parent_table_name: str)`**

   - 动态创建SubclassIdMixin类
   - 提供 `id: UUID = Field(foreign_key='parent_table.id', primary_key=True)`
   - 必须放在继承列表的第一位，确保通过MRO覆盖UUIDTableBase的id
2. **`AutoPolymorphicIdentityMixin`**

   - 自动根据类名生成polymorphic_identity
   - 格式：`{parent_identity}.{classname_lowercase}`
   - 如果没有父类identity，直接使用类名小写

**注意事项**：

- SubclassIdMixin必须放在继承列表**第一位**（MRO优先级）
- AutoPolymorphicIdentityMixin放在靠后位置（在ABC之前）
- 如果需要手动指定polymorphic_identity，可以在类定义时传入参数：
  ```python
  class CustomASR(ASR, table=True, polymorphic_identity='my_custom_asr'):
      pass
  ```

---

### `__init__.py` 模块组织规范

`__init__.py` 是Python包的入口文件，本项目根据不同场景使用不同的组织模式。

#### 模式一：模块导出模式（SQLModel/业务模块）

**用途**：从子模块收集和重新导出公共API

**特征**：

- 使用相对导入 `from .xxx import ...`
- 平铺导出所有需要外部访问的类/函数/常量
- 可选：使用分组注释说明导出内容的类型
- **可选但推荐**：添加模块级 docstring 说明架构和历史变更

**基础示例**：

```python
# sqlmodels/user/__init__.py
from .user import (
    User,
    UserSourceMethodEnum,
    UserInfoResponse,
    UserLoginOrRegisterRequest,
    UserJWTPayload,
)
from .speaker_info import (
    SpeakerInfo,
    SpeakerInfoBase,
    SpeakerData,
    SpeakerIdentificationResult,
    SexEnum,
    SpeakerSourceTypeEnum,
    SpeakerInfoExtractionException,
)
```

**分组注释示例**（当导出内容较多时）：

```python
# sqlmodels/character/__init__.py
"""Character模块 - 统一导出"""

from .character import (
    # 数据库模型
    Character,
    UserCharacterLinkModel,
    CharacterBase,

    # 消息和常量
    Messages,
    DEFAULT_SUMMARY_PROMPT,
)

from .memories.text.text import TextMemory
from .messages import CharacterOutputMessageBase, TextEchoMessage, AudioPlaybackEndMessage
```

**文档化导出示例**（⭐ 可选但推荐）：

**注意**：文档化导出并不是必须的，对于任何包都是**可选但推荐**的。当模块架构复杂或有重要历史变更时，建议使用此模式。

```python
# sqlmodels/character/asr/__init__.py
"""
ASR（Automatic Speech Recognition）配置模块

使用联表继承（Joined Table Inheritance）实现多态ASR配置。

架构：
    ASR (抽象基类，有表)
    └── WebSocketASR (WebSocket连接到外部ASR Service) [推荐]

历史：
    - FunASR, ExperimentalASR 已移除（使用HTTP API，已被WebSocketASR替代）
"""
from .base import ASR, ASRBase, ASRException
from .websocket_asr import WebSocketASR, WebSocketASRBase

# WebSocket消息定义
from .websocket_messages import (
    MessageTypeEnum,
    ErrorMessage,
    EndOfStreamMessage,
    TranscriptionInfo,
    TranscriptionResponse,
)
```

**适用场景**：

- `sqlmodels/` 下的所有子包
- `utils/` 等工具模块
- 所有业务逻辑模块

**推荐添加文档化的场景**：

- 使用联表继承的配置模块（ASR, TTS, LLM, Tool）
- 有历史演进需要记录的模块
- 架构复杂需要说明的模块

---

#### 模式二：FastAPI路由聚合模式（路由中间节点）

**用途**：构建层级化的API路由结构

**特征**：

- 从 `fastapi` 导入 `APIRouter`
- 创建带 `prefix` 的 router
- 通过 `router.include_router()` 包含子路由
- 导出 router 供上层包含

**示例**：

```python
# root_endpoint/__init__.py
from fastapi import APIRouter
from .api import router as api_router

router = APIRouter()
router.include_router(api_router)
```

```python
# root_endpoint/api/__init__.py
from fastapi import APIRouter
from .v1 import router as v1_router

router = APIRouter(prefix="/api")
router.include_router(v1_router)
```

```python
# root_endpoint/api/v1/__init__.py
from fastapi import APIRouter
from .admin import router as admin_router
from .character import router as character_router
from .device import router as device_router
from .llm import router as llm_router
from .ota import router as ota_router
from .rva import router as rva_router
from .tts import router as tts_router
from .user import router as user_router
from .verification_code import router as verification_code_router

router = APIRouter(prefix="/v1")
router.include_router(admin_router)
router.include_router(character_router)
router.include_router(device_router)
router.include_router(llm_router)
router.include_router(ota_router)
router.include_router(rva_router)
router.include_router(tts_router)
router.include_router(user_router)
router.include_router(verification_code_router)
```

**路由层次**：

```
root_endpoint/           → /
└── api/                 → /api
    └── v1/              → /api/v1
        ├── admin/       → /api/v1/admin
        ├── character/   → /api/v1/character
        ├── device/      → /api/v1/device
        ├── llm/         → /api/v1/llm
        ├── ota/         → /api/v1/ota
        ├── rva/         → /api/v1/rva
        ├── tts/         → /api/v1/tts
        ├── user/        → /api/v1/user
        └── verification_code/  → /api/v1/verification_code
```

**适用场景**：

- `root_endpoint/` 及其所有非叶子子目录
- 所有需要路由聚合的中间层节点

---

#### 模式三：FastAPI端点实现模式（路由叶子节点）

**用途**：在 `__init__.py` 中直接定义端点处理函数

**特征**：

- 创建带 `prefix` 的 `APIRouter`
- 导入依赖项和数据模型
- 使用 `@router.post/get/websocket` 装饰器定义端点
- 包含详细的 docstring 说明端点行为

**示例**：

```python
# root_endpoint/api/v1/user/__init__.py
from fastapi import APIRouter
from loguru import logger as l

from dependencies import SessionDep, CurrentActiveUserDep, ServerConfigDep
from sqlmodels.user import UserLoginOrRegisterRequest, UserSourceMethodEnum
from sqlmodels import User

router = APIRouter(prefix="/user")

@router.post('')
async def register_or_login(
        session: SessionDep,
        user: CurrentActiveUserDep,
        server_config: ServerConfigDep,
        request: UserLoginOrRegisterRequest
) -> ...:
    """
    用户注册或登录端点

    如果用户不存在则注册，存在则登录。
    """
    source: UserSourceMethodEnum = request.source

    if server_config.require_captcha:
        # 验证码逻辑
        pass

    # 生成并返回令牌
    pass
```

**FastStream MQTT订阅器示例**：

```python
# stream/subscribers/device_input.py
"""
设备输入订阅器

订阅Stream: devices:input
功能：验证设备输入并转发到角色处理Stream
"""
from typing import Any
from uuid import UUID

from faststream import FastStream
from loguru import logger as l
from sqlmodel.ext.asyncio.session import AsyncSession

from dependencies import SessionDep
from sqlmodels.character import Character
from sqlmodels.client_device import ClientDevice
from sqlmodels.database_connection import DatabaseManager

from ..app import CHARACTERS_PROCESSING_STREAM, DEVICES_INPUT_STREAM, broker


@broker.subscriber(DEVICES_INPUT_STREAM, group="device-input-processor")
async def handle_device_input(msg: dict[str, Any]) -> None:
    """
    处理设备输入消息并转发到角色处理Stream

    流程：
    1. 验证消息格式（device_id, character_id必填）
    2. PostgreSQL-first验证ClientDevice和Character存在性
    3. 转发到characters:processing Stream

    消息格式：
    - 上行（MQTT/UDP）: {"device_id": "uuid", "character_id": "uuid", "type": "audio"|"text", "data": ...}
    - 下行（FastStream）: 转发到characters:processing Stream

    认证：
    - MQTT: 通过Hello握手建立会话
    - UDP: 通过SessionInfo验证序列号

    错误处理：
    - 验证失败: 记录日志并清理Redis状态
    - 设备不存在: 拒绝处理
    - 角色不存在: 拒绝处理
    """
    try:
        # 验证消息格式
        device_id_str: str | None = msg.get('device_id')
        character_id_str: str | None = msg.get('character_id')

        if not device_id_str or not character_id_str:
            l.warning(f"消息格式无效: {msg}")
            return

        device_id = UUID(device_id_str)
        character_id = UUID(character_id_str)

        # 验证设备和角色存在
        async with DatabaseManager.session() as session:
            device = await ClientDevice.get(
                session,
                ClientDevice.id == device_id,
                fetch_mode='one_or_none'
            )
            if not device:
                l.warning(f"设备不存在: {device_id}")
                return

            character = await Character.get(
                session,
                Character.id == character_id,
                fetch_mode='one_or_none'
            )
            if not character:
                l.warning(f"角色不存在: {character_id}")
                return

        # 转发到处理Stream
        await broker.publish(
            msg,
            stream=CHARACTERS_PROCESSING_STREAM
        )
        l.debug(f"已转发消息到处理队列: device={device_id}, character={character_id}")

    except ValueError as e:
        l.error(f"消息解析错误: {e}")
    except Exception as e:
        l.exception(f"处理设备输入异常: {e}")
```

**适用场景**：

- `root_endpoint/api/v1/` 下的所有叶子端点目录
- 所有需要定义具体端点的目录

---

#### 命名约定

- **相对导入**：一律使用 `from .xxx import ...`，不使用 `from package.xxx import ...`
- **子路由命名**：统一格式 `from .子目录 import router as 子目录_router`
- **类型导出**：导出类的同时导出相关的枚举、异常、DTO、常量

**示例**：

```python
# ✅ 正确
from .base import Tool, ToolResponse, ToolTypeEnum, ToolException

# ❌ 错误
from sqlmodels.character.llm.openai_compatibles.tools.base import Tool
```

---

#### 导出粒度原则

**应该导出的内容**：

- ✅ 需要被外部模块使用的类、函数、常量
- ✅ 数据库模型及其配套的枚举、异常、DTO
- ✅ 抽象基类和具体实现类
- ✅ 公共工具函数和常量

**不应该导出的内容**：

- ❌ 以 `_` 开头的私有对象
- ❌ 只在包内部使用的辅助函数
- ❌ 实现细节（如内部使用的临时类）

**关于 `__all__` 的规定**：

**禁止使用 `__all__`**。`__init__.py` 应该只负责显式导出必要的公共内容，私有内容（以 `_` 开头）**不允许**在 `__init__.py` 中导出。通过显式的 `from .xxx import ...` 语句已经清楚表明了导出意图，使用 `__all__` 会造成冗余和维护负担。

**错误示例**：

```python
# ❌ 错误：使用 __all__
from .base import Tool, _validate_tool_name

__all__ = ['Tool']  # 不要使用 __all__
```

**正确示例**：

```python
# ✅ 正确：只导出公共API，不使用 __all__
from .tool import Tool, ToolResponse, ToolTypeEnum
from .function import Function, FunctionParam
from .exceptions import ToolException

# _validate_tool_name() 是私有函数，不在这里导入，自然不会导出
```

**原因**：

1. 显式导入已经明确了导出意图，`__all__` 是冗余的
2. 私有内容（`_xxx`）不应该出现在 `__init__.py` 中
3. 减少维护成本（不需要同时维护导入列表和 `__all__` 列表）
4. 符合"显式优于隐式"的设计哲学

---

#### FastAPI路由结构规则

**层级规则**：

每层 `__init__.py` 的职责：

1. 创建本层 `APIRouter`（设置 `prefix`）
2. 包含所有直接子路由
3. 导出 `router` 供上层包含

**完整示例**：

```python
# 第一层：root_endpoint/__init__.py
from fastapi import APIRouter
from .api import router as api_router

router = APIRouter()
router.include_router(api_router)

# 第二层：root_endpoint/api/__init__.py
from fastapi import APIRouter
from .v1 import router as v1_router

router = APIRouter(prefix="/api")
router.include_router(v1_router)

# 第三层：root_endpoint/api/v1/__init__.py
from fastapi import APIRouter
from .user import router as user_router
from .character import router as character_router

router = APIRouter(prefix="/v1")
router.include_router(user_router)
router.include_router(character_router)

# 第四层：root_endpoint/api/v1/user/__init__.py
from fastapi import APIRouter

router = APIRouter(prefix="/user")

@router.post('/login')
async def login(...):
    pass
```

**URL与目录对应关系**：

| URL路径                | 文件路径                                  | prefix设置         |
| ---------------------- | ----------------------------------------- | ------------------ |
| `/`                  | `root_endpoint/__init__.py`             | 无                 |
| `/api`               | `root_endpoint/api/__init__.py`         | `prefix="/api"`  |
| `/api/v1`            | `root_endpoint/api/v1/__init__.py`      | `prefix="/v1"`   |
| `/api/v1/user`       | `root_endpoint/api/v1/user/__init__.py` | `prefix="/user"` |
| `/api/v1/user/login` | 端点装饰器 `@router.post('/login')`     | -                  |

**关键原则**：

- ✅ URL结构 = 目录结构（设计哲学第6条）
- ✅ prefix只写当前层的路径部分，不包含父路径
- ✅ 中间节点负责聚合，叶子节点负责实现
- ❌ 禁止在 `root_endpoint/` 下创建独立的 `.py` 文件（只允许 `__init__.py` 和子目录）

---

#### 导入顺序规范（符合PEP 8和Black）

所有 `__init__.py` 文件必须遵循以下导入顺序：

```python
# 1. 标准库导入
from typing import Any
from uuid import UUID

# 2. 第三方库导入
from fastapi import APIRouter
from loguru import logger as l
from sqlmodel import Field

# 3. 本地应用导入（从项目根目录的包开始）
from dependencies import SessionDep
from sqlmodels.user import User
from sqlmodels.base import UUIDTableBase

# 4. 相对导入（同包内的模块）
from .base import BaseClass
from .submodule import SubClass
```

**分组规则**：

- 每组之间用**一个空行**分隔
- 同组内按字母顺序排序（`from` 语句按模块名排序）
- 相对导入永远放在最后

**错误示例**：

```python
# ❌ 混乱的导入顺序
from .base import BaseClass
from fastapi import APIRouter
from sqlmodels.user import User
from typing import Any
from .submodule import SubClass
```

**正确示例**：

```python
# ✅ 清晰的导入顺序
from typing import Any

from fastapi import APIRouter

from sqlmodels.user import User

from .base import BaseClass
from .submodule import SubClass
```

---

#### 特殊注意事项

1. **所有Python包目录都必须有 `__init__.py`**

   - 即使是空文件也要创建
   - 空文件可以只包含一个 pass 或留空
   - 确保包可以被正确导入
2. **避免循环导入**

   - 顶层 `__init__.py`（如 `sqlmodels/__init__.py`）可以导出常用的顶层类
   - 子模块的 `__init__.py` 只导出本包内容
   - **禁止向上导入**（`from ..parent import`）
3. **类型提示的导出**

   - 如果导出泛型类型变量（如 `T`），需要一并导出
   - 例如：`from .table_base import TableBase, UUIDTableBase, T`
4. **FastAPI端点的docstring必须包含**

   - 端点功能描述
   - 认证方式说明
   - 请求/响应格式规范
   - 异常处理说明

**示例**：

```python
@router.post("/character")
async def create_character(
        session: SessionDep,
        current_user: CurrentActiveUserDep,
        character_data: CharacterBase
):
    """
    创建角色端点

    功能：创建新的Character配置

    认证：
    - JWT token in Authorization header
    - 验证用户存在且激活

    请求体：
    - CharacterBase模型（JSON格式）

    响应：
    - 完整的Character对象（包含ID）

    错误处理：
    - HTTPException 400: 请求数据无效
    - HTTPException 401: 未授权
    - HTTPException 500: 服务器错误
    """
    pass
```

---

#### 使用模式决策树

**如何选择使用哪个模式？**

```
是 __init__.py 文件吗？
├─ 否 → 不适用本规范
└─ 是
   ├─ 是 root_endpoint/ 下的文件吗？
   │  ├─ 是
   │  │  ├─ 包含子路由吗（有 router.include_router()）？
   │  │  │  ├─ 是 → 模式二：FastAPI路由聚合
   │  │  │  └─ 否 → 模式三：FastAPI端点实现
   │  │  └─ ...
   │  └─ 否 → 模式一：模块导出（考虑添加文档化说明）
   └─ ...
```

**快速参考表**：

| 目录类型        | 使用模式             | 核心特征                          |
| --------------- | -------------------- | --------------------------------- |
| SQLModel业务包  | 模式一               | `from .xxx import ...` 平铺导出 |
| 配置类子包      | 模式一（建议文档化） | 包含架构docstring + 导出          |
| FastAPI中间节点 | 模式二               | `router.include_router()` 聚合  |
| FastAPI叶子节点 | 模式三               | `@router.post/websocket` 实现   |

---

**注意**：此规范会持续更新，对此文件有任何建议修改可以发起PR，没有在规范里提到的都没有硬性要求，可以参考[PEP 8](https://peps.python.org/pep-0008/)
