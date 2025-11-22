import os
from sqlalchemy import Table, Column, Integer, ForeignKey
from src.database.base import Base

# Schema padrão: middleware_oab
SCHEMA_NAME = os.getenv("DB_SCHEMA", "middleware_oab")


Sessoes_analistas = Table(
    "Sessoes_analistas",
    Base.metadata,
    Column("analista_id", Integer, ForeignKey(f"{SCHEMA_NAME}.Analista_de_ti.analista_id"), primary_key=True),
    Column("sessao_id", Integer, ForeignKey(f"{SCHEMA_NAME}.Sessao.sessao_id"), primary_key=True),
    schema=SCHEMA_NAME
)