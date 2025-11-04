from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.routes.auth_dependencies import require_any_user, AuthUser
from src.schemas.computador import ComputadorCreate, ComputadorUpdate, ComputadorResponse
from src.schemas.comum import MensagemResponse
from src.services.computador_service import ComputadorService

router = APIRouter(
    prefix="/computadores",
    tags=["Computadores"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post(
    "",
    response_model=ComputadorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo computador",
    description="Cria um novo computador no sistema. O IP e número de tombamento devem ser únicos.",
    response_description="Computador criado com sucesso",
)
def criar_computador(
    computador: ComputadorCreate,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Cria um novo computador no sistema.

    - **ip_da_maquina**: Endereço IP do computador (deve ser único)
    - **numero_de_tombamento**: Número de tombamento do computador (deve ser único)
    - **coworking_id**: ID da sala de coworking onde o computador está localizado (opcional)
    """
    service = ComputadorService(db)
    return service.criar_computador(computador)


@router.get(
    "",
    response_model=List[ComputadorResponse],
    summary="Listar computadores",
    description="Retorna uma lista paginada de todos os computadores cadastrados no sistema.",
)
def listar_computadores(
    skip: int = 0,
    limit: int = 100,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos os computadores com paginação.

    - **skip**: Número de registros a pular (para paginação)
    - **limit**: Número máximo de registros a retornar (padrão: 100)
    """
    service = ComputadorService(db)
    return service.listar_computadores(skip=skip, limit=limit)


@router.get(
    "/{computador_id}",
    response_model=ComputadorResponse,
    summary="Obter computador por ID",
    description="Retorna os detalhes de um computador específico pelo seu ID.",
)
def obter_computador(
    computador_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Retorna os detalhes de um computador específico.

    - **computador_id**: ID único do computador
    """
    service = ComputadorService(db)
    return service.obter_computador(computador_id)


@router.get(
    "/coworking/{coworking_id}",
    response_model=List[ComputadorResponse],
    summary="Listar computadores por sala",
    description="Retorna todos os computadores de uma sala de coworking específica.",
)
def listar_computadores_por_coworking(
    coworking_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos os computadores de uma sala de coworking.

    - **coworking_id**: ID da sala de coworking
    """
    service = ComputadorService(db)
    return service.listar_computadores_por_coworking(coworking_id)


@router.put(
    "/{computador_id}",
    response_model=ComputadorResponse,
    summary="Atualizar computador",
    description="Atualiza os dados de um computador existente.",
)
def atualizar_computador(
    computador_id: int,
    computador: ComputadorUpdate,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de um computador.

    - **computador_id**: ID único do computador
    - **computador**: Dados a serem atualizados (campos opcionais)
    """
    service = ComputadorService(db)
    return service.atualizar_computador(computador_id, computador)


@router.delete(
    "/{computador_id}",
    response_model=MensagemResponse,
    summary="Deletar computador",
    description="Remove um computador do sistema. Esta operação é irreversível.",
)
def deletar_computador(
    computador_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Deleta um computador do sistema.

    - **computador_id**: ID único do computador a ser deletado
    """
    service = ComputadorService(db)
    service.deletar_computador(computador_id)
    return MensagemResponse(mensagem="Computador deletado com sucesso")

