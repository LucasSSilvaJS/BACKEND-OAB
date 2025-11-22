import os
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base

# Schema padrão: middleware_oab
SCHEMA_NAME = os.getenv("DB_SCHEMA", "middleware_oab")


class Analista_de_ti(Base):
    __tablename__ = "Analista_de_ti"
    __table_args__ = {"schema": SCHEMA_NAME}


    analista_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(50), nullable=False, unique=True)
    senha = Column(String(100), nullable=False)
    cadastro_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.Cadastro.cadastro_id"))


    cadastro = relationship("Cadastro", back_populates="analista_ti")
    sessoes = relationship("Sessao", secondary=f"{SCHEMA_NAME}.Sessoes_analistas", back_populates="analistas")