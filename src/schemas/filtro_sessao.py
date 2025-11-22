from typing import Optional, Union
from datetime import date, datetime, time
from enum import Enum
from pydantic import BaseModel, Field, model_validator


class OrdenacaoData(str, Enum):
    """Opções de ordenação por data"""
    MAIS_RECENTE_PRIMEIRO = "mais_recente"  # Mais recente primeiro (DESC)
    MAIS_ANTIGA_PRIMEIRO = "mais_antiga"    # Mais antiga primeiro (ASC)


class FiltroSessao(BaseModel):
    """Filtros para listagem de sessões"""
    skip: int = 0
    limit: int = 100
    administrador_id: Optional[int] = None
    data_especifica: Optional[date] = Field(None, description="Filtrar por data >= data informada (deve ser usada junto com inicio/finalizacao)")
    inicio: Optional[datetime] = Field(None, description="Hora de início (DateTime) - usar junto com data_especifica")
    finalizacao: Optional[datetime] = Field(None, description="Hora de finalização (DateTime) - usar junto com data_especifica")
    ip_computador: Optional[str] = None  # Busca parcial no IP do computador (string)
    apenas_ativas: Optional[bool] = None  # Apenas sessões ativas (True) ou todas (False/None)
    ordenar_por_data: Optional[OrdenacaoData] = OrdenacaoData.MAIS_RECENTE_PRIMEIRO
    
    @model_validator(mode='after')
    def validar_inicio_finalizacao_com_data(self):
        """Valida que inicio e finalizacao sejam usados apenas com data_especifica"""
        if (self.inicio is not None or self.finalizacao is not None) and self.data_especifica is None:
            raise ValueError("Os campos 'inicio' e 'finalizacao' devem ser usados junto com 'data_especifica'")
        return self

