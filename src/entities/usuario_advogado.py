import os
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base

# Schema padrão: middleware_oab
SCHEMA_NAME = os.getenv("DB_SCHEMA", "middleware_oab")


class Usuario_advogado(Base):
    __tablename__ = "Usuario_advogado"
    __table_args__ = {"schema": SCHEMA_NAME}


    usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    registro_oab = Column(String(20), nullable=False, unique=True)
    codigo_de_seguranca = Column(String(50), nullable=False)
    adimplencia_oab = Column(Boolean, default=True)
    cadastro_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.Cadastro.cadastro_id"))


    cadastro = relationship("Cadastro", back_populates="usuario_advogado")
    sessao = relationship("Sessao", back_populates="usuario", uselist=False)