from typing import Optional, List
from sqlalchemy.orm import Session
from src.entities.computador import Computador
from src.repositories.base_repository import BaseRepository


class ComputadorRepository(BaseRepository[Computador]):
    def __init__(self, db: Session):
        super().__init__(Computador, db)

    def get_by_id(self, computador_id: int) -> Optional[Computador]:
        return self.db.query(Computador).filter(
            Computador.computador_id == computador_id
        ).first()

    def get_by_ip(self, ip_da_maquina: str) -> Optional[Computador]:
        return self.db.query(Computador).filter(
            Computador.ip_da_maquina == ip_da_maquina
        ).first()

    def get_by_tombamento(self, numero_de_tombamento: str) -> Optional[Computador]:
        return self.db.query(Computador).filter(
            Computador.numero_de_tombamento == numero_de_tombamento
        ).first()

    def get_by_coworking(self, coworking_id: int) -> List[Computador]:
        return self.db.query(Computador).filter(
            Computador.coworking_id == coworking_id
        ).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Computador]:
        return self.db.query(Computador).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> Computador:
        return super().create(obj_in)

    def update(self, db_obj: Computador, obj_in: dict) -> Computador:
        return super().update(db_obj, obj_in)

    def delete(self, db_obj: Computador) -> bool:
        return super().delete(db_obj)

