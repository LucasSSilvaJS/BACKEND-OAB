from typing import Optional
from pydantic import BaseModel
from src.schemas.cadastro import CadastroResponse


class AnalistaTBase(BaseModel):
    usuario: str
    senha: str


class AnalistaTCreate(AnalistaTBase):
    cadastro_id: int


class AnalistaTUpdate(BaseModel):
    usuario: Optional[str] = None
    senha: Optional[str] = None


class AnalistaTResponse(BaseModel):
    analista_id: int
    usuario: str
    cadastro_id: int
    cadastro: Optional[CadastroResponse] = None

    class Config:
        from_attributes = True

