import pytest

@pytest.mark.asyncio
async def test_initialize_db():
    """测试创建数据库结构"""
    from models import database
    
    await database.init_db(url='sqlite:///:memory:')

@pytest.fixture
async def db_session():
    """测试获取数据库连接Session"""
    from models import database
    
    await database.init_db(url='sqlite:///:memory:')
    
    async for session in database.get_session():
        yield session

@pytest.mark.asyncio
async def test_initialize_db():
    """测试数据库创建并初始化配置"""
    from models import migration
    from models import database
    
    await database.init_db(url='sqlite:///:memory:')
    
    await migration.init_default_settings()

@pytest.mark.asyncio
async def test_add_settings():
    """测试数据库的增删改查"""
    from models import database
    from models.setting import Setting
    
    await database.init_db(url='sqlite:///:memory:')
    
    # 测试增 Create
    await Setting.add(
        type='example_type', 
        name='example_name', 
        value='example_value')
    
    # 测试查 Read
    setting = await Setting.get(
        type='example_type', 
        name='example_name')
    
    assert setting is not None, "设置项应该存在"
    assert setting.value == 'example_value', "设置值不匹配"
    
    # 测试改 Update
    await Setting.set(
        type='example_type', 
        name='example_name', 
        value='updated_value')
    
    after_update_setting = await Setting.get(
        type='example_type', 
        name='example_name'
        )
    
    assert after_update_setting is not None, "设置项应该存在"
    assert after_update_setting.value == 'updated_value', "更新后的设置值不匹配"
    
    # 测试删 Delete
    await Setting.delete(
        type='example_type', 
        name='example_name')
    
    after_delete_setting = await Setting.get(
        type='example_type', 
        name='example_name'
    )
    
    assert after_delete_setting is None, "设置项应该被删除"