from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.schemas.cadastro import CadastroCreate, CadastroUpdate, CadastroResponse
from src.schemas.comum import MensagemResponse
from src.services.cadastro_service import CadastroService

router = APIRouter(
    prefix="/cadastros",
    tags=["Cadastros"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post(
    "",
    response_model=CadastroResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo cadastro",
    description="Cria um novo cadastro no sistema. O email e CPF devem ser únicos.",
    response_description="Cadastro criado com sucesso",
)
def criar_cadastro(cadastro: CadastroCreate, db: Session = Depends(get_db)):
    """
    Cria um novo cadastro no sistema.

    - **nome**: Nome completo da pessoa
    - **email**: Email único (será validado)
    - **telefone**: Telefone de contato (opcional)
    - **cpf**: CPF único (será validado)
    - **rg**: RG da pessoa (opcional)
    - **endereco**: Endereço completo (opcional)
    """
    service = CadastroService(db)
    return service.criar_cadastro(cadastro)


@router.get(
    "",
    response_model=List[CadastroResponse],
    summary="Listar cadastros",
    description="Retorna uma lista paginada de todos os cadastros cadastrados no sistema.",
)
def listar_cadastros(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todos os cadastros com paginação.

    - **skip**: Número de registros a pular (para paginação)
    - **limit**: Número máximo de registros a retornar (padrão: 100)
    """
    service = CadastroService(db)
    return service.listar_cadastros(skip=skip, limit=limit)


@router.get(
    "/{cadastro_id}",
    response_model=CadastroResponse,
    summary="Obter cadastro por ID",
    description="Retorna os detalhes de um cadastro específico pelo seu ID.",
)
def obter_cadastro(cadastro_id: int, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de um cadastro específico.

    - **cadastro_id**: ID único do cadastro
    """
    service = CadastroService(db)
    return service.obter_cadastro(cadastro_id)


@router.put(
    "/{cadastro_id}",
    response_model=CadastroResponse,
    summary="Atualizar cadastro",
    description="Atualiza os dados de um cadastro existente. Apenas os campos fornecidos serão atualizados.",
)
def atualizar_cadastro(
    cadastro_id: int,
    cadastro: CadastroUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza os dados de um cadastro.

    - **cadastro_id**: ID único do cadastro
    - **cadastro**: Dados a serem atualizados (campos opcionais)
    """
    service = CadastroService(db)
    return service.atualizar_cadastro(cadastro_id, cadastro)


@router.delete(
    "/{cadastro_id}",
    response_model=MensagemResponse,
    summary="Deletar cadastro",
    description="Remove um cadastro do sistema. Esta operação é irreversível.",
)
def deletar_cadastro(cadastro_id: int, db: Session = Depends(get_db)):
    """
    Deleta um cadastro do sistema.

    - **cadastro_id**: ID único do cadastro a ser deletado
    """
    service = CadastroService(db)
    service.deletar_cadastro(cadastro_id)
    return MensagemResponse(mensagem="Cadastro deletado com sucesso")

