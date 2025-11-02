from typing import List
from datetime import date
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.schemas.sessao import SessaoCreate, SessaoUpdate, SessaoResponse
from src.schemas.comum import MensagemResponse
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
def criar_sessao(sessao: SessaoCreate, db: Session = Depends(get_db)):
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
    summary="Listar sessões",
    description="Retorna uma lista paginada de todas as sessões cadastradas.",
)
def listar_sessoes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todas as sessões com paginação.

    - **skip**: Número de registros a pular (para paginação)
    - **limit**: Número máximo de registros a retornar (padrão: 100)
    """
    service = SessaoService(db)
    return service.listar_sessoes(skip=skip, limit=limit)


@router.get(
    "/ativas",
    response_model=List[SessaoResponse],
    summary="Listar sessões ativas",
    description="Retorna todas as sessões que estão atualmente ativas (não finalizadas).",
)
def listar_sessoes_ativas(db: Session = Depends(get_db)):
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
def obter_sessao(sessao_id: int, db: Session = Depends(get_db)):
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
def listar_sessoes_por_usuario(usuario_id: int, db: Session = Depends(get_db)):
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
def listar_sessoes_por_data(data: date, db: Session = Depends(get_db)):
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
def finalizar_sessao(sessao_id: int, db: Session = Depends(get_db)):
    """
    Finaliza uma sessão ativa.

    - **sessao_id**: ID único da sessão a ser finalizada
    """
    service = SessaoService(db)
    return service.finalizar_sessao(sessao_id)


@router.delete(
    "/{sessao_id}",
    response_model=MensagemResponse,
    summary="Deletar sessão",
    description="Remove uma sessão do sistema. Esta operação é irreversível.",
)
def deletar_sessao(sessao_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma sessão do sistema.

    - **sessao_id**: ID único da sessão a ser deletada
    """
    service = SessaoService(db)
    service.deletar_sessao(sessao_id)
    return MensagemResponse(mensagem="Sessão deletada com sucesso")

