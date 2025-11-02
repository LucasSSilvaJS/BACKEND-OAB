from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class CadastroBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    cpf: str
    rg: Optional[str] = None
    endereco: Optional[str] = None


class CadastroCreate(CadastroBase):
    pass


class CadastroUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    rg: Optional[str] = None
    endereco: Optional[str] = None


class CadastroResponse(CadastroBase):
    cadastro_id: int
    data_cadastro: datetime

    class Config:
        from_attributes = True

