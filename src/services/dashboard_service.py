from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.dashboard_repository import DashboardRepository
from src.repositories.subsecional_repository import SubsecionalRepository
from src.repositories.unidade_repository import UnidadeRepository
from src.repositories.sala_coworking_repository import SalaCoworkingRepository
from src.schemas.dashboard import DashboardFiltros, DashboardResponse, PicoAcesso, CoworkingMaisUtilizado, FrequenciaMensal


class DashboardService:
    def __init__(self, db: Session):
        self.dashboard_repo = DashboardRepository(db)
        self.subsecional_repo = SubsecionalRepository(db)
        self.unidade_repo = UnidadeRepository(db)
        self.sala_repo = SalaCoworkingRepository(db)

    def _validar_filtros(self, filtros: DashboardFiltros) -> None:
        """Valida se os filtros existem e estão relacionados corretamente"""
        # Validar subseccional
        if not self.subsecional_repo.get_by_id(filtros.subsecional_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subseccional não encontrada. Por favor, selecione uma subseccional válida."
            )
        
        # Validar unidade
        unidade = self.unidade_repo.get_by_id(filtros.unidade_id)
        if not unidade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unidade não encontrada. Por favor, selecione uma unidade válida."
            )
        
        # Verificar se a unidade pertence à subseccional
        if unidade.subsecional_id != filtros.subsecional_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A unidade selecionada não pertence à subseccional informada. Por favor, selecione uma unidade válida."
            )
        
        # Validar sala coworking
        sala = self.sala_repo.get_by_id(filtros.coworking_id)
        if not sala:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sala de coworking não encontrada. Por favor, selecione uma sala válida."
            )
        
        # Verificar se a sala pertence à unidade e subseccional
        if sala.unidade_id != filtros.unidade_id or sala.subsecional_id != filtros.subsecional_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A sala de coworking selecionada não pertence à unidade e subseccional informadas. Por favor, selecione uma sala válida."
            )

    def _nome_mes(self, numero_mes: int) -> str:
        """Converte número do mês para nome em português"""
        meses = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        return meses.get(numero_mes, "Desconhecido")

    def obter_dados_dashboard(self, filtros: DashboardFiltros) -> DashboardResponse:
        """Obtém todos os dados do dashboard com base nos filtros"""
        # Validar filtros
        self._validar_filtros(filtros)

        # Contar sessões ativas
        sessoes_ativas = self.dashboard_repo.contar_sessoes_ativas(filtros.coworking_id, filtros.ano)
        total_sessoes = self.dashboard_repo.contar_total_sessoes(filtros.coworking_id, filtros.ano)

        # Obter pico de acesso
        pico_acesso_data = self.dashboard_repo.obter_pico_acesso(filtros.coworking_id, filtros.ano)
        pico_acesso = None
        if pico_acesso_data:
            hora_pico, quantidade = pico_acesso_data
            pico_acesso = PicoAcesso(
                horario=hora_pico.strftime("%H:%M"),
                data=hora_pico.strftime("%d/%m/%Y"),
                quantidade=quantidade
            )

        # Obter coworking mais utilizado (na mesma subsecional/unidade)
        coworking_mais_utilizado_data = self.dashboard_repo.obter_coworking_mais_utilizado(
            filtros.subsecional_id,
            filtros.unidade_id,
            filtros.ano
        )
        coworking_mais_utilizado = None
        if coworking_mais_utilizado_data:
            coworking_mais_utilizado = CoworkingMaisUtilizado(**coworking_mais_utilizado_data)

        # Obter frequência mensal
        frequencia_data = self.dashboard_repo.obter_frequencia_mensal(filtros.coworking_id, filtros.ano)
        frequencia_mensal = [
            FrequenciaMensal(
                mes=self._nome_mes(item['mes']),
                ano=item['ano'],
                total_sessoes=item['total_sessoes']
            )
            for item in frequencia_data
        ]

        return DashboardResponse(
            sessoes_ativas=sessoes_ativas,
            total_sessoes=total_sessoes,
            pico_acesso=pico_acesso,
            coworking_mais_utilizado=coworking_mais_utilizado,
            frequencia_mensal=frequencia_mensal
        )

