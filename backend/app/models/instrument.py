from typing import Optional
from sqlmodel import SQLModel, Field


class Instrument(SQLModel, table=True):
    __tablename__ = "instruments"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(max_length=20, unique=True)
    name: str = Field(max_length=100)
    asset_class: str = Field(max_length=20)
    is_active: bool = Field(default=True)
