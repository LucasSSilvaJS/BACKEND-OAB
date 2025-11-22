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
    
    **Dados retornados:**
    - Número de sessões ativas
    - Total de sessões
    - Pico de acesso (horário e data com mais sessões)
    - Sala coworking mais utilizada (na unidade/subseccional)
    - Frequência de uso de computadores por mês
    
    **Validações:**
    - Todos os filtros são obrigatórios
    - A unidade deve pertencer à subseccional informada
    - A sala coworking deve pertencer à unidade e subseccional informadas
    """,
)
def obter_dashboard(
    subsecional_id: int = Query(..., description="ID da subseccional (obrigatório)"),
    unidade_id: int = Query(..., description="ID da unidade (obrigatório)"),
    coworking_id: int = Query(..., description="ID da sala coworking (obrigatório)"),
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Retorna os dados do dashboard com base nos filtros hierárquicos.
    
    - **subsecional_id**: ID da subseccional (obrigatório)
    - **unidade_id**: ID da unidade que pertence à subseccional (obrigatório)
    - **coworking_id**: ID da sala coworking que pertence à unidade (obrigatório)
    
    Todos os três parâmetros são obrigatórios e devem estar relacionados corretamente.
    """
    filtros = DashboardFiltros(
        subsecional_id=subsecional_id,
        unidade_id=unidade_id,
        coworking_id=coworking_id
    )
    
    service = DashboardService(db)
    return service.obter_dados_dashboard(filtros)

