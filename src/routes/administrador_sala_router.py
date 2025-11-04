from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.routes.auth_dependencies import require_any_user, AuthUser
from src.schemas.administrador_sala import (
    AdministradorSalaCreate,
    AdministradorSalaUpdate,
    AdministradorSalaResponse
)
from src.schemas.comum import MensagemResponse
from src.services.administrador_sala_service import AdministradorSalaService

router = APIRouter(
    prefix="/administradores-sala",
    tags=["Administradores de Sala"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post(
    "",
    response_model=AdministradorSalaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo administrador de sala",
    description="Cria um novo administrador de sala no sistema. O usuário deve ser único e o cadastro deve existir.",
    response_description="Administrador de sala criado com sucesso",
)
def criar_administrador(
    administrador: AdministradorSalaCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo administrador de sala no sistema.

    - **usuario**: Nome de usuário do administrador (deve ser único)
    - **senha**: Senha do administrador (será hashada automaticamente)
    - **adm_local**: Se é administrador local (padrão: False)
    - **admin_central**: Se é administrador central (padrão: False)
    - **cadastro_id**: ID do cadastro associado ao administrador
    """
    service = AdministradorSalaService(db)
    return service.criar_administrador(administrador)


@router.get(
    "",
    response_model=List[AdministradorSalaResponse],
    summary="Listar administradores de sala",
    description="Retorna uma lista paginada de todos os administradores de sala cadastrados no sistema.",
)
def listar_administradores(
    skip: int = 0,
    limit: int = 100,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos os administradores de sala com paginação.

    - **skip**: Número de registros a pular (para paginação)
    - **limit**: Número máximo de registros a retornar (padrão: 100)
    """
    service = AdministradorSalaService(db)
    return service.listar_administradores(skip=skip, limit=limit)


@router.get(
    "/{admin_id}",
    response_model=AdministradorSalaResponse,
    summary="Obter administrador de sala por ID",
    description="Retorna os detalhes de um administrador de sala específico pelo seu ID.",
)
def obter_administrador(
    admin_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Retorna os detalhes de um administrador de sala específico.

    - **admin_id**: ID único do administrador de sala
    """
    service = AdministradorSalaService(db)
    return service.obter_administrador(admin_id)


@router.put(
    "/{admin_id}",
    response_model=AdministradorSalaResponse,
    summary="Atualizar administrador de sala",
    description="Atualiza os dados de um administrador de sala existente.",
)
def atualizar_administrador(
    admin_id: int,
    administrador: AdministradorSalaUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de um administrador de sala.

    - **admin_id**: ID único do administrador de sala
    - **administrador**: Dados a serem atualizados (campos opcionais)
    """
    service = AdministradorSalaService(db)
    return service.atualizar_administrador(admin_id, administrador)


@router.delete(
    "/{admin_id}",
    response_model=MensagemResponse,
    summary="Deletar administrador de sala",
    description="Remove um administrador de sala do sistema. Esta operação é irreversível.",
)
def deletar_administrador(
    admin_id: int,
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    """
    Deleta um administrador de sala do sistema.

    - **admin_id**: ID único do administrador de sala a ser deletado
    """
    service = AdministradorSalaService(db)
    service.deletar_administrador(admin_id)
    return MensagemResponse(mensagem="Administrador de sala deletado com sucesso")

