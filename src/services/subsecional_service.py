from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.subsecional_repository import SubsecionalRepository
from src.schemas.subsecional import SubsecionalCreate, SubsecionalUpdate, SubsecionalResponse


class SubsecionalService:
    def __init__(self, db: Session):
        self.repository = SubsecionalRepository(db)

    def criar_subsecional(self, subsecional: SubsecionalCreate) -> SubsecionalResponse:
        # Verificar se nome já existe
        if self.repository.get_by_nome(subsecional.nome):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subsecional com este nome já existe"
            )
        
        subsecional_dict = subsecional.model_dump()
        db_subsecional = self.repository.create(subsecional_dict)
        return SubsecionalResponse.model_validate(db_subsecional)

    def obter_subsecional(self, subsecional_id: int) -> SubsecionalResponse:
        db_subsecional = self.repository.get_by_id(subsecional_id)
        if not db_subsecional:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subsecional não encontrada"
            )
        return SubsecionalResponse.model_validate(db_subsecional)

    def listar_subsecionais(self, skip: int = 0, limit: int = 100) -> List[SubsecionalResponse]:
        subsecionais = self.repository.get_all(skip=skip, limit=limit)
        return [SubsecionalResponse.model_validate(s) for s in subsecionais]

    def atualizar_subsecional(self, subsecional_id: int, subsecional: SubsecionalUpdate) -> SubsecionalResponse:
        db_subsecional = self.repository.get_by_id(subsecional_id)
        if not db_subsecional:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subsecional não encontrada"
            )
        
        # Verificar se novo nome já existe
        if subsecional.nome and subsecional.nome != db_subsecional.nome:
            if self.repository.get_by_nome(subsecional.nome):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Subsecional com este nome já existe"
                )
        
        update_dict = subsecional.model_dump(exclude_unset=True)
        updated_subsecional = self.repository.update(db_subsecional, update_dict)
        return SubsecionalResponse.model_validate(updated_subsecional)

    def deletar_subsecional(self, subsecional_id: int) -> bool:
        db_subsecional = self.repository.get_by_id(subsecional_id)
        if not db_subsecional:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subsecional não encontrada"
            )
        return self.repository.delete(db_subsecional)

