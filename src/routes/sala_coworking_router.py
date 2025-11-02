from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.schemas.sala_coworking import SalaCoworkingCreate, SalaCoworkingUpdate, SalaCoworkingResponse
from src.schemas.comum import MensagemResponse
from src.services.sala_coworking_service import SalaCoworkingService

router = APIRouter(
    prefix="/salas-coworking",
    tags=["Salas de Coworking"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post(
    "",
    response_model=SalaCoworkingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova sala de coworking",
    description="Cria uma nova sala de coworking no sistema. Deve estar vinculada a uma subsecional e unidade válidas.",
    response_description="Sala de coworking criada com sucesso",
)
def criar_sala(sala: SalaCoworkingCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova sala de coworking no sistema.

    - **nome_da_sala**: Nome da sala de coworking
    - **subsecional_id**: ID da subsecional à qual a sala pertence
    - **unidade_id**: ID da unidade à qual a sala pertence
    - **administrador_id**: ID do administrador responsável pela sala (opcional)
    """
    service = SalaCoworkingService(db)
    return service.criar_sala(sala)


@router.get(
    "",
    response_model=List[SalaCoworkingResponse],
    summary="Listar salas de coworking",
    description="Retorna uma lista paginada de todas as salas de coworking cadastradas no sistema.",
)
def listar_salas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todas as salas de coworking com paginação.

    - **skip**: Número de registros a pular (para paginação)
    - **limit**: Número máximo de registros a retornar (padrão: 100)
    """
    service = SalaCoworkingService(db)
    return service.listar_salas(skip=skip, limit=limit)


@router.get(
    "/{coworking_id}",
    response_model=SalaCoworkingResponse,
    summary="Obter sala por ID",
    description="Retorna os detalhes de uma sala de coworking específica pelo seu ID.",
)
def obter_sala(coworking_id: int, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de uma sala de coworking específica.

    - **coworking_id**: ID único da sala de coworking
    """
    service = SalaCoworkingService(db)
    return service.obter_sala(coworking_id)


@router.get(
    "/subsecional/{subsecional_id}",
    response_model=List[SalaCoworkingResponse],
    summary="Listar salas por subsecional",
    description="Retorna todas as salas de coworking de uma subsecional específica.",
)
def listar_salas_por_subsecional(subsecional_id: int, db: Session = Depends(get_db)):
    """
    Lista todas as salas de coworking de uma subsecional.

    - **subsecional_id**: ID da subsecional
    """
    service = SalaCoworkingService(db)
    return service.listar_salas_por_subsecional(subsecional_id)


@router.get(
    "/unidade/{unidade_id}",
    response_model=List[SalaCoworkingResponse],
    summary="Listar salas por unidade",
    description="Retorna todas as salas de coworking de uma unidade específica.",
)
def listar_salas_por_unidade(unidade_id: int, db: Session = Depends(get_db)):
    """
    Lista todas as salas de coworking de uma unidade.

    - **unidade_id**: ID da unidade
    """
    service = SalaCoworkingService(db)
    return service.listar_salas_por_unidade(unidade_id)


@router.put(
    "/{coworking_id}",
    response_model=SalaCoworkingResponse,
    summary="Atualizar sala de coworking",
    description="Atualiza os dados de uma sala de coworking existente.",
)
def atualizar_sala(
    coworking_id: int,
    sala: SalaCoworkingUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de uma sala de coworking.

    - **coworking_id**: ID único da sala de coworking
    - **sala**: Dados a serem atualizados (campos opcionais)
    """
    service = SalaCoworkingService(db)
    return service.atualizar_sala(coworking_id, sala)


@router.delete(
    "/{coworking_id}",
    response_model=MensagemResponse,
    summary="Deletar sala de coworking",
    description="Remove uma sala de coworking do sistema. Esta operação é irreversível.",
)
def deletar_sala(coworking_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma sala de coworking do sistema.

    - **coworking_id**: ID único da sala de coworking a ser deletada
    """
    service = SalaCoworkingService(db)
    service.deletar_sala(coworking_id)
    return MensagemResponse(mensagem="Sala de coworking deletada com sucesso")

