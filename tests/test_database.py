from models import database

import pytest

@pytest.mark.asyncio
async def test_initialize_db():
    """Fixture to initialize the database before tests."""
    await database.init_db()