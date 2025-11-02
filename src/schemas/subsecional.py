from typing import Optional
from pydantic import BaseModel


class SubsecionalBase(BaseModel):
    nome: str


class SubsecionalCreate(SubsecionalBase):
    pass


class SubsecionalUpdate(BaseModel):
    nome: Optional[str] = None


class SubsecionalResponse(SubsecionalBase):
    subsecional_id: int

    class Config:
        from_attributes = True

