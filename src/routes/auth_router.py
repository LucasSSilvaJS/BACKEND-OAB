from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.schemas.auth import (
    LoginAdvogado,
    LoginAdministrador,
    LoginAnalista,
    TokenResponse,
    TipoUsuario
)
from src.repositories.usuario_advogado_repository import UsuarioAdvogadoRepository
from src.repositories.administrador_sala_repository import AdministradorSalaRepository
from src.repositories.analista_ti_repository import AnalistaTIRepository
from src.utils.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/login/advogado",
    response_model=TokenResponse,
    summary="Login de Advogado",
    description="Autentica um advogado usando registro OAB e código de segurança"
)
async def login_advogado(
    credentials: LoginAdvogado,
    db: Session = Depends(get_db)
):
    """
    Endpoint de login para advogados.
    
    Autentica um advogado usando:
    - registro_oab: Registro OAB do advogado
    - codigo_de_seguranca: Código de segurança do advogado
    """
    usuario_repo = UsuarioAdvogadoRepository(db)
    usuario = usuario_repo.get_by_registro_oab(credentials.registro_oab)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Registro OAB ou código de segurança inválidos"
        )
    
    # Verificar código de segurança (comparação direta, não é hash)
    if usuario.codigo_de_seguranca != credentials.codigo_de_seguranca:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Registro OAB ou código de segurança inválidos"
        )
    
    # Verificar adimplência
    if not usuario.adimplencia_oab:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Advogado não está adimplente com a OAB"
        )
    
    # Criar token
    access_token = create_access_token(
        data={
            "sub": str(usuario.usuario_id),
            "tipo_usuario": TipoUsuario.ADVOGADO.value,
            "usuario_id": usuario.usuario_id
        }
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        tipo_usuario=TipoUsuario.ADVOGADO,
        usuario_id=usuario.usuario_id,
        cadastro_id=usuario.cadastro_id,
        nome=usuario.cadastro.nome
    )


@router.post(
    "/login/administrador",
    response_model=TokenResponse,
    summary="Login de Administrador",
    description="Autentica um administrador de sala usando usuário e senha"
)
async def login_administrador(
    credentials: LoginAdministrador,
    db: Session = Depends(get_db)
):
    """
    Endpoint de login para administradores de sala.
    
    Autentica um administrador usando:
    - usuario: Nome de usuário do administrador
    - senha: Senha do administrador (hash bcrypt)
    """
    admin_repo = AdministradorSalaRepository(db)
    administrador = admin_repo.get_by_usuario(credentials.usuario)
    
    if not administrador:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )
    
    # Verificar senha (hash bcrypt)
    if not verify_password(credentials.senha, administrador.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )
    
    # Criar token
    access_token = create_access_token(
        data={
            "sub": str(administrador.admin_id),
            "tipo_usuario": TipoUsuario.ADMINISTRADOR.value,
            "usuario_id": administrador.admin_id
        }
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        tipo_usuario=TipoUsuario.ADMINISTRADOR,
        usuario_id=administrador.admin_id,
        cadastro_id=administrador.cadastro_id,
        nome=administrador.cadastro.nome
    )


@router.post(
    "/login/analista",
    response_model=TokenResponse,
    summary="Login de Analista de TI",
    description="Autentica um analista de TI usando usuário e senha"
)
async def login_analista(
    credentials: LoginAnalista,
    db: Session = Depends(get_db)
):
    """
    Endpoint de login para analistas de TI.
    
    Autentica um analista usando:
    - usuario: Nome de usuário do analista
    - senha: Senha do analista (hash bcrypt)
    """
    analista_repo = AnalistaTIRepository(db)
    analista = analista_repo.get_by_usuario(credentials.usuario)
    
    if not analista:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )
    
    # Verificar senha (hash bcrypt)
    if not verify_password(credentials.senha, analista.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )
    
    # Criar token
    access_token = create_access_token(
        data={
            "sub": str(analista.analista_id),
            "tipo_usuario": TipoUsuario.ANALISTA.value,
            "usuario_id": analista.analista_id
        }
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        tipo_usuario=TipoUsuario.ANALISTA,
        usuario_id=analista.analista_id,
        cadastro_id=analista.cadastro_id,
        nome=analista.cadastro.nome
    )

