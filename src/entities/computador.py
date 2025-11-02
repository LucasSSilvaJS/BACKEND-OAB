from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base


class Computador(Base):
    __tablename__ = "Computador"


    computador_id = Column(Integer, primary_key=True, autoincrement=True)
    ip_da_maquina = Column(String(15), nullable=False, unique=True)
    numero_de_tombamento = Column(String(50), nullable=False, unique=True)
    coworking_id = Column(Integer, ForeignKey("Sala_coworking.coworking_id"))


    sala = relationship("Sala_coworking", back_populates="computadores")
    sessao = relationship("Sessao", back_populates="computador", uselist=False)