import pytest

@pytest.mark.asyncio
async def test_user_curd():
    """测试数据库的增删改查"""
    from models import database, migration
    from models.group import Group
    from models.user import User
    
    await database.init_db(url='sqlite:///:memory:')
    
    await migration.migration()
    
    # 新建一个测试用户组
    test_user_group = Group(name='test_user_group')
    created_group = await Group.create(test_user_group)
    
    test_user = User(
        email='test_user',
        password='test_password',
        group_id=created_group.id
    )
    
    # 测试增 Create
    created_user = await User.create(test_user)
    
    # 验证用户是否存在
    assert created_user.id is not None
    assert created_user.email == 'test_user'
    assert created_user.password == 'test_password'
    assert created_user.group_id == created_group.id
    
    # 测试查 Read
    fetched_user = await User.get(id=created_user.id)
    
    assert fetched_user is not None
    assert fetched_user.email == 'test_user'
    assert fetched_user.password == 'test_password'
    assert fetched_user.group_id == created_group.id
    
    # 测试改 Update
    updated_user = await User.update(
        id=fetched_user.id,
        email='updated_user',
        password='updated_password'
    )
    
    assert updated_user is not None
    assert updated_user.email == 'updated_user'
    assert updated_user.password == 'updated_password'
    
    # 测试删除 Delete
    await User.delete(id=updated_user.id)
    deleted_user = await User.get(id=updated_user.id)
    
    assert deleted_user is None