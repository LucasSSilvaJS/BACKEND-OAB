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
        
        NOTA: Uma sessão ativa é uma sessão que está marcada como ativa no banco.
        Se a sessão tem final_de_sessao preenchido mas ainda está ativada, 
        ela será contada como ativa (pode ser uma inconsistência de dados, 
        mas seguimos o que está no banco).
        
        IMPORTANTE: Sessões ativas são sempre contadas, independente do ano,
        pois uma sessão ativa é uma sessão que está acontecendo AGORA.
        O filtro de ano não se aplica a sessões ativas.
        """
        # Buscar IDs dos computadores da sala
        computadores_ids = [
            comp.computador_id 
            for comp in self.db.query(Computador.computador_id).filter(
                Computador.coworking_id == coworking_id
            ).all()
        ]
        
        if not computadores_ids:
            return 0
        
        # Query usando IN para garantir que encontramos todas as sessões
        # Contar apenas por ativado == True (seguindo o que está no banco)
        query = self.db.query(Sessao).filter(
            Sessao.computador_id.in_(computadores_ids),
            Sessao.ativado == True  # Sessão está ativada (critério principal)
        )
        
        # NOTA: Não filtrar sessões ativas por ano, pois uma sessão ativa
        # é uma sessão que está acontecendo agora, independente de quando começou
        # Também não verificar final_de_sessao, pois se está ativada no banco,
        # deve ser contada como ativa
        
        count = query.count()
        return count

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

