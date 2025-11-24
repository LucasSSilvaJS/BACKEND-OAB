from typing import Optional, List, Dict, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, desc
from src.entities.sessao import Sessao
from src.entities.computador import Computador
from src.entities.sala_coworking import Sala_coworking


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def validar_hierarquia(self, subsecional_id: int, unidade_id: int, coworking_id: int) -> bool:
        """Valida se a hierarquia subsecional -> unidade -> coworking está correta"""
        sala = self.db.query(Sala_coworking).filter(
            Sala_coworking.coworking_id == coworking_id,
            Sala_coworking.unidade_id == unidade_id,
            Sala_coworking.subsecional_id == subsecional_id
        ).first()
        return sala is not None

    def contar_sessoes_ativas(self, coworking_id: int, ano: Optional[int] = None) -> int:
        """Conta o número de sessões ativas na sala coworking
        
        Uma sessão é considerada ativa quando:
        - ativado == True
        - final_de_sessao IS NULL (não foi finalizada)
        
        IMPORTANTE: Sessões ativas são sempre contadas, independente do ano,
        pois uma sessão ativa é uma sessão que está acontecendo AGORA.
        O filtro de ano não se aplica a sessões ativas.
        """
        query = self.db.query(Sessao).join(
            Computador, Sessao.computador_id == Computador.computador_id
        ).filter(
            Computador.coworking_id == coworking_id,
            Sessao.ativado == True,
            Sessao.final_de_sessao.is_(None)
        )
        
        # NOTA: Não filtrar sessões ativas por ano, pois uma sessão ativa
        # é uma sessão que está acontecendo agora, independente de quando começou
        
        return query.count()

    def contar_total_sessoes(self, coworking_id: int, ano: Optional[int] = None) -> int:
        """Conta o total de sessões na sala coworking"""
        query = self.db.query(Sessao).join(
            Computador, Sessao.computador_id == Computador.computador_id
        ).filter(
            Computador.coworking_id == coworking_id
        )
        
        if ano is not None:
            query = query.filter(extract('year', Sessao.data) == ano)
        
        return query.count()

    def obter_pico_acesso(self, coworking_id: int, ano: Optional[int] = None) -> Optional[Tuple[datetime, int]]:
        """Obtém o horário de pico de acesso (dia/hora com mais sessões iniciadas)"""
        query = self.db.query(
            func.date_trunc('hour', Sessao.inicio_de_sessao).label('hora'),
            func.count(Sessao.sessao_id).label('quantidade')
        ).join(
            Computador, Sessao.computador_id == Computador.computador_id
        ).filter(
            Computador.coworking_id == coworking_id
        )
        
        if ano is not None:
            query = query.filter(extract('year', Sessao.data) == ano)
        
        resultado = query.group_by(
            func.date_trunc('hour', Sessao.inicio_de_sessao)
        ).order_by(
            desc('quantidade')
        ).first()

        if resultado:
            return (resultado.hora, resultado.quantidade)
        return None

    def obter_coworking_mais_utilizado(self, subsecional_id: int, unidade_id: int, ano: Optional[int] = None) -> Optional[Dict]:
        """Obtém a sala coworking mais utilizada na unidade/subsecional"""
        query = self.db.query(
            Sala_coworking.coworking_id,
            Sala_coworking.nome_da_sala,
            func.count(Sessao.sessao_id).label('total_sessoes')
        ).join(
            Computador, Sala_coworking.coworking_id == Computador.coworking_id
        ).join(
            Sessao, Computador.computador_id == Sessao.computador_id
        ).filter(
            Sala_coworking.subsecional_id == subsecional_id,
            Sala_coworking.unidade_id == unidade_id
        )
        
        if ano is not None:
            query = query.filter(extract('year', Sessao.data) == ano)
        
        resultado = query.group_by(
            Sala_coworking.coworking_id,
            Sala_coworking.nome_da_sala
        ).order_by(
            desc('total_sessoes')
        ).first()

        if resultado:
            return {
                'coworking_id': resultado.coworking_id,
                'nome_da_sala': resultado.nome_da_sala,
                'total_sessoes': resultado.total_sessoes
            }
        return None

    def obter_frequencia_mensal(self, coworking_id: int, ano: Optional[int] = None) -> List[Dict]:
        """Obtém a frequência de uso de computadores por mês"""
        query = self.db.query(
            extract('year', Sessao.data).label('ano'),
            extract('month', Sessao.data).label('mes'),
            func.count(Sessao.sessao_id).label('total_sessoes')
        ).join(
            Computador, Sessao.computador_id == Computador.computador_id
        ).filter(
            Computador.coworking_id == coworking_id
        )
        
        if ano is not None:
            query = query.filter(extract('year', Sessao.data) == ano)
        
        resultados = query.group_by(
            extract('year', Sessao.data),
            extract('month', Sessao.data)
        ).order_by(
            extract('year', Sessao.data),
            extract('month', Sessao.data)
        ).all()

        return [
            {
                'ano': int(r.ano),
                'mes': int(r.mes),
                'total_sessoes': r.total_sessoes
            }
            for r in resultados
        ]

