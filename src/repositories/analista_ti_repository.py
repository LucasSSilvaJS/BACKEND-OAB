from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from src.entities.analista_de_ti import Analista_de_ti
from src.repositories.base_repository import BaseRepository


class AnalistaTIRepository(BaseRepository[Analista_de_ti]):
    def __init__(self, db: Session):
        super().__init__(Analista_de_ti, db)

    def get_by_id(self, analista_id: int) -> Optional[Analista_de_ti]:
        return self.db.query(Analista_de_ti).options(
            joinedload(Analista_de_ti.cadastro)
        ).filter(
            Analista_de_ti.analista_id == analista_id
        ).first()

    def get_by_usuario(self, usuario: str) -> Optional[Analista_de_ti]:
        return self.db.query(Analista_de_ti).options(
            joinedload(Analista_de_ti.cadastro)
        ).filter(
            Analista_de_ti.usuario == usuario
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Analista_de_ti]:
        return self.db.query(Analista_de_ti).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> Analista_de_ti:
        return super().create(obj_in)

    def update(self, db_obj: Analista_de_ti, obj_in: dict) -> Analista_de_ti:
        return super().update(db_obj, obj_in)

    def delete(self, db_obj: Analista_de_ti) -> bool:
        return super().delete(db_obj)

