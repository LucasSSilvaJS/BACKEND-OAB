from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel


class SessaoBase(BaseModel):
    data: date
    inicio_de_sessao: datetime
    final_de_sessao: Optional[datetime] = None
    ativado: bool = True
    computador_id: int
    usuario_id: int
    administrador_id: int


class SessaoCreate(SessaoBase):
    analista_ids: Optional[List[int]] = None


class SessaoUpdate(BaseModel):
    data: Optional[date] = None
    inicio_de_sessao: Optional[datetime] = None
    final_de_sessao: Optional[datetime] = None
    ativado: Optional[bool] = None
    computador_id: Optional[int] = None
    usuario_id: Optional[int] = None
    administrador_id: Optional[int] = None
    analista_ids: Optional[List[int]] = None


class SessaoResponse(SessaoBase):
    sessao_id: int

    class Config:
        from_attributes = True

