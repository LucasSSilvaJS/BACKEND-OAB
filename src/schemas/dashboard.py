from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class DashboardFiltros(BaseModel):
    subsecional_id: int = Field(..., description="ID da subseccional (obrigatório)")
    unidade_id: int = Field(..., description="ID da unidade (obrigatório)")
    coworking_id: int = Field(..., description="ID da sala coworking (obrigatório)")


class PicoAcesso(BaseModel):
    horario: str = Field(..., description="Horário do pico de acesso (HH:MM)")
    data: str = Field(..., description="Data do pico de acesso (DD/MM/YYYY)")
    quantidade: int = Field(..., description="Quantidade de sessões no pico")


class CoworkingMaisUtilizado(BaseModel):
    coworking_id: int
    nome_da_sala: str
    total_sessoes: int


class FrequenciaMensal(BaseModel):
    mes: str = Field(..., description="Nome do mês")
    ano: int = Field(..., description="Ano")
    total_sessoes: int = Field(..., description="Total de sessões no mês")


class DashboardResponse(BaseModel):
    sessoes_ativas: int = Field(..., description="Número de sessões atualmente ativas")
    total_sessoes: int = Field(..., description="Total de sessões (todas)")
    pico_acesso: Optional[PicoAcesso] = Field(None, description="Informações do pico de acesso")
    coworking_mais_utilizado: Optional[CoworkingMaisUtilizado] = Field(None, description="Sala coworking mais utilizada")
    frequencia_mensal: List[FrequenciaMensal] = Field(default_factory=list, description="Frequência de uso por mês")

