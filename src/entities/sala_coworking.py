from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base


class Sala_coworking(Base):
    __tablename__ = "Sala_coworking"


    coworking_id = Column(Integer, primary_key=True, autoincrement=True)
    nome_da_sala = Column(String(100), nullable=False)
    subsecional_id = Column(Integer, ForeignKey("Subsecional.subsecional_id"))
    unidade_id = Column(Integer, ForeignKey("Unidade.unidade_id"))
    administrador_id = Column(Integer, ForeignKey("Administrador_sala_coworking.admin_id"), nullable=True)


    subsecional = relationship("Subsecional", back_populates="salas")
    unidade = relationship("Unidade", back_populates="salas")
    administrador = relationship("Administrador_sala_coworking", back_populates="sala")
    computadores = relationship("Computador", back_populates="sala")