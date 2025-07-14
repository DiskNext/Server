import pytest

@pytest.mark.asyncio
async def test_user_curd():
    """测试数据库的增删改查"""
    from models import database
    from models.group import Group
    from models.user import User
    
    await database.init_db(url='sqlite:///:memory:')
    
    # 新建一个测试用户组
    test_group = Group(name='test_group')
    created_group = await Group.create(test_group)
    
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