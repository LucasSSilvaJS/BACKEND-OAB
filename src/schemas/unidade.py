from typing import Optional
from pydantic import BaseModel
from src.entities.unidade import HierarquiaEnum


class UnidadeBase(BaseModel):
    nome: str
    hierarquia: HierarquiaEnum
    endereco: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    subsecional_id: int


class UnidadeCreate(UnidadeBase):
    pass


class UnidadeUpdate(BaseModel):
    nome: Optional[str] = None
    hierarquia: Optional[HierarquiaEnum] = None
    endereco: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    subsecional_id: Optional[int] = None


class UnidadeResponse(UnidadeBase):
    unidade_id: int

    class Config:
        from_attributes = True

