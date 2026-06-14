from typing import Optional
from sqlmodel import Field, SQLModel

class HeroBase(SQLModel):
    name: str = Field(min_length=1, max_length=50)
    age: Optional[int] = Field(default=None, ge=0, le=150)

class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class HeroCreate(HeroBase):
    pass
