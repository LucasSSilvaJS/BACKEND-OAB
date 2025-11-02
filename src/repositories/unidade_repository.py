from typing import Optional, List
from sqlalchemy.orm import Session
from src.entities.unidade import Unidade
from src.repositories.base_repository import BaseRepository


class UnidadeRepository(BaseRepository[Unidade]):
    def __init__(self, db: Session):
        super().__init__(Unidade, db)

    def get_by_id(self, unidade_id: int) -> Optional[Unidade]:
        return self.db.query(Unidade).filter(
            Unidade.unidade_id == unidade_id
        ).first()

    def get_by_subsecional(self, subsecional_id: int) -> List[Unidade]:
        return self.db.query(Unidade).filter(
            Unidade.subsecional_id == subsecional_id
        ).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Unidade]:
        return self.db.query(Unidade).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> Unidade:
        return super().create(obj_in)

    def update(self, db_obj: Unidade, obj_in: dict) -> Unidade:
        return super().update(db_obj, obj_in)

    def delete(self, db_obj: Unidade) -> bool:
        return super().delete(db_obj)

