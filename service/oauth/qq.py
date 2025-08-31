from pydantic import BaseModel
import aiohttp

async def get_access_token(
    code: str
)