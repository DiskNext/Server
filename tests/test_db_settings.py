import pytest

@pytest.mark.asyncio
async def test_settings_curd():
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
    assert setting == 'example_value', "设置值不匹配"
    
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
    assert after_update_setting == 'updated_value', "更新后的设置值不匹配"
    
    # 测试删 Delete
    await Setting.delete(
        type='example_type', 
        name='example_name')
    
    after_delete_setting = await Setting.get(
        type='example_type', 
        name='example_name'
    )
    
    assert after_delete_setting is None, "设置项应该被删除"