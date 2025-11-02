from typing import Optional, List
from sqlalchemy.orm import Session
from src.entities.sala_coworking import Sala_coworking
from src.repositories.base_repository import BaseRepository


class SalaCoworkingRepository(BaseRepository[Sala_coworking]):
    def __init__(self, db: Session):
        super().__init__(Sala_coworking, db)

    def get_by_id(self, coworking_id: int) -> Optional[Sala_coworking]:
        return self.db.query(Sala_coworking).filter(
            Sala_coworking.coworking_id == coworking_id
        ).first()

    def get_by_subsecional(self, subsecional_id: int) -> List[Sala_coworking]:
        return self.db.query(Sala_coworking).filter(
            Sala_coworking.subsecional_id == subsecional_id
        ).all()

    def get_by_unidade(self, unidade_id: int) -> List[Sala_coworking]:
        return self.db.query(Sala_coworking).filter(
            Sala_coworking.unidade_id == unidade_id
        ).all()

    def get_by_administrador(self, administrador_id: int) -> List[Sala_coworking]:
        return self.db.query(Sala_coworking).filter(
            Sala_coworking.administrador_id == administrador_id
        ).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Sala_coworking]:
        return self.db.query(Sala_coworking).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> Sala_coworking:
        return super().create(obj_in)

    def update(self, db_obj: Sala_coworking, obj_in: dict) -> Sala_coworking:
        return super().update(db_obj, obj_in)

    def delete(self, db_obj: Sala_coworking) -> bool:
        return super().delete(db_obj)

