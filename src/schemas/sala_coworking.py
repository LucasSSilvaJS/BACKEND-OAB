from typing import Optional
from pydantic import BaseModel


class SalaCoworkingBase(BaseModel):
    nome_da_sala: str
    subsecional_id: int
    unidade_id: int
    administrador_id: Optional[int] = None


class SalaCoworkingCreate(SalaCoworkingBase):
    pass


class SalaCoworkingUpdate(BaseModel):
    nome_da_sala: Optional[str] = None
    subsecional_id: Optional[int] = None
    unidade_id: Optional[int] = None
    administrador_id: Optional[int] = None


class SalaCoworkingResponse(SalaCoworkingBase):
    coworking_id: int

    class Config:
        from_attributes = True

