from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.schemas.usuario_advogado import UsuarioAdvogadoCreate, UsuarioAdvogadoUpdate, UsuarioAdvogadoResponse
from src.schemas.comum import MensagemResponse
from src.services.usuario_advogado_service import UsuarioAdvogadoService

router = APIRouter(
    prefix="/usuarios-advogados",
    tags=["Usuários Advogados"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post(
    "",
    response_model=UsuarioAdvogadoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo usuário advogado",
    description="Cria um novo usuário advogado no sistema. O registro OAB deve ser único e o cadastro deve existir.",
    response_description="Usuário advogado criado com sucesso",
)
def criar_usuario(usuario: UsuarioAdvogadoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário advogado no sistema.

    - **registro_oab**: Número de registro na OAB (deve ser único)
    - **codigo_de_seguranca**: Código de segurança do advogado
    - **adimplencia_oab**: Status de adimplência (padrão: True)
    - **cadastro_id**: ID do cadastro associado ao usuário
    """
    service = UsuarioAdvogadoService(db)
    return service.criar_usuario(usuario)


@router.get(
    "",
    response_model=List[UsuarioAdvogadoResponse],
    summary="Listar usuários advogados",
    description="Retorna uma lista paginada de todos os usuários advogados cadastrados no sistema.",
)
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todos os usuários advogados com paginação.

    - **skip**: Número de registros a pular (para paginação)
    - **limit**: Número máximo de registros a retornar (padrão: 100)
    """
    service = UsuarioAdvogadoService(db)
    return service.listar_usuarios(skip=skip, limit=limit)


@router.get(
    "/{usuario_id}",
    response_model=UsuarioAdvogadoResponse,
    summary="Obter usuário advogado por ID",
    description="Retorna os detalhes de um usuário advogado específico pelo seu ID.",
)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de um usuário advogado específico.

    - **usuario_id**: ID único do usuário advogado
    """
    service = UsuarioAdvogadoService(db)
    return service.obter_usuario(usuario_id)


@router.put(
    "/{usuario_id}",
    response_model=UsuarioAdvogadoResponse,
    summary="Atualizar usuário advogado",
    description="Atualiza os dados de um usuário advogado existente.",
)
def atualizar_usuario(
    usuario_id: int,
    usuario: UsuarioAdvogadoUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de um usuário advogado.

    - **usuario_id**: ID único do usuário advogado
    - **usuario**: Dados a serem atualizados (campos opcionais)
    """
    service = UsuarioAdvogadoService(db)
    return service.atualizar_usuario(usuario_id, usuario)


@router.delete(
    "/{usuario_id}",
    response_model=MensagemResponse,
    summary="Deletar usuário advogado",
    description="Remove um usuário advogado do sistema. Esta operação é irreversível.",
)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Deleta um usuário advogado do sistema.

    - **usuario_id**: ID único do usuário advogado a ser deletado
    """
    service = UsuarioAdvogadoService(db)
    service.deletar_usuario(usuario_id)
    return MensagemResponse(mensagem="Usuário advogado deletado com sucesso")

