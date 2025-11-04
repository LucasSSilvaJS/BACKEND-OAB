from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.routes.auth_dependencies import require_any_user, AuthUser
from src.schemas.analista_de_ti import AnalistaTCreate, AnalistaTUpdate, AnalistaTResponse
from src.schemas.comum import MensagemResponse
from src.services.analista_ti_service import AnalistaTIService

router = APIRouter(
    prefix="/analistas-ti",
    tags=["Analistas de TI"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post(
    "",
    response_model=AnalistaTResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo analista de TI",
    description="Cria um novo analista de TI no sistema. O usuário deve ser único e o cadastro deve existir.",
    response_description="Analista de TI criado com sucesso",
)
def criar_analista(
    analista: AnalistaTCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo analista de TI no sistema.

    - **usuario**: Nome de usuário do analista (deve ser único)
    - **senha**: Senha do analista (será hashada automaticamente)
    - **cadastro_id**: ID do cadastro associado ao analista
    """
    service = AnalistaTIService(db)
    return service.criar_analista(analista)


@router.get(
    "",
    response_model=List[AnalistaTResponse],
    summary="Listar analistas de TI",
    description="Retorna uma lista paginada de todos os analistas de TI cadastrados no sistema.",
)
def listar_analistas(
    skip: int = 0,
    limit: int = 100,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos os analistas de TI com paginação.

    - **skip**: Número de registros a pular (para paginação)
    - **limit**: Número máximo de registros a retornar (padrão: 100)
    """
    service = AnalistaTIService(db)
    return service.listar_analistas(skip=skip, limit=limit)


@router.get(
    "/{analista_id}",
    response_model=AnalistaTResponse,
    summary="Obter analista de TI por ID",
    description="Retorna os detalhes de um analista de TI específico pelo seu ID.",
)
def obter_analista(
    analista_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Retorna os detalhes de um analista de TI específico.

    - **analista_id**: ID único do analista de TI
    """
    service = AnalistaTIService(db)
    return service.obter_analista(analista_id)


@router.put(
    "/{analista_id}",
    response_model=AnalistaTResponse,
    summary="Atualizar analista de TI",
    description="Atualiza os dados de um analista de TI existente.",
)
def atualizar_analista(
    analista_id: int,
    analista: AnalistaTUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de um analista de TI.

    - **analista_id**: ID único do analista de TI
    - **analista**: Dados a serem atualizados (campos opcionais)
    """
    service = AnalistaTIService(db)
    return service.atualizar_analista(analista_id, analista)


@router.delete(
    "/{analista_id}",
    response_model=MensagemResponse,
    summary="Deletar analista de TI",
    description="Remove um analista de TI do sistema. Esta operação é irreversível.",
)
def deletar_analista(
    analista_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Deleta um analista de TI do sistema.

    - **analista_id**: ID único do analista de TI a ser deletado
    """
    service = AnalistaTIService(db)
    service.deletar_analista(analista_id)
    return MensagemResponse(mensagem="Analista de TI deletado com sucesso")

