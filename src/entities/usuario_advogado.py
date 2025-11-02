from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base


class Usuario_advogado(Base):
    __tablename__ = "Usuario_advogado"


    usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    registro_oab = Column(String(20), nullable=False, unique=True)
    codigo_de_seguranca = Column(String(50), nullable=False)
    adimplencia_oab = Column(Boolean, default=True)
    cadastro_id = Column(Integer, ForeignKey("Cadastro.cadastro_id"))


    cadastro = relationship("Cadastro", back_populates="usuario_advogado")
    sessao = relationship("Sessao", back_populates="usuario", uselist=False)