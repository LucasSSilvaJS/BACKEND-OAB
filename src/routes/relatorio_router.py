from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.routes.auth_dependencies import require_analista, AuthUser
from src.schemas.relatorio import RelatorioRequest, RelatorioResponse
from src.services.relatorio_service import RelatorioService

router = APIRouter(
    prefix="/relatorios",
    tags=["Relatórios"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post(
    "/gerar",
    response_model=RelatorioResponse,
    summary="Gerar relatório de uso de sala coworking",
    description="""
    Gera um relatório detalhado em Markdown sobre o uso de uma sala de coworking usando IA (Google Gemini).
    
    **EXCLUSIVO PARA ANALISTAS DE TI**
    
    O relatório inclui:
    - Análise de sessões ativas e históricas
    - Identificação de padrões de uso
    - Picos de acesso
    - Frequência mensal de utilização
    - Recomendações para otimização
    
    **Parâmetros obrigatórios:**
    - subsecional_id: ID da subseccional
    - unidade_id: ID da unidade (deve pertencer à subseccional)
    - coworking_id: ID da sala coworking (deve pertencer à unidade)
    
    **Configuração necessária:**
    - Variável de ambiente GEMINI_API_KEY deve estar configurada no arquivo .env
    """,
)
def gerar_relatorio(
    request: RelatorioRequest,
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
    """
    Gera um relatório completo em Markdown sobre o uso de uma sala de coworking.
    
    **Acesso restrito:** Apenas analistas de TI podem gerar relatórios.
    
    - **subsecional_id**: ID da subseccional
    - **unidade_id**: ID da unidade que pertence à subseccional
    - **coworking_id**: ID da sala coworking que pertence à unidade
    
    O relatório é gerado usando Inteligência Artificial (Google Gemini) e inclui:
    - Sumário executivo
    - Análise detalhada de métricas
    - Identificação de padrões e tendências
    - Recomendações práticas de otimização
    - Conclusões baseadas em dados
    """
    service = RelatorioService(db)
    return service.gerar_relatorio(request, current_user.nome)

