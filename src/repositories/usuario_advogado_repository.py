from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from src.entities.usuario_advogado import Usuario_advogado
from src.repositories.base_repository import BaseRepository


class UsuarioAdvogadoRepository(BaseRepository[Usuario_advogado]):
    def __init__(self, db: Session):
        super().__init__(Usuario_advogado, db)

    def get_by_id(self, usuario_id: int) -> Optional[Usuario_advogado]:
        return self.db.query(Usuario_advogado).options(
            joinedload(Usuario_advogado.cadastro)
        ).filter(
            Usuario_advogado.usuario_id == usuario_id
        ).first()

    def get_by_registro_oab(self, registro_oab: str) -> Optional[Usuario_advogado]:
        return self.db.query(Usuario_advogado).options(
            joinedload(Usuario_advogado.cadastro)
        ).filter(
            Usuario_advogado.registro_oab == registro_oab
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Usuario_advogado]:
        return self.db.query(Usuario_advogado).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> Usuario_advogado:
        return super().create(obj_in)

    def update(self, db_obj: Usuario_advogado, obj_in: dict) -> Usuario_advogado:
        return super().update(db_obj, obj_in)

    def delete(self, db_obj: Usuario_advogado) -> bool:
        return super().delete(db_obj)

