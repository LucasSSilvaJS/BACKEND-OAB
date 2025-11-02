from typing import Optional
from pydantic import BaseModel


class ComputadorBase(BaseModel):
    ip_da_maquina: str
    numero_de_tombamento: str
    coworking_id: Optional[int] = None


class ComputadorCreate(ComputadorBase):
    pass


class ComputadorUpdate(BaseModel):
    ip_da_maquina: Optional[str] = None
    numero_de_tombamento: Optional[str] = None
    coworking_id: Optional[int] = None


class ComputadorResponse(ComputadorBase):
    computador_id: int

    class Config:
        from_attributes = True

