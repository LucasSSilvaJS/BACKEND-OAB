from typing import Optional, List
from sqlalchemy.orm import Session
from src.entities.cadastro import Cadastro
from src.repositories.base_repository import BaseRepository


class CadastroRepository(BaseRepository[Cadastro]):
    def __init__(self, db: Session):
        super().__init__(Cadastro, db)

    def get_by_id(self, cadastro_id: int) -> Optional[Cadastro]:
        return self.db.query(Cadastro).filter(Cadastro.cadastro_id == cadastro_id).first()

    def get_by_email(self, email: str) -> Optional[Cadastro]:
        return self.db.query(Cadastro).filter(Cadastro.email == email).first()

    def get_by_cpf(self, cpf: str) -> Optional[Cadastro]:
        return self.db.query(Cadastro).filter(Cadastro.cpf == cpf).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Cadastro]:
        return self.db.query(Cadastro).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> Cadastro:
        return super().create(obj_in)

    def update(self, db_obj: Cadastro, obj_in: dict) -> Cadastro:
        return super().update(db_obj, obj_in)

    def delete(self, db_obj: Cadastro) -> bool:
        return super().delete(db_obj)

