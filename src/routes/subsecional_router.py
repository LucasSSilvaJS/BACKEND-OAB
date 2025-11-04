from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.routes.auth_dependencies import require_any_user, AuthUser
from src.schemas.subsecional import SubsecionalCreate, SubsecionalUpdate, SubsecionalResponse
from src.schemas.comum import MensagemResponse
from src.services.subsecional_service import SubsecionalService

router = APIRouter(
    prefix="/subsecionais",
    tags=["Subsecionais"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post(
    "",
    response_model=SubsecionalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova subsecional",
    description="Cria uma nova subsecional no sistema. O nome deve ser único.",
    response_description="Subsecional criada com sucesso",
)
def criar_subsecional(
    subsecional: SubsecionalCreate,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Cria uma nova subsecional no sistema.

    - **nome**: Nome da subsecional (deve ser único)
    """
    service = SubsecionalService(db)
    return service.criar_subsecional(subsecional)


@router.get(
    "",
    response_model=List[SubsecionalResponse],
    summary="Listar subsecionais",
    description="Retorna uma lista paginada de todas as subsecionais cadastradas no sistema.",
)
def listar_subsecionais(
    skip: int = 0,
    limit: int = 100,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas as subsecionais com paginação.

    - **skip**: Número de registros a pular (para paginação)
    - **limit**: Número máximo de registros a retornar (padrão: 100)
    """
    service = SubsecionalService(db)
    return service.listar_subsecionais(skip=skip, limit=limit)


@router.get(
    "/{subsecional_id}",
    response_model=SubsecionalResponse,
    summary="Obter subsecional por ID",
    description="Retorna os detalhes de uma subsecional específica pelo seu ID.",
)
def obter_subsecional(
    subsecional_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Retorna os detalhes de uma subsecional específica.

    - **subsecional_id**: ID único da subsecional
    """
    service = SubsecionalService(db)
    return service.obter_subsecional(subsecional_id)


@router.put(
    "/{subsecional_id}",
    response_model=SubsecionalResponse,
    summary="Atualizar subsecional",
    description="Atualiza os dados de uma subsecional existente.",
)
def atualizar_subsecional(
    subsecional_id: int,
    subsecional: SubsecionalUpdate,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de uma subsecional.

    - **subsecional_id**: ID único da subsecional
    - **subsecional**: Dados a serem atualizados (campos opcionais)
    """
    service = SubsecionalService(db)
    return service.atualizar_subsecional(subsecional_id, subsecional)


@router.delete(
    "/{subsecional_id}",
    response_model=MensagemResponse,
    summary="Deletar subsecional",
    description="Remove uma subsecional do sistema. Esta operação é irreversível.",
)
def deletar_subsecional(
    subsecional_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Deleta uma subsecional do sistema.

    - **subsecional_id**: ID único da subsecional a ser deletada
    """
    service = SubsecionalService(db)
    service.deletar_subsecional(subsecional_id)
    return MensagemResponse(mensagem="Subsecional deletada com sucesso")

