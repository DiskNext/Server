from typing import Optional
from sqlmodel import SQLModel, Field

class BaseModel(SQLModel):
    __abstract__ = True
    
    id: Optional[int] = Field(default=None, primary_key=True, description="主键ID")