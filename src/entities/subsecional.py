from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.base import Base


class Subsecional(Base):
    __tablename__ = "Subsecional"


    subsecional_id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)


    unidades = relationship("Unidade", back_populates="subsecional")
    salas = relationship("Sala_coworking", back_populates="subsecional")