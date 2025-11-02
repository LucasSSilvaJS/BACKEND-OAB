from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class MensagemResponse(BaseModel):
    mensagem: str
    sucesso: bool = True


class ErroResponse(BaseModel):
    mensagem: str
    detalhes: Optional[str] = None
    sucesso: bool = False

