"""
Router para popular o banco de dados em massa.
Cada endpoint recebe um array de objetos e insere todos de uma vez.

⚠️ ATENÇÃO: Todas as rotas requerem autenticação como Analista de TI.
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, status, HTTPException, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from src.routes.dependencies import get_db
from src.routes.auth_dependencies import require_analista, AuthUser
from src.database import seed

router = APIRouter(
    prefix="/seed",
    tags=["Seed - Popular Banco"],
    responses={404: {"description": "Não encontrado"}},
)


# Schemas para documentação melhorada
class CadastroSeed(BaseModel):
    """Schema para cadastro"""
    nome: str = Field(..., description="Nome completo da pessoa", example="João Silva")
    email: str = Field(..., description="Email único (obrigatório)", example="joao@email.com")
    cpf: str = Field(..., description="CPF único (obrigatório, 11 dígitos)", example="12345678901")
    telefone: str = Field(None, description="Telefone (opcional)", example="11999999999")
    rg: str = Field(None, description="RG (opcional)", example="123456789")
    endereco: str = Field(None, description="Endereço completo (opcional)", example="Rua Exemplo, 123")


class SubsecionalSeed(BaseModel):
    """Schema para subsecional"""
    nome: str = Field(..., description="Nome da subsecional (obrigatório, único)", example="Subsecional Norte")


class UnidadeSeed(BaseModel):
    """Schema para unidade"""
    nome: str = Field(..., description="Nome da unidade (obrigatório)", example="Unidade Centro")
    hierarquia: str = Field(..., description="Hierarquia: 'SEDE' ou 'FILIAL' (obrigatório)", example="SEDE")
    subsecional_id: int = Field(..., description="ID da subsecional (obrigatório)", example=1)
    endereco: str = Field(None, description="Endereço (opcional)", example="Rua Centro, 100")
    latitude: float = Field(None, description="Latitude (opcional)", example=-23.5505)
    longitude: float = Field(None, description="Longitude (opcional)", example=-46.6333)


class SalaCoworkingSeed(BaseModel):
    """Schema para sala de coworking"""
    nome_da_sala: str = Field(..., description="Nome da sala (obrigatório)", example="Sala A")
    subsecional_id: int = Field(..., description="ID da subsecional (obrigatório)", example=1)
    unidade_id: int = Field(..., description="ID da unidade (obrigatório)", example=1)
    administrador_id: int = Field(None, description="ID do administrador (opcional)", example=1)


class ComputadorSeed(BaseModel):
    """Schema para computador"""
    ip_da_maquina: str = Field(..., description="IP único da máquina (obrigatório, formato: xxx.xxx.xxx.xxx)", example="192.168.1.100")
    numero_de_tombamento: str = Field(..., description="Número de tombamento único (obrigatório)", example="T001")
    coworking_id: int = Field(..., description="ID da sala de coworking (obrigatório)", example=1)


class UsuarioAdvogadoSeed(BaseModel):
    """Schema para usuário advogado"""
    cadastro_id: int = Field(..., description="ID do cadastro (obrigatório)", example=1)
    registro_oab: str = Field(..., description="Registro OAB único (obrigatório)", example="12345")
    codigo_de_seguranca: str = Field(..., description="Código de segurança (obrigatório)", example="ABC123")
    adimplencia_oab: bool = Field(True, description="Status de adimplência (padrão: true)", example=True)


class AnalistaTISeed(BaseModel):
    """Schema para analista de TI"""
    cadastro_id: int = Field(..., description="ID do cadastro (obrigatório)", example=1)
    usuario: str = Field(..., description="Nome de usuário único (obrigatório)", example="analista1")
    senha: str = Field(..., description="Senha (será hasheada automaticamente)", example="senha123")


class AdministradorSalaSeed(BaseModel):
    """Schema para administrador de sala"""
    cadastro_id: int = Field(..., description="ID do cadastro (obrigatório)", example=1)
    usuario: str = Field(..., description="Nome de usuário único (obrigatório)", example="admin1")
    senha: str = Field(..., description="Senha (será hasheada automaticamente)", example="senha123")
    adm_local: bool = Field(False, description="É administrador local? (padrão: false)", example=True)
    admin_central: bool = Field(False, description="É administrador central? (padrão: false)", example=False)


class SessaoSeed(BaseModel):
    """Schema para sessão"""
    data: str = Field(..., description="Data da sessão (formato: YYYY-MM-DD)", example="2025-01-15")
    inicio_de_sessao: str = Field(..., description="Data e hora de início (formato: YYYY-MM-DDTHH:MM:SS)", example="2025-01-15T08:00:00")
    computador_id: int = Field(..., description="ID do computador (obrigatório)", example=1)
    usuario_id: int = Field(..., description="ID do usuário advogado (obrigatório)", example=1)
    administrador_id: int = Field(..., description="ID do administrador (obrigatório)", example=1)
    final_de_sessao: str = Field(None, description="Data e hora de finalização (opcional, formato: YYYY-MM-DDTHH:MM:SS)", example="2025-01-15T18:00:00")
    ativado: bool = Field(True, description="Status da sessão (padrão: true)", example=True)


@router.post(
    "/cadastros",
    status_code=status.HTTP_201_CREATED,
    summary="Popular cadastros em massa",
    description="""
    Insere múltiplos cadastros no banco de dados de uma vez.
    
    **Campos obrigatórios:**
    - `nome`: Nome completo
    - `email`: Email único (não pode repetir)
    - `cpf`: CPF único (11 dígitos, não pode repetir)
    
    **Campos opcionais:**
    - `telefone`: Telefone de contato
    - `rg`: Número do RG
    - `endereco`: Endereço completo
    
    **Validações:**
    - Email deve ser único no banco
    - CPF deve ser único no banco
    - Registros duplicados serão ignorados (não interrompe a inserção dos demais)
    
    **Resposta:**
    Retorna o total de cadastros criados e seus IDs.
    """,
    response_description="Lista de cadastros criados com sucesso"
)
def popular_cadastros(
    cadastros: List[Dict[str, Any]] = Body(
        ...,
        example=[
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
        ],
        description="Array de objetos com os dados dos cadastros"
    ),
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
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
    description="""
    Insere múltiplas subseccionais no banco de dados de uma vez.
    
    **Campos obrigatórios:**
    - `nome`: Nome da subsecional (deve ser único)
    
    **Validações:**
    - Nome deve ser único no banco
    - Registros duplicados serão ignorados
    
    **Resposta:**
    Retorna o total de subseccionais criadas e seus IDs.
    """,
    response_description="Lista de subseccionais criadas com sucesso"
)
def popular_subsecionais(
    subsecionais: List[Dict[str, Any]] = Body(
        ...,
        example=[
            {"nome": "Subsecional Norte"},
            {"nome": "Subsecional Sul"},
            {"nome": "Subsecional Leste"},
            {"nome": "Subsecional Oeste"}
        ],
        description="Array de objetos com os dados das subseccionais"
    ),
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
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
    description="""
    Insere múltiplas unidades no banco de dados de uma vez.
    
    **Campos obrigatórios:**
    - `nome`: Nome da unidade
    - `hierarquia`: Deve ser "SEDE" ou "FILIAL"
    - `subsecional_id`: ID da subsecional (deve existir no banco)
    
    **Campos opcionais:**
    - `endereco`: Endereço da unidade
    - `latitude`: Coordenada de latitude
    - `longitude`: Coordenada de longitude
    
    **Validações:**
    - `subsecional_id` deve existir no banco
    - `hierarquia` deve ser exatamente "SEDE" ou "FILIAL"
    
    **Resposta:**
    Retorna o total de unidades criadas e seus IDs.
    """,
    response_description="Lista de unidades criadas com sucesso"
)
def popular_unidades(
    unidades: List[Dict[str, Any]] = Body(
        ...,
        example=[
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
        ],
        description="Array de objetos com os dados das unidades"
    ),
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
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
    description="""
    Insere múltiplas salas de coworking no banco de dados de uma vez.
    
    **Campos obrigatórios:**
    - `nome_da_sala`: Nome da sala
    - `subsecional_id`: ID da subsecional (deve existir no banco)
    - `unidade_id`: ID da unidade (deve existir no banco)
    
    **Campos opcionais:**
    - `administrador_id`: ID do administrador (deve existir no banco)
    
    **Validações:**
    - `subsecional_id` deve existir no banco
    - `unidade_id` deve existir no banco
    - `administrador_id` deve existir no banco (se fornecido)
    
    **Resposta:**
    Retorna o total de salas criadas e seus IDs.
    """,
    response_description="Lista de salas de coworking criadas com sucesso"
)
def popular_salas_coworking(
    salas: List[Dict[str, Any]] = Body(
        ...,
        example=[
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
        ],
        description="Array de objetos com os dados das salas de coworking"
    ),
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
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
    description="""
    Insere múltiplos computadores no banco de dados de uma vez.
    
    **Campos obrigatórios:**
    - `ip_da_maquina`: IP da máquina (deve ser único, formato: xxx.xxx.xxx.xxx)
    - `numero_de_tombamento`: Número de tombamento (deve ser único)
    - `coworking_id`: ID da sala de coworking (deve existir no banco)
    
    **Validações:**
    - `ip_da_maquina` deve ser único no banco
    - `numero_de_tombamento` deve ser único no banco
    - `coworking_id` deve existir no banco
    - Registros duplicados serão ignorados
    
    **Resposta:**
    Retorna o total de computadores criados e seus IDs.
    """,
    response_description="Lista de computadores criados com sucesso"
)
def popular_computadores(
    computadores: List[Dict[str, Any]] = Body(
        ...,
        example=[
            {
                "ip_da_maquina": "192.168.1.100",
                "numero_de_tombamento": "T001",
                "coworking_id": 1
            },
            {
                "ip_da_maquina": "192.168.1.101",
                "numero_de_tombamento": "T002",
                "coworking_id": 1
            },
            {
                "ip_da_maquina": "192.168.1.102",
                "numero_de_tombamento": "T003",
                "coworking_id": 1
            }
        ],
        description="Array de objetos com os dados dos computadores"
    ),
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
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
    description="""
    Insere múltiplos usuários advogados no banco de dados de uma vez.
    
    **Campos obrigatórios:**
    - `cadastro_id`: ID do cadastro (deve existir no banco)
    - `registro_oab`: Número do registro OAB (deve ser único)
    - `codigo_de_seguranca`: Código de segurança
    
    **Campos opcionais:**
    - `adimplencia_oab`: Status de adimplência (padrão: true)
    
    **Validações:**
    - `cadastro_id` deve existir no banco
    - `registro_oab` deve ser único no banco
    - Registros duplicados serão ignorados
    
    **Resposta:**
    Retorna o total de usuários advogados criados e seus IDs.
    """,
    response_description="Lista de usuários advogados criados com sucesso"
)
def popular_usuarios_advogados(
    usuarios: List[Dict[str, Any]] = Body(
        ...,
        example=[
            {
                "cadastro_id": 1,
                "registro_oab": "12345",
                "codigo_de_seguranca": "ABC123",
                "adimplencia_oab": True
            },
            {
                "cadastro_id": 2,
                "registro_oab": "67890",
                "codigo_de_seguranca": "XYZ789",
                "adimplencia_oab": True
            }
        ],
        description="Array de objetos com os dados dos usuários advogados"
    ),
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
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
    description="""
    Insere múltiplos analistas de TI no banco de dados de uma vez.
    
    **Campos obrigatórios:**
    - `cadastro_id`: ID do cadastro (deve existir no banco)
    - `usuario`: Nome de usuário (deve ser único)
    - `senha`: Senha (será hasheada automaticamente)
    
    **Validações:**
    - `cadastro_id` deve existir no banco
    - `usuario` deve ser único no banco
    - A senha será hasheada automaticamente antes de ser salva
    - Registros duplicados serão ignorados
    
    **Resposta:**
    Retorna o total de analistas de TI criados e seus IDs.
    """,
    response_description="Lista de analistas de TI criados com sucesso"
)
def popular_analistas_ti(
    analistas: List[Dict[str, Any]] = Body(
        ...,
        example=[
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
        ],
        description="Array de objetos com os dados dos analistas de TI"
    ),
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
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
    description="""
    Insere múltiplos administradores de sala no banco de dados de uma vez.
    
    **Campos obrigatórios:**
    - `cadastro_id`: ID do cadastro (deve existir no banco)
    - `usuario`: Nome de usuário (deve ser único)
    - `senha`: Senha (será hasheada automaticamente)
    
    **Campos opcionais:**
    - `adm_local`: É administrador local? (padrão: false)
    - `admin_central`: É administrador central? (padrão: false)
    
    **Validações:**
    - `cadastro_id` deve existir no banco
    - `usuario` deve ser único no banco
    - A senha será hasheada automaticamente antes de ser salva
    - Registros duplicados serão ignorados
    
    **Resposta:**
    Retorna o total de administradores de sala criados e seus IDs.
    """,
    response_description="Lista de administradores de sala criados com sucesso"
)
def popular_administradores_sala(
    administradores: List[Dict[str, Any]] = Body(
        ...,
        example=[
            {
                "cadastro_id": 1,
                "usuario": "admin1",
                "senha": "senha123",
                "adm_local": True,
                "admin_central": False
            },
            {
                "cadastro_id": 2,
                "usuario": "admin2",
                "senha": "senha456",
                "adm_local": False,
                "admin_central": True
            }
        ],
        description="Array de objetos com os dados dos administradores de sala"
    ),
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
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
    description="""
    Insere múltiplas sessões no banco de dados de uma vez.
    
    **Campos obrigatórios:**
    - `data`: Data da sessão (formato: YYYY-MM-DD)
    - `inicio_de_sessao`: Data e hora de início (formato: YYYY-MM-DDTHH:MM:SS)
    - `computador_id`: ID do computador (deve existir no banco)
    - `usuario_id`: ID do usuário advogado (deve existir no banco)
    - `administrador_id`: ID do administrador (deve existir no banco)
    
    **Campos opcionais:**
    - `final_de_sessao`: Data e hora de finalização (formato: YYYY-MM-DDTHH:MM:SS)
    - `ativado`: Status da sessão (padrão: true)
    
    **Validações:**
    - `computador_id` deve existir no banco
    - `usuario_id` deve existir no banco
    - `administrador_id` deve existir no banco
    - A data deve estar no formato correto
    - O datetime deve estar no formato correto
    
    **Resposta:**
    Retorna o total de sessões criadas e seus IDs.
    """,
    response_description="Lista de sessões criadas com sucesso"
)
def popular_sessoes(
    sessoes: List[Dict[str, Any]] = Body(
        ...,
        example=[
            {
                "data": "2025-01-15",
                "inicio_de_sessao": "2025-01-15T08:00:00",
                "computador_id": 1,
                "usuario_id": 1,
                "administrador_id": 1,
                "ativado": True
            },
            {
                "data": "2025-01-15",
                "inicio_de_sessao": "2025-01-15T09:00:00",
                "final_de_sessao": "2025-01-15T18:00:00",
                "computador_id": 2,
                "usuario_id": 2,
                "administrador_id": 1,
                "ativado": False
            }
        ],
        description="Array de objetos com os dados das sessões"
    ),
    current_user: AuthUser = Depends(require_analista),
    db: Session = Depends(get_db)
):
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
