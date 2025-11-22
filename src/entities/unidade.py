import os
import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.database.base import Base

# Schema padrão: middleware_oab
SCHEMA_NAME = os.getenv("DB_SCHEMA", "middleware_oab")


class HierarquiaEnum(str, enum.Enum):
    SEDE = "SEDE"
    FILIAL = "FILIAL"


class Unidade(Base):
    __tablename__ = "Unidade"
    __table_args__ = {"schema": SCHEMA_NAME}

    unidade_id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    hierarquia = Column(Enum(HierarquiaEnum), nullable=False)
    endereco = Column(String(255))
    latitude = Column(Float(precision=6))
    longitude = Column(Float(precision=6))
    subsecional_id = Column(Integer, ForeignKey(f"{SCHEMA_NAME}.Subsecional.subsecional_id"))

    subsecional = relationship("Subsecional", back_populates="unidades")
    salas = relationship("Sala_coworking", back_populates="unidade")
