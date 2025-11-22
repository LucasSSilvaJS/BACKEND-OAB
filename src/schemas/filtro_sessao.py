from typing import Optional
from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel


class OrdenacaoData(str, Enum):
    """Opções de ordenação por data"""
    MAIS_RECENTE_PRIMEIRO = "mais_recente"  # Mais recente primeiro (DESC)
    MAIS_ANTIGA_PRIMEIRO = "mais_antiga"    # Mais antiga primeiro (ASC)


class FiltroSessao(BaseModel):
    """Filtros para listagem de sessões"""
    skip: int = 0
    limit: int = 100
    administrador_id: Optional[int] = None
    computador_id: Optional[int] = None  # Filtrar por ID do computador
    usuario_id: Optional[int] = None  # Filtrar por ID do usuário
    inicio_de: Optional[datetime] = None  # Hora de início >= (DateTime)
    inicio_ate: Optional[datetime] = None  # Hora de início <= (DateTime)
    finalizacao_de: Optional[datetime] = None  # Hora de finalização >= (DateTime)
    finalizacao_ate: Optional[datetime] = None  # Hora de finalização <= (DateTime)
    data_especifica: Optional[date] = None  # Filtro por data específica (campo 'data')
    ip_computador: Optional[str] = None  # Busca parcial no IP do computador
    apenas_ativas: Optional[bool] = None  # Apenas sessões ativas (ativado=True e final_de_sessao IS NULL)
    apenas_inativas: Optional[bool] = None  # Apenas sessões inativas (ativado=False OU final_de_sessao IS NOT NULL)
    ordenar_por_data: Optional[OrdenacaoData] = OrdenacaoData.MAIS_RECENTE_PRIMEIRO
    ordenar_por_usuario: Optional[bool] = False  # Ordenar alfabeticamente por nome do usuário

