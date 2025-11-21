from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, computed_field


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


class SubsecionalInfo(BaseModel):
    subsecional_id: int
    nome: str

    class Config:
        from_attributes = True


class UnidadeInfo(BaseModel):
    unidade_id: int
    nome: str

    class Config:
        from_attributes = True


class SalaCoworkingInfo(BaseModel):
    coworking_id: int
    nome_da_sala: str

    class Config:
        from_attributes = True


class SessaoResponse(SessaoBase):
    sessao_id: int
    sala_coworking: Optional[SalaCoworkingInfo] = None
    unidade: Optional[UnidadeInfo] = None
    subsecional: Optional[SubsecionalInfo] = None

    class Config:
        from_attributes = True

