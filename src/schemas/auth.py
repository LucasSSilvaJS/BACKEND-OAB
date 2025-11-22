from enum import Enum
from pydantic import BaseModel


class TipoUsuario(str, Enum):
    ADVOGADO = "ADVOGADO"
    ADMINISTRADOR = "ADMINISTRADOR"
    ANALISTA = "ANALISTA"


class LoginAdvogado(BaseModel):
    registro_oab: str
    codigo_de_seguranca: str


class LoginAdministrador(BaseModel):
    usuario: str
    senha: str


class LoginAnalista(BaseModel):
    usuario: str
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    tipo_usuario: TipoUsuario
    usuario_id: int
    cadastro_id: int
    nome: str

