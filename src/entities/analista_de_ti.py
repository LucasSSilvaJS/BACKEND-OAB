from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base


class Analista_de_ti(Base):
    __tablename__ = "Analista_de_ti"


    analista_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(50), nullable=False, unique=True)
    senha = Column(String(100), nullable=False)
    cadastro_id = Column(Integer, ForeignKey("Cadastro.cadastro_id"))


    cadastro = relationship("Cadastro", back_populates="analista_ti")
    sessoes = relationship("Sessao", secondary="Sessoes_analistas", back_populates="analistas")