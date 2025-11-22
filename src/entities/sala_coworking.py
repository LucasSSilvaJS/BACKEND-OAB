import os
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base

# Schema padrão: middleware_oab
SCHEMA_NAME = os.getenv("DB_SCHEMA", "middleware_oab")


class Sala_coworking(Base):
    __tablename__ = "Sala_coworking"
    __table_args__ = {"schema": SCHEMA_NAME}


    coworking_id = Column(Integer, primary_key=True, autoincrement=True)
    nome_da_sala = Column(String(100), nullable=False)
    subsecional_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.Subsecional.subsecional_id"))
    unidade_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.Unidade.unidade_id"))
    administrador_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.Administrador_sala_coworking.admin_id"), nullable=True)


    subsecional = relationship("Subsecional", back_populates="salas")
    unidade = relationship("Unidade", back_populates="salas")
    administrador = relationship("Administrador_sala_coworking", back_populates="sala")
    computadores = relationship("Computador", back_populates="sala")