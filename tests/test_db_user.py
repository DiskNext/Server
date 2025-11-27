import pytest

@pytest.mark.asyncio
async def test_user_curd():
    """测试数据库的增删改查"""
    from models import database, migration
    from models.group import Group
    from models.user import User

    await database.init_db(url='sqlite+aiosqlite:///:memory:')

    await migration.migration()

    async for session in database.get_session():
        # 新建一个测试用户组
        test_user_group = Group(name='test_user_group')
        created_group = await test_user_group.save(session)

        test_user = User(
            username='test_user',
            password='test_password',
            group_id=created_group.id
        )

        # 测试增 Create
        created_user = await test_user.save(session)

        # 验证用户是否存在
        assert created_user.id is not None
        assert created_user.username == 'test_user'
        assert created_user.password == 'test_password'
        assert created_user.group_id == created_group.id

        # 测试查 Read
        fetched_user = await User.get(session, User.id == created_user.id)

        assert fetched_user is not None
        assert fetched_user.username == 'test_user'
        assert fetched_user.password == 'test_password'
        assert fetched_user.group_id == created_group.id

        # 测试改 Update
        updated_user = await fetched_user.update(
            session,
            {"username": "updated_user", "password": "updated_password"}
        )

        assert updated_user is not None
        assert updated_user.username == 'updated_user'
        assert updated_user.password == 'updated_password'

        # 测试删除 Delete
        await updated_user.delete(session)
        deleted_user = await User.get(session, User.id == updated_user.id)

        assert deleted_user is None
        break
