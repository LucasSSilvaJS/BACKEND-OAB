from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.sala_coworking_repository import SalaCoworkingRepository
from src.repositories.subsecional_repository import SubsecionalRepository
from src.repositories.unidade_repository import UnidadeRepository
from src.repositories.administrador_sala_repository import AdministradorSalaRepository
from src.schemas.sala_coworking import SalaCoworkingCreate, SalaCoworkingUpdate, SalaCoworkingResponse


class SalaCoworkingService:
    def __init__(self, db: Session):
        self.repository = SalaCoworkingRepository(db)
        self.subsecional_repo = SubsecionalRepository(db)
        self.unidade_repo = UnidadeRepository(db)
        self.admin_repo = AdministradorSalaRepository(db)

    def criar_sala(self, sala: SalaCoworkingCreate) -> SalaCoworkingResponse:
        # Validar subsecional
        if not self.subsecional_repo.get_by_id(sala.subsecional_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subsecional não encontrada"
            )
        
        # Validar unidade
        if not self.unidade_repo.get_by_id(sala.unidade_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unidade não encontrada"
            )
        
        # Validar administrador se fornecido
        if sala.administrador_id and not self.admin_repo.get_by_id(sala.administrador_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador não encontrado"
            )
        
        sala_dict = sala.model_dump()
        db_sala = self.repository.create(sala_dict)
        return SalaCoworkingResponse.model_validate(db_sala)

    def obter_sala(self, coworking_id: int) -> SalaCoworkingResponse:
        db_sala = self.repository.get_by_id(coworking_id)
        if not db_sala:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sala de coworking não encontrada"
            )
        return SalaCoworkingResponse.model_validate(db_sala)

    def listar_salas(self, skip: int = 0, limit: int = 100) -> List[SalaCoworkingResponse]:
        salas = self.repository.get_all(skip=skip, limit=limit)
        return [SalaCoworkingResponse.model_validate(s) for s in salas]

    def listar_salas_por_subsecional(self, subsecional_id: int) -> List[SalaCoworkingResponse]:
        salas = self.repository.get_by_subsecional(subsecional_id)
        return [SalaCoworkingResponse.model_validate(s) for s in salas]

    def listar_salas_por_unidade(self, unidade_id: int) -> List[SalaCoworkingResponse]:
        salas = self.repository.get_by_unidade(unidade_id)
        return [SalaCoworkingResponse.model_validate(s) for s in salas]

    def listar_salas_por_subsecional_e_unidade(self, subsecional_id: int, unidade_id: int) -> List[SalaCoworkingResponse]:
        salas = self.repository.get_by_subsecional_e_unidade(subsecional_id, unidade_id)
        return [SalaCoworkingResponse.model_validate(s) for s in salas]

    def atualizar_sala(self, coworking_id: int, sala: SalaCoworkingUpdate) -> SalaCoworkingResponse:
        db_sala = self.repository.get_by_id(coworking_id)
        if not db_sala:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sala de coworking não encontrada"
            )
        
        # Validar subsecional se fornecido
        if sala.subsecional_id and not self.subsecional_repo.get_by_id(sala.subsecional_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subsecional não encontrada"
            )
        
        # Validar unidade se fornecido
        if sala.unidade_id and not self.unidade_repo.get_by_id(sala.unidade_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unidade não encontrada"
            )
        
        # Validar administrador se fornecido
        if sala.administrador_id and not self.admin_repo.get_by_id(sala.administrador_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador não encontrado"
            )
        
        update_dict = sala.model_dump(exclude_unset=True)
        updated_sala = self.repository.update(db_sala, update_dict)
        return SalaCoworkingResponse.model_validate(updated_sala)

    def deletar_sala(self, coworking_id: int) -> bool:
        db_sala = self.repository.get_by_id(coworking_id)
        if not db_sala:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sala de coworking não encontrada"
            )
        return self.repository.delete(db_sala)

