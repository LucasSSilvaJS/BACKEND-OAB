from typing import Optional, List
from datetime import date, datetime
from sqlalchemy.orm import Session, joinedload
from src.entities.sessao import Sessao
from src.entities.analista_de_ti import Analista_de_ti
from src.repositories.base_repository import BaseRepository


class SessaoRepository(BaseRepository[Sessao]):
    def __init__(self, db: Session):
        super().__init__(Sessao, db)

    def get_by_id(self, sessao_id: int) -> Optional[Sessao]:
        return self.db.query(Sessao).options(
            joinedload(Sessao.computador).joinedload('sala').joinedload('subsecional'),
            joinedload(Sessao.computador).joinedload('sala').joinedload('unidade')
        ).filter(Sessao.sessao_id == sessao_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Sessao]:
        return self.db.query(Sessao).options(
            joinedload(Sessao.computador).joinedload('sala').joinedload('subsecional'),
            joinedload(Sessao.computador).joinedload('sala').joinedload('unidade')
        ).offset(skip).limit(limit).all()

    def get_by_usuario(self, usuario_id: int) -> List[Sessao]:
        return self.db.query(Sessao).options(
            joinedload(Sessao.computador).joinedload('sala').joinedload('subsecional'),
            joinedload(Sessao.computador).joinedload('sala').joinedload('unidade')
        ).filter(Sessao.usuario_id == usuario_id).all()

    def get_by_computador(self, computador_id: int) -> Optional[Sessao]:
        return self.db.query(Sessao).filter(Sessao.computador_id == computador_id).first()

    def get_by_administrador(self, administrador_id: int) -> List[Sessao]:
        return self.db.query(Sessao).filter(Sessao.administrador_id == administrador_id).all()

    def get_by_administrador_paginado(self, administrador_id: int, skip: int = 0, limit: int = 100) -> List[Sessao]:
        return self.db.query(Sessao).options(
            joinedload(Sessao.computador).joinedload('sala').joinedload('subsecional'),
            joinedload(Sessao.computador).joinedload('sala').joinedload('unidade')
        ).filter(Sessao.administrador_id == administrador_id).offset(skip).limit(limit).all()

    def get_ativas(self) -> List[Sessao]:
        return self.db.query(Sessao).options(
            joinedload(Sessao.computador).joinedload('sala').joinedload('subsecional'),
            joinedload(Sessao.computador).joinedload('sala').joinedload('unidade')
        ).filter(Sessao.ativado == True).all()

    def get_por_data(self, data: date) -> List[Sessao]:
        return self.db.query(Sessao).options(
            joinedload(Sessao.computador).joinedload('sala').joinedload('subsecional'),
            joinedload(Sessao.computador).joinedload('sala').joinedload('unidade')
        ).filter(Sessao.data == data).all()

    def create(self, obj_in: dict, analista_ids: Optional[List[int]] = None) -> Sessao:
        db_obj = Sessao(**obj_in)
        if analista_ids:
            analistas = self.db.query(Analista_de_ti).filter(
                Analista_de_ti.analista_id.in_(analista_ids)
            ).all()
            db_obj.analistas = analistas
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: Sessao, obj_in: dict, analista_ids: Optional[List[int]] = None) -> Sessao:
        for field, value in obj_in.items():
            if field != "analista_ids":
                setattr(db_obj, field, value)
        
        if analista_ids is not None:
            analistas = self.db.query(Analista_de_ti).filter(
                Analista_de_ti.analista_id.in_(analista_ids)
            ).all()
            db_obj.analistas = analistas
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def finalizar_sessao(self, sessao: Sessao, final_de_sessao: datetime) -> Sessao:
        sessao.final_de_sessao = final_de_sessao
        sessao.ativado = False
        self.db.commit()
        self.db.refresh(sessao)
        return sessao

    def desativar_sessao(self, sessao: Sessao) -> Sessao:
        sessao.ativado = False
        self.db.commit()
        self.db.refresh(sessao)
        return sessao

    def delete(self, db_obj: Sessao) -> bool:
        return super().delete(db_obj)

