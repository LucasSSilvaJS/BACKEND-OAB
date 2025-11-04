from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.routes.auth_dependencies import require_any_user, AuthUser
from src.schemas.unidade import UnidadeCreate, UnidadeUpdate, UnidadeResponse
from src.schemas.comum import MensagemResponse
from src.services.unidade_service import UnidadeService

router = APIRouter(
    prefix="/unidades",
    tags=["Unidades"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post(
    "",
    response_model=UnidadeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova unidade",
    description="Cria uma nova unidade no sistema. Deve estar vinculada a uma subsecional válida.",
    response_description="Unidade criada com sucesso",
)
def criar_unidade(
    unidade: UnidadeCreate,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Cria uma nova unidade no sistema.

    - **nome**: Nome da unidade
    - **hierarquia**: Hierarquia da unidade (SEDE ou FILIAL)
    - **endereco**: Endereço da unidade (opcional)
    - **latitude**: Latitude geográfica (opcional)
    - **longitude**: Longitude geográfica (opcional)
    - **subsecional_id**: ID da subsecional à qual a unidade pertence
    """
    service = UnidadeService(db)
    return service.criar_unidade(unidade)


@router.get(
    "",
    response_model=List[UnidadeResponse],
    summary="Listar unidades",
    description="Retorna uma lista paginada de todas as unidades cadastradas no sistema.",
)
def listar_unidades(
    skip: int = 0,
    limit: int = 100,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas as unidades com paginação.

    - **skip**: Número de registros a pular (para paginação)
    - **limit**: Número máximo de registros a retornar (padrão: 100)
    """
    service = UnidadeService(db)
    return service.listar_unidades(skip=skip, limit=limit)


@router.get(
    "/{unidade_id}",
    response_model=UnidadeResponse,
    summary="Obter unidade por ID",
    description="Retorna os detalhes de uma unidade específica pelo seu ID.",
)
def obter_unidade(
    unidade_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Retorna os detalhes de uma unidade específica.

    - **unidade_id**: ID único da unidade
    """
    service = UnidadeService(db)
    return service.obter_unidade(unidade_id)


@router.get(
    "/subsecional/{subsecional_id}",
    response_model=List[UnidadeResponse],
    summary="Listar unidades por subsecional",
    description="Retorna todas as unidades de uma subsecional específica.",
)
def listar_unidades_por_subsecional(
    subsecional_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas as unidades de uma subsecional.

    - **subsecional_id**: ID da subsecional
    """
    service = UnidadeService(db)
    return service.listar_unidades_por_subsecional(subsecional_id)


@router.put(
    "/{unidade_id}",
    response_model=UnidadeResponse,
    summary="Atualizar unidade",
    description="Atualiza os dados de uma unidade existente.",
)
def atualizar_unidade(
    unidade_id: int,
    unidade: UnidadeUpdate,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de uma unidade.

    - **unidade_id**: ID único da unidade
    - **unidade**: Dados a serem atualizados (campos opcionais)
    """
    service = UnidadeService(db)
    return service.atualizar_unidade(unidade_id, unidade)


@router.delete(
    "/{unidade_id}",
    response_model=MensagemResponse,
    summary="Deletar unidade",
    description="Remove uma unidade do sistema. Esta operação é irreversível.",
)
def deletar_unidade(
    unidade_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Deleta uma unidade do sistema.

    - **unidade_id**: ID único da unidade a ser deletada
    """
    service = UnidadeService(db)
    service.deletar_unidade(unidade_id)
    return MensagemResponse(mensagem="Unidade deletada com sucesso")

