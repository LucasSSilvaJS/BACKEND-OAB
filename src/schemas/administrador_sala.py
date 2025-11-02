from typing import Optional
from pydantic import BaseModel
from src.schemas.cadastro import CadastroResponse


class AdministradorSalaBase(BaseModel):
    usuario: str
    senha: str
    adm_local: bool = False
    admin_central: bool = False


class AdministradorSalaCreate(AdministradorSalaBase):
    cadastro_id: int


class AdministradorSalaUpdate(BaseModel):
    usuario: Optional[str] = None
    senha: Optional[str] = None
    adm_local: Optional[bool] = None
    admin_central: Optional[bool] = None


class AdministradorSalaResponse(BaseModel):
    admin_id: int
    usuario: str
    adm_local: bool
    admin_central: bool
    cadastro_id: int
    cadastro: Optional[CadastroResponse] = None

    class Config:
        from_attributes = True

