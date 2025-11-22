"""
Router para popular o banco de dados em massa.
Cada endpoint recebe um array de objetos e insere todos de uma vez.
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.routes.auth_dependencies import require_analista, AuthUser
from src.database import seed

router = APIRouter(
    prefix="/seed",
    tags=["Seed - Popular Banco"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post(
    "/cadastros",
    status_code=status.HTTP_201_CREATED,
    summary="Popular cadastros em massa",
    description="Insere múltiplos cadastros no banco de dados de uma vez.",
)
def popular_cadastros(
    cadastros: List[Dict[str, Any]],
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
    """
    Popula o banco com múltiplos cadastros.
    
    **Exemplo de body:**
    ```json
    [
        {
            "nome": "João Silva",
            "email": "joao@email.com",
            "cpf": "12345678901",
            "telefone": "11999999999",
            "rg": "123456789",
            "endereco": "Rua Exemplo, 123"
        },
        {
            "nome": "Maria Santos",
            "email": "maria@email.com",
            "cpf": "98765432100",
            "telefone": "11888888888"
        }
    ]
    ```
    """
    try:
        objetos = seed.popular_cadastros(db, cadastros)
        return {
            "mensagem": f"{len(objetos)} cadastro(s) criado(s) com sucesso",
            "total": len(objetos),
            "ids": [obj.cadastro_id for obj in objetos]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao popular cadastros: {str(e)}"
        )


@router.post(
    "/subsecionais",
    status_code=status.HTTP_201_CREATED,
    summary="Popular subseccionais em massa",
    description="Insere múltiplas subseccionais no banco de dados de uma vez.",
)
def popular_subsecionais(
    subsecionais: List[Dict[str, Any]],
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
    """
    Popula o banco com múltiplas subseccionais.
    
    **Exemplo de body:**
    ```json
    [
        {"nome": "Subsecional Norte"},
        {"nome": "Subsecional Sul"},
        {"nome": "Subsecional Leste"}
    ]
    ```
    """
    try:
        objetos = seed.popular_subsecionais(db, subsecionais)
        return {
            "mensagem": f"{len(objetos)} subsecional(is) criada(s) com sucesso",
            "total": len(objetos),
            "ids": [obj.subsecional_id for obj in objetos]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao popular subseccionais: {str(e)}"
        )


@router.post(
    "/unidades",
    status_code=status.HTTP_201_CREATED,
    summary="Popular unidades em massa",
    description="Insere múltiplas unidades no banco de dados de uma vez.",
)
def popular_unidades(
    unidades: List[Dict[str, Any]],
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
    """
    Popula o banco com múltiplas unidades.
    
    **Exemplo de body:**
    ```json
    [
        {
            "nome": "Unidade Centro",
            "hierarquia": "SEDE",
            "subsecional_id": 1,
            "endereco": "Rua Centro, 100",
            "latitude": -23.5505,
            "longitude": -46.6333
        },
        {
            "nome": "Unidade Zona Norte",
            "hierarquia": "FILIAL",
            "subsecional_id": 1
        }
    ]
    ```
    """
    try:
        objetos = seed.popular_unidades(db, unidades)
        return {
            "mensagem": f"{len(objetos)} unidade(s) criada(s) com sucesso",
            "total": len(objetos),
            "ids": [obj.unidade_id for obj in objetos]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao popular unidades: {str(e)}"
        )


@router.post(
    "/salas-coworking",
    status_code=status.HTTP_201_CREATED,
    summary="Popular salas de coworking em massa",
    description="Insere múltiplas salas de coworking no banco de dados de uma vez.",
)
def popular_salas_coworking(
    salas: List[Dict[str, Any]],
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
    """
    Popula o banco com múltiplas salas de coworking.
    
    **Exemplo de body:**
    ```json
    [
        {
            "nome_da_sala": "Sala A",
            "subsecional_id": 1,
            "unidade_id": 1,
            "administrador_id": 1
        },
        {
            "nome_da_sala": "Sala B",
            "subsecional_id": 1,
            "unidade_id": 1
        }
    ]
    ```
    """
    try:
        objetos = seed.popular_salas_coworking(db, salas)
        return {
            "mensagem": f"{len(objetos)} sala(s) de coworking criada(s) com sucesso",
            "total": len(objetos),
            "ids": [obj.coworking_id for obj in objetos]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao popular salas de coworking: {str(e)}"
        )


@router.post(
    "/computadores",
    status_code=status.HTTP_201_CREATED,
    summary="Popular computadores em massa",
    description="Insere múltiplos computadores no banco de dados de uma vez.",
)
def popular_computadores(
    computadores: List[Dict[str, Any]],
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
    """
    Popula o banco com múltiplos computadores.
    
    **Exemplo de body:**
    ```json
    [
        {
            "ip_da_maquina": "192.168.1.100",
            "numero_de_tombamento": "T001",
            "coworking_id": 1
        },
        {
            "ip_da_maquina": "192.168.1.101",
            "numero_de_tombamento": "T002",
            "coworking_id": 1
        }
    ]
    ```
    """
    try:
        objetos = seed.popular_computadores(db, computadores)
        return {
            "mensagem": f"{len(objetos)} computador(es) criado(s) com sucesso",
            "total": len(objetos),
            "ids": [obj.computador_id for obj in objetos]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao popular computadores: {str(e)}"
        )


@router.post(
    "/usuarios-advogados",
    status_code=status.HTTP_201_CREATED,
    summary="Popular usuários advogados em massa",
    description="Insere múltiplos usuários advogados no banco de dados de uma vez.",
)
def popular_usuarios_advogados(
    usuarios: List[Dict[str, Any]],
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
    """
    Popula o banco com múltiplos usuários advogados.
    
    **Exemplo de body:**
    ```json
    [
        {
            "cadastro_id": 1,
            "registro_oab": "12345",
            "codigo_de_seguranca": "ABC123",
            "adimplencia_oab": true
        },
        {
            "cadastro_id": 2,
            "registro_oab": "67890",
            "codigo_de_seguranca": "XYZ789",
            "adimplencia_oab": true
        }
    ]
    ```
    """
    try:
        objetos = seed.popular_usuarios_advogados(db, usuarios)
        return {
            "mensagem": f"{len(objetos)} usuário(s) advogado(s) criado(s) com sucesso",
            "total": len(objetos),
            "ids": [obj.usuario_id for obj in objetos]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao popular usuários advogados: {str(e)}"
        )


@router.post(
    "/analistas-ti",
    status_code=status.HTTP_201_CREATED,
    summary="Popular analistas de TI em massa",
    description="Insere múltiplos analistas de TI no banco de dados de uma vez.",
)
def popular_analistas_ti(
    analistas: List[Dict[str, Any]],
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
    """
    Popula o banco com múltiplos analistas de TI.
    
    **Exemplo de body:**
    ```json
    [
        {
            "cadastro_id": 1,
            "usuario": "analista1",
            "senha": "senha123"
        },
        {
            "cadastro_id": 2,
            "usuario": "analista2",
            "senha": "senha456"
        }
    ]
    ```
    """
    try:
        objetos = seed.popular_analistas_ti(db, analistas)
        return {
            "mensagem": f"{len(objetos)} analista(s) de TI criado(s) com sucesso",
            "total": len(objetos),
            "ids": [obj.analista_id for obj in objetos]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao popular analistas de TI: {str(e)}"
        )


@router.post(
    "/administradores-sala",
    status_code=status.HTTP_201_CREATED,
    summary="Popular administradores de sala em massa",
    description="Insere múltiplos administradores de sala no banco de dados de uma vez.",
)
def popular_administradores_sala(
    administradores: List[Dict[str, Any]],
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
    """
    Popula o banco com múltiplos administradores de sala.
    
    **Exemplo de body:**
    ```json
    [
        {
            "cadastro_id": 1,
            "usuario": "admin1",
            "senha": "senha123",
            "adm_local": true,
            "admin_central": false
        },
        {
            "cadastro_id": 2,
            "usuario": "admin2",
            "senha": "senha456",
            "adm_local": false,
            "admin_central": true
        }
    ]
    ```
    """
    try:
        objetos = seed.popular_administradores_sala(db, administradores)
        return {
            "mensagem": f"{len(objetos)} administrador(es) de sala criado(s) com sucesso",
            "total": len(objetos),
            "ids": [obj.admin_id for obj in objetos]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao popular administradores de sala: {str(e)}"
        )


@router.post(
    "/sessoes",
    status_code=status.HTTP_201_CREATED,
    summary="Popular sessões em massa",
    description="Insere múltiplas sessões no banco de dados de uma vez.",
)
def popular_sessoes(
    sessoes: List[Dict[str, Any]],
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
    """
    Popula o banco com múltiplas sessões.
    
    **Exemplo de body:**
    ```json
    [
        {
            "data": "2025-01-15",
            "inicio_de_sessao": "2025-01-15T08:00:00",
            "computador_id": 1,
            "usuario_id": 1,
            "administrador_id": 1,
            "ativado": true
        },
        {
            "data": "2025-01-15",
            "inicio_de_sessao": "2025-01-15T09:00:00",
            "computador_id": 2,
            "usuario_id": 2,
            "administrador_id": 1,
            "ativado": true
        }
    ]
    ```
    """
    try:
        objetos = seed.popular_sessoes(db, sessoes)
        return {
            "mensagem": f"{len(objetos)} sessão(ões) criada(s) com sucesso",
            "total": len(objetos),
            "ids": [obj.sessao_id for obj in objetos]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao popular sessões: {str(e)}"
        )

