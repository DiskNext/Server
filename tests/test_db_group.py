import pytest

@pytest.mark.asyncio
async def test_group_curd():
    """测试数据库的增删改查"""
    from models import database, migration
    from models.group import Group
    
    await database.init_db(url='sqlite:///:memory:')
    
    await migration.migration()
    
    # 测试增 Create
    test_group = Group(name='test_group')
    created_group = await Group.create(test_group)
    
    assert created_group is not None
    assert created_group.id is not None
    assert created_group.name == 'test_group'
    
    # 测试查 Read
    fetched_group = await Group.get(id=created_group.id)
    assert fetched_group is not None
    assert fetched_group.id == created_group.id
    assert fetched_group.name == 'test_group'
    
    # 测试更新 Update
    updated_group = await Group.set(
        id=fetched_group.id,
        name='updated_group')
    
    assert updated_group is not None
    assert updated_group.id == fetched_group.id
    assert updated_group.name == 'updated_group'
    
    # 测试删除 Delete
    await Group.delete(id=updated_group.id)
    deleted_group = await Group.get(id=updated_group.id)
    assert deleted_group is None