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
    data_inicio_de: Optional[date] = None  # Data de início >=
    data_inicio_ate: Optional[date] = None  # Data de início <=
    data_finalizacao_de: Optional[date] = None  # Data de finalização >=
    data_finalizacao_ate: Optional[date] = None  # Data de finalização <=
    data_especifica: Optional[date] = None  # Filtro por data específica
    ip_computador: Optional[str] = None  # Busca parcial no IP
    apenas_ativas: Optional[bool] = None  # Apenas sessões ativas
    ordenar_por_data: Optional[OrdenacaoData] = OrdenacaoData.MAIS_RECENTE_PRIMEIRO
    ordenar_por_usuario: Optional[bool] = False  # Ordenar alfabeticamente por nome do usuário

