from typing import Optional, List
from sqlalchemy.orm import Session
from src.entities.administrador_sala_coworking import Administrador_sala_coworking
from src.repositories.base_repository import BaseRepository


class AdministradorSalaRepository(BaseRepository[Administrador_sala_coworking]):
    def __init__(self, db: Session):
        super().__init__(Administrador_sala_coworking, db)

    def get_by_id(self, admin_id: int) -> Optional[Administrador_sala_coworking]:
        return self.db.query(Administrador_sala_coworking).filter(
            Administrador_sala_coworking.admin_id == admin_id
        ).first()

    def get_by_usuario(self, usuario: str) -> Optional[Administrador_sala_coworking]:
        return self.db.query(Administrador_sala_coworking).filter(
            Administrador_sala_coworking.usuario == usuario
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Administrador_sala_coworking]:
        return self.db.query(Administrador_sala_coworking).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> Administrador_sala_coworking:
        return super().create(obj_in)

    def update(self, db_obj: Administrador_sala_coworking, obj_in: dict) -> Administrador_sala_coworking:
        return super().update(db_obj, obj_in)

    def delete(self, db_obj: Administrador_sala_coworking) -> bool:
        return super().delete(db_obj)

