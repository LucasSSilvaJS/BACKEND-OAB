from datetime import datetime
from pydantic import BaseModel, Field


class RelatorioRequest(BaseModel):
    subsecional_id: int = Field(..., description="ID da subseccional")
    unidade_id: int = Field(..., description="ID da unidade")
    coworking_id: int = Field(..., description="ID da sala coworking")


class RelatorioResponse(BaseModel):
    markdown: str = Field(..., description="Relatório em formato Markdown")
    subsecional_id: int
    subsecional_nome: str
    unidade_id: int
    unidade_nome: str
    unidade_hierarquia: str
    coworking_id: int
    coworking_nome: str
    gerado_por: str = Field(..., description="Nome do analista que gerou o relatório")
    gerado_por_id: int = Field(..., description="ID do analista que gerou o relatório")
    data_geracao: datetime = Field(..., description="Data e hora da geração do relatório")
    total_sessoes: int = Field(..., description="Total de sessões históricas")
    sessoes_ativas: int = Field(..., description="Sessões ativas no momento")

