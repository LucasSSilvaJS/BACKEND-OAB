from typing import Optional, List
from sqlalchemy.orm import Session
from src.entities.subsecional import Subsecional
from src.repositories.base_repository import BaseRepository


class SubsecionalRepository(BaseRepository[Subsecional]):
    def __init__(self, db: Session):
        super().__init__(Subsecional, db)

    def get_by_id(self, subsecional_id: int) -> Optional[Subsecional]:
        return self.db.query(Subsecional).filter(
            Subsecional.subsecional_id == subsecional_id
        ).first()

    def get_by_nome(self, nome: str) -> Optional[Subsecional]:
        return self.db.query(Subsecional).filter(
            Subsecional.nome == nome
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Subsecional]:
        return self.db.query(Subsecional).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> Subsecional:
        return super().create(obj_in)

    def update(self, db_obj: Subsecional, obj_in: dict) -> Subsecional:
        return super().update(db_obj, obj_in)

    def delete(self, db_obj: Subsecional) -> bool:
        return super().delete(db_obj)

