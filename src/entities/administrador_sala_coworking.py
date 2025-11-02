from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base


class Administrador_sala_coworking(Base):
    __tablename__ = "Administrador_sala_coworking"


    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(50), nullable=False, unique=True)
    senha = Column(String(100), nullable=False)
    adm_local = Column(Boolean, default=False)
    admin_central = Column(Boolean, default=False)
    cadastro_id = Column(Integer, ForeignKey("Cadastro.cadastro_id"))


    cadastro = relationship("Cadastro", back_populates="administrador_sala")
    sala = relationship("Sala_coworking", back_populates="administrador", uselist=False)
    sessoes = relationship("Sessao", back_populates="administrador")