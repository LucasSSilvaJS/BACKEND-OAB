from pydantic import BaseModel, Field


class RelatorioRequest(BaseModel):
    subsecional_id: int = Field(..., description="ID da subseccional")
    unidade_id: int = Field(..., description="ID da unidade")
    coworking_id: int = Field(..., description="ID da sala coworking")


class RelatorioResponse(BaseModel):
    markdown: str = Field(..., description="Relatório em formato Markdown")
    subsecional_nome: str
    unidade_nome: str
    coworking_nome: str
    gerado_por: str = Field(..., description="Nome do analista que gerou o relatório")

