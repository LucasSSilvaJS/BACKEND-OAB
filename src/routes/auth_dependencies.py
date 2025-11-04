from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.routes.dependencies import get_db
from src.schemas.auth import TipoUsuario
from src.utils.security import verify_token
from src.repositories.usuario_advogado_repository import UsuarioAdvogadoRepository
from src.repositories.administrador_sala_repository import AdministradorSalaRepository
from src.repositories.analista_ti_repository import AnalistaTIRepository


security = HTTPBearer()


class AuthUser:
    """Classe para armazenar informações do usuário autenticado"""
    def __init__(self, usuario_id: int, tipo_usuario: TipoUsuario):
        self.usuario_id = usuario_id
        self.tipo_usuario = tipo_usuario


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> AuthUser:
    """
    Dependência para obter o usuário atual autenticado.
    
    Verifica o token JWT e retorna as informações do usuário.
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    usuario_id: int = payload.get("usuario_id")
    tipo_usuario_str: str = payload.get("tipo_usuario")
    
    if usuario_id is None or tipo_usuario_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: informações do usuário ausentes",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar se o tipo de usuário é válido
    try:
        tipo_usuario = TipoUsuario(tipo_usuario_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: tipo de usuário inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar se o usuário ainda existe no banco de dados
    if tipo_usuario == TipoUsuario.ADVOGADO:
        repo = UsuarioAdvogadoRepository(db)
        usuario = repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
    elif tipo_usuario == TipoUsuario.ADMINISTRADOR:
        repo = AdministradorSalaRepository(db)
        usuario = repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
    elif tipo_usuario == TipoUsuario.ANALISTA:
        repo = AnalistaTIRepository(db)
        usuario = repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    return AuthUser(usuario_id=usuario_id, tipo_usuario=tipo_usuario)


def require_permission(*allowed_types: TipoUsuario):
    """
    Factory para criar dependências que requerem tipos específicos de usuário.
    
    Args:
        *allowed_types: Tipos de usuário permitidos
    
    Returns:
        Dependência do FastAPI que verifica se o usuário tem permissão
    """
    async def permission_checker(
        current_user: AuthUser = Depends(get_current_user)
    ) -> AuthUser:
        if current_user.tipo_usuario not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Tipos permitidos: {[t.value for t in allowed_types]}"
            )
        return current_user
    
    return permission_checker


# Dependências pré-configuradas para facilitar o uso
require_advogado = require_permission(TipoUsuario.ADVOGADO)
require_administrador = require_permission(TipoUsuario.ADMINISTRADOR)
require_analista = require_permission(TipoUsuario.ANALISTA)
require_advogado_or_administrador = require_permission(TipoUsuario.ADVOGADO, TipoUsuario.ADMINISTRADOR)
require_advogado_or_analista = require_permission(TipoUsuario.ADVOGADO, TipoUsuario.ANALISTA)
require_administrador_or_analista = require_permission(TipoUsuario.ADMINISTRADOR, TipoUsuario.ANALISTA)
require_any_user = require_permission(TipoUsuario.ADVOGADO, TipoUsuario.ADMINISTRADOR, TipoUsuario.ANALISTA)

