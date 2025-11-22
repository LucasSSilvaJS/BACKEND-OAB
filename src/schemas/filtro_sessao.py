from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class OrdenacaoData(str, Enum):
    """Opções de ordenação por data"""
    MAIS_RECENTE_PRIMEIRO = "mais_recente"  # Mais recente primeiro (DESC)
    MAIS_ANTIGA_PRIMEIRO = "mais_antiga"    # Mais antiga primeiro (ASC)


class FiltroSessao(BaseModel):
    """Filtros para listagem de sessões"""
    skip: int = 0
    limit: int = 100
    administrador_id: Optional[int] = None
    datetime_inicio: Optional[datetime] = Field(None, description="DateTime mínimo para filtrar sessões. Retorna sessões com inicio_de_sessao >= datetime_inicio")
    ip_computador: Optional[str] = None  # Busca parcial no IP do computador (string)
    apenas_ativas: Optional[bool] = None  # Apenas sessões ativas (True) ou todas (False/None)
    ordenar_por_data: Optional[OrdenacaoData] = OrdenacaoData.MAIS_RECENTE_PRIMEIRO

