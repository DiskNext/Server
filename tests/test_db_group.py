import pytest

@pytest.mark.asyncio
async def test_group_curd():
    """测试数据库的增删改查"""
    from models import database, migration
    from models.group import Group

    await database.init_db(url='sqlite+aiosqlite:///:memory:')

    await migration.migration()

    async for session in database.get_session():
        # 测试增 Create
        test_group = Group(name='test_group')
        created_group = await test_group.save(session)

        assert created_group is not None
        assert created_group.id is not None
        assert created_group.name == 'test_group'

        # 测试查 Read
        fetched_group = await Group.get(session, Group.id == created_group.id)
        assert fetched_group is not None
        assert fetched_group.id == created_group.id
        assert fetched_group.name == 'test_group'

        # 测试更新 Update
        updated_group = await fetched_group.update(session, {"name": "updated_group"})

        assert updated_group is not None
        assert updated_group.id == fetched_group.id
        assert updated_group.name == 'updated_group'

        # 测试删除 Delete
        await updated_group.delete(session)
        deleted_group = await Group.get(session, Group.id == updated_group.id)
        assert deleted_group is None
        break
