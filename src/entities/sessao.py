from sqlalchemy import Column, Integer, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base


class Sessao(Base):
    __tablename__ = "Sessao"


    sessao_id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    inicio_de_sessao = Column(DateTime, nullable=False)
    final_de_sessao = Column(DateTime, nullable=True)
    ativado = Column(Boolean, default=True)
    computador_id = Column(Integer, ForeignKey("Computador.computador_id"))
    usuario_id = Column(Integer, ForeignKey("Usuario_advogado.usuario_id"))
    administrador_id = Column(Integer, ForeignKey("Administrador_sala_coworking.admin_id"))


    computador = relationship("Computador", back_populates="sessao")
    usuario = relationship("Usuario_advogado", back_populates="sessao")
    administrador = relationship("Administrador_sala_coworking", back_populates="sessoes")
    analistas = relationship("Analista_de_ti", secondary="Sessoes_analistas", back_populates="sessoes")