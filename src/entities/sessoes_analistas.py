from sqlalchemy import Table, Column, Integer, ForeignKey
from src.database.base import Base


Sessoes_analistas = Table(
    "Sessoes_analistas",
    Base.metadata,
    Column("analista_id", Integer, ForeignKey("Analista_de_ti.analista_id"), primary_key=True),
    Column("sessao_id", Integer, ForeignKey("Sessao.sessao_id"), primary_key=True)
)