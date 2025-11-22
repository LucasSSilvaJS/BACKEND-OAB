import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.base import Base

# Schema padrão: middleware_oab
SCHEMA_NAME = os.getenv("DB_SCHEMA", "middleware_oab")


class Subsecional(Base):
    __tablename__ = "Subsecional"
    __table_args__ = {"schema": SCHEMA_NAME}


    subsecional_id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)


    unidades = relationship("Unidade", back_populates="subsecional")
    salas = relationship("Sala_coworking", back_populates="subsecional")