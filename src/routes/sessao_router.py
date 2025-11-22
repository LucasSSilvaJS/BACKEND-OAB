from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.routes.auth_dependencies import require_any_user, AuthUser
from src.schemas.sessao import SessaoCreate, SessaoUpdate, SessaoResponse
from src.schemas.comum import MensagemResponse
from src.schemas.filtro_sessao import FiltroSessao, OrdenacaoData
from src.services.sessao_service import SessaoService

router = APIRouter(
    prefix="/sessoes",
    tags=["Sessões"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post(
    "",
    response_model=SessaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova sessão",
    description="Cria uma nova sessão de uso de computador. O computador deve estar disponível.",
    response_description="Sessão criada com sucesso",
)
def criar_sessao(
    sessao: SessaoCreate,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Cria uma nova sessão de uso de computador.

    - **data**: Data da sessão
    - **inicio_de_sessao**: Data e hora de início da sessão
    - **final_de_sessao**: Data e hora de término (opcional, preenchido ao finalizar)
    - **ativado**: Status da sessão (padrão: True)
    - **computador_id**: ID do computador a ser usado
    - **usuario_id**: ID do usuário advogado
    - **administrador_id**: ID do administrador responsável
    - **analista_ids**: Lista de IDs dos analistas de TI (opcional)
    """
    service = SessaoService(db)
    return service.criar_sessao(sessao)


@router.get(
    "",
    response_model=List[SessaoResponse],
    summary="Listar sessões com filtros avançados",
    description="""
    Retorna uma lista paginada de sessões com sistema robusto de filtros.
    
    **Filtros disponíveis:**
    - Paginação (skip, limit)
    - Administrador
    - Data de início (intervalo)
    - Data de finalização (intervalo)
    - Data específica
    - IP do computador (busca parcial)
    - Apenas sessões ativas
    - Ordenação por data (mais recente/antiga primeiro)
    - Ordenação alfabética por nome do usuário
    """,
)
def listar_sessoes(
    skip: int = Query(0, ge=0, description="Número de registros a pular (paginação)"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros (padrão: 100, máx: 1000)"),
    administrador_id: Optional[int] = Query(None, description="Filtrar por ID do administrador"),
    data_inicio_de: Optional[date] = Query(None, description="Filtrar sessões iniciadas a partir desta data (YYYY-MM-DD)"),
    data_inicio_ate: Optional[date] = Query(None, description="Filtrar sessões iniciadas até esta data (YYYY-MM-DD)"),
    data_finalizacao_de: Optional[date] = Query(None, description="Filtrar sessões finalizadas a partir desta data (YYYY-MM-DD)"),
    data_finalizacao_ate: Optional[date] = Query(None, description="Filtrar sessões finalizadas até esta data (YYYY-MM-DD)"),
    data_especifica: Optional[date] = Query(None, description="Filtrar por data específica (YYYY-MM-DD). Prioridade sobre data_inicio"),
    ip_computador: Optional[str] = Query(None, description="Buscar por IP do computador (busca parcial, case-insensitive)"),
    apenas_ativas: Optional[bool] = Query(None, description="Retornar apenas sessões ativas (True) ou todas (False/None)"),
    ordenar_por_data: OrdenacaoData = Query(
        OrdenacaoData.MAIS_RECENTE_PRIMEIRO,
        description="Ordenação por data: 'mais_recente' (DESC) ou 'mais_antiga' (ASC)"
    ),
    ordenar_por_usuario: bool = Query(False, description="Ordenar alfabeticamente por nome do usuário (prioridade sobre ordenar_por_data)"),
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Lista sessões com sistema robusto de filtros e ordenação.
    
    **Exemplos de uso:**
    
    1. Buscar todas as sessões com paginação:
       GET /sessoes?skip=0&limit=50
    
    2. Filtrar por administrador:
       GET /sessoes?administrador_id=1
    
    3. Filtrar por data específica:
       GET /sessoes?data_especifica=2025-11-22
    
    4. Filtrar sessões ativas ordenadas por usuário:
       GET /sessoes?apenas_ativas=true&ordenar_por_usuario=true
    
    5. Buscar por IP do computador:
       GET /sessoes?ip_computador=192.168
    
    6. Filtrar por intervalo de datas de início:
       GET /sessoes?data_inicio_de=2025-11-01&data_inicio_ate=2025-11-30
    
    7. Ordenar da mais antiga para a mais recente:
       GET /sessoes?ordenar_por_data=mais_antiga
    
    **Observações:**
    - Todos os filtros podem ser combinados
    - A ordenação por usuário tem prioridade sobre ordenação por data
    - O filtro 'data_especifica' tem prioridade sobre 'data_inicio_de'/'data_inicio_ate'
    """
    filtros = FiltroSessao(
        skip=skip,
        limit=limit,
        administrador_id=administrador_id,
        data_inicio_de=data_inicio_de,
        data_inicio_ate=data_inicio_ate,
        data_finalizacao_de=data_finalizacao_de,
        data_finalizacao_ate=data_finalizacao_ate,
        data_especifica=data_especifica,
        ip_computador=ip_computador,
        apenas_ativas=apenas_ativas,
        ordenar_por_data=ordenar_por_data,
        ordenar_por_usuario=ordenar_por_usuario
    )
    
    service = SessaoService(db)
    return service.listar_sessoes(filtros)


@router.get(
    "/ativas",
    response_model=List[SessaoResponse],
    summary="Listar sessões ativas",
    description="Retorna todas as sessões que estão atualmente ativas (não finalizadas).",
)
def listar_sessoes_ativas(
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas as sessões que estão atualmente ativas.
    """
    service = SessaoService(db)
    return service.listar_sessoes_ativas()


@router.get(
    "/{sessao_id}",
    response_model=SessaoResponse,
    summary="Obter sessão por ID",
    description="Retorna os detalhes de uma sessão específica pelo seu ID.",
)
def obter_sessao(
    sessao_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Retorna os detalhes de uma sessão específica.

    - **sessao_id**: ID único da sessão
    """
    service = SessaoService(db)
    return service.obter_sessao(sessao_id)


@router.get(
    "/usuario/{usuario_id}",
    response_model=List[SessaoResponse],
    summary="Listar sessões por usuário",
    description="Retorna todas as sessões de um usuário advogado específico.",
)
def listar_sessoes_por_usuario(
    usuario_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas as sessões de um usuário advogado.

    - **usuario_id**: ID do usuário advogado
    """
    service = SessaoService(db)
    return service.listar_sessoes_por_usuario(usuario_id)


@router.get(
    "/data/{data}",
    response_model=List[SessaoResponse],
    summary="Listar sessões por data",
    description="Retorna todas as sessões de uma data específica (formato: YYYY-MM-DD).",
)
def listar_sessoes_por_data(
    data: date,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas as sessões de uma data específica.

    - **data**: Data no formato YYYY-MM-DD
    """
    service = SessaoService(db)
    return service.listar_sessoes_por_data(data)


@router.put(
    "/{sessao_id}",
    response_model=SessaoResponse,
    summary="Atualizar sessão",
    description="Atualiza os dados de uma sessão existente.",
)
def atualizar_sessao(
    sessao_id: int,
    sessao: SessaoUpdate,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de uma sessão.

    - **sessao_id**: ID único da sessão
    - **sessao**: Dados a serem atualizados (campos opcionais)
    """
    service = SessaoService(db)
    return service.atualizar_sessao(sessao_id, sessao)


@router.post(
    "/{sessao_id}/finalizar",
    response_model=SessaoResponse,
    summary="Finalizar sessão",
    description="Finaliza uma sessão ativa, registrando o horário de término e desativando a sessão.",
)
def finalizar_sessao(
    sessao_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Finaliza uma sessão ativa.

    - **sessao_id**: ID único da sessão a ser finalizada
    """
    service = SessaoService(db)
    return service.finalizar_sessao(sessao_id)


@router.post(
    "/{sessao_id}/desativar",
    response_model=SessaoResponse,
    summary="Desativar sessão",
    description="Desativa uma sessão ativa, alterando apenas o atributo ativado para false.",
)
def desativar_sessao(
    sessao_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Desativa uma sessão ativa.

    - **sessao_id**: ID único da sessão a ser desativada
    """
    service = SessaoService(db)
    return service.desativar_sessao(sessao_id)


@router.delete(
    "/{sessao_id}",
    response_model=MensagemResponse,
    summary="Deletar sessão",
    description="Remove uma sessão do sistema. Esta operação é irreversível.",
)
def deletar_sessao(
    sessao_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Deleta uma sessão do sistema.

    - **sessao_id**: ID único da sessão a ser deletada
    """
    service = SessaoService(db)
    service.deletar_sessao(sessao_id)
    return MensagemResponse(mensagem="Sessão deletada com sucesso")

