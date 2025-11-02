from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from src.database.base import Base


class Cadastro(Base):
    __tablename__ = "Cadastro"


    cadastro_id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    telefone = Column(String(15))
    cpf = Column(String(14), nullable=False, unique=True)
    rg = Column(String(20))
    endereco = Column(String(255))
    data_cadastro = Column(DateTime, server_default=func.now())


    usuario_advogado = relationship("Usuario_advogado", back_populates="cadastro", uselist=False)
    analista_ti = relationship("Analista_de_ti", back_populates="cadastro", uselist=False)
    administrador_sala = relationship("Administrador_sala_coworking", back_populates="cadastro", uselist=False)