from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from src.entities.administrador_sala_coworking import Administrador_sala_coworking
from src.repositories.base_repository import BaseRepository


class AdministradorSalaRepository(BaseRepository[Administrador_sala_coworking]):
    def __init__(self, db: Session):
        super().__init__(Administrador_sala_coworking, db)

    def get_by_id(self, admin_id: int) -> Optional[Administrador_sala_coworking]:
        return self.db.query(Administrador_sala_coworking).options(
            joinedload(Administrador_sala_coworking.cadastro)
        ).filter(
            Administrador_sala_coworking.admin_id == admin_id
        ).first()

    def get_by_usuario(self, usuario: str) -> Optional[Administrador_sala_coworking]:
        return self.db.query(Administrador_sala_coworking).options(
            joinedload(Administrador_sala_coworking.cadastro)
        ).filter(
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

    def get_vinculacao_completa(self, admin_id: int) -> Optional[dict]:
        """Retorna os IDs e nomes vinculados ao administrador (coworking, unidade, subsecional)"""
        from src.entities.sala_coworking import Sala_coworking
        
        administrador = self.get_by_id(admin_id)
        if not administrador:
            return None
        
        # Buscar sala vinculada ao administrador com relacionamentos
        sala = self.db.query(Sala_coworking).options(
            joinedload(Sala_coworking.unidade),
            joinedload(Sala_coworking.subsecional)
        ).filter(
            Sala_coworking.administrador_id == admin_id
        ).first()
        
        if not sala:
            return {
                "coworking": None,
                "unidade": None,
                "subsecional": None
            }
        
        resultado = {
            "coworking": {
                "id": sala.coworking_id,
                "nome": sala.nome_da_sala
            },
            "unidade": None,
            "subsecional": None
        }
        
        # Buscar informações da unidade
        if sala.unidade:
            resultado["unidade"] = {
                "id": sala.unidade.unidade_id,
                "nome": sala.unidade.nome
            }
        
        # Buscar informações da subsecional
        if sala.subsecional:
            resultado["subsecional"] = {
                "id": sala.subsecional.subsecional_id,
                "nome": sala.subsecional.nome
            }
        
        return resultado

