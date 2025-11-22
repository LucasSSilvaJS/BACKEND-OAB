from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.routes.auth_dependencies import require_any_user, AuthUser
from src.schemas.dashboard import DashboardFiltros, DashboardResponse
from src.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    responses={404: {"description": "Não encontrado"}},
)


@router.get(
    "",
    response_model=DashboardResponse,
    summary="Obter dados do dashboard",
    description="""
    Obtém os dados do dashboard com base nos filtros hierárquicos.
    
    **Filtros obrigatórios (hierárquicos):**
    1. **subsecional_id**: ID da subseccional
    2. **unidade_id**: ID da unidade (deve pertencer à subseccional)
    3. **coworking_id**: ID da sala coworking (deve pertencer à unidade e subseccional)
    
    **Filtros:**
    - **subsecional_id**: ID da subseccional (obrigatório)
    - **unidade_id**: ID da unidade (obrigatório)
    - **coworking_id**: ID da sala coworking (obrigatório)
    - **ano**: Ano para filtrar os dados (opcional). Se não informado, retorna dados de todos os anos
    
    **Dados retornados:**
    - Número de sessões ativas
    - Total de sessões
    - Pico de acesso (horário e data com mais sessões)
    - Sala coworking mais utilizada (na unidade/subseccional)
    - Frequência de uso de computadores por mês
    
    **Validações:**
    - Os três primeiros filtros são obrigatórios
    - A unidade deve pertencer à subseccional informada
    - A sala coworking deve pertencer à unidade e subseccional informadas
    - O filtro de ano é opcional e filtra todos os dados por ano
    """,
)
def obter_dashboard(
    subsecional_id: int = Query(..., description="ID da subseccional (obrigatório)"),
    unidade_id: int = Query(..., description="ID da unidade (obrigatório)"),
    coworking_id: int = Query(..., description="ID da sala coworking (obrigatório)"),
    ano: Optional[int] = Query(None, description="Ano para filtrar os dados (opcional). Ex: 2025. Se não informado, retorna dados de todos os anos"),
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Retorna os dados do dashboard com base nos filtros hierárquicos.
    
    - **subsecional_id**: ID da subseccional (obrigatório)
    - **unidade_id**: ID da unidade que pertence à subseccional (obrigatório)
    - **coworking_id**: ID da sala coworking que pertence à unidade (obrigatório)
    - **ano**: Ano para filtrar os dados (opcional). Se não informado, retorna dados de todos os anos
    
    Todos os três primeiros parâmetros são obrigatórios e devem estar relacionados corretamente.
    """
    filtros = DashboardFiltros(
        subsecional_id=subsecional_id,
        unidade_id=unidade_id,
        coworking_id=coworking_id,
        ano=ano
    )
    
    service = DashboardService(db)
    return service.obter_dados_dashboard(filtros)

