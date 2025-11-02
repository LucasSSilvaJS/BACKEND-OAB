from typing import Optional
from pydantic import BaseModel
from src.schemas.cadastro import CadastroResponse


class UsuarioAdvogadoBase(BaseModel):
    registro_oab: str
    codigo_de_seguranca: str
    adimplencia_oab: bool = True


class UsuarioAdvogadoCreate(UsuarioAdvogadoBase):
    cadastro_id: int


class UsuarioAdvogadoUpdate(BaseModel):
    registro_oab: Optional[str] = None
    codigo_de_seguranca: Optional[str] = None
    adimplencia_oab: Optional[bool] = None


class UsuarioAdvogadoResponse(UsuarioAdvogadoBase):
    usuario_id: int
    cadastro_id: int
    cadastro: Optional[CadastroResponse] = None

    class Config:
        from_attributes = True

