from pydantic import BaseModel
import aiohttp

class GithubAccessToken(BaseModel):
    access_token: str
    token_type: str
    scope: str

class GithubUserData(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str | None
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool
    name: str | None
    company: str | None
    blog: str | None
    location: str | None
    email: str | None
    hireable: bool | None
    bio: str | None
    twitter_username: str | None
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: str  # ISO 8601 format date-time string
    updated_at: str  # ISO 8601 format date-time string

class GithubUserInfoResponse(BaseModel):
    code: str
    user_data: GithubUserData

async def get_access_token(code: str) -> GithubAccessToken:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url='https://github.com/login/oauth/access_token',
            params={
                'client_id': '',
                'client_secret': '',
                'code': code
            },
            headers={'accept': 'application/json'},
            proxy='socks5://127.0.0.1:7890'
        ) as access_resp:
            access_data = await access_resp.json()
            return GithubAccessToken(
                access_token=access_data.get('access_token'), 
                token_type=access_data.get('token_type'), 
                scope=access_data.get('scope')
            )

async def get_user_info(access_token: str | GithubAccessToken) -> GithubUserInfoResponse:
    if isinstance(access_token, GithubAccessToken):
        access_token = access_token.access_token
        
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url='https://api.github.com/user', 
            headers={
                'accept': 'application/json',
                'Authorization': f'token {access_token}'},
            proxy='socks5://127.0.0.1:7890'
            ) as resp:
            user_data = await resp.json()
            return GithubUserInfoResponse(**user_data)