from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.unidade_repository import UnidadeRepository
from src.repositories.subsecional_repository import SubsecionalRepository
from src.schemas.unidade import UnidadeCreate, UnidadeUpdate, UnidadeResponse


class UnidadeService:
    def __init__(self, db: Session):
        self.repository = UnidadeRepository(db)
        self.subsecional_repo = SubsecionalRepository(db)

    def criar_unidade(self, unidade: UnidadeCreate) -> UnidadeResponse:
        # Validar subsecional
        if not self.subsecional_repo.get_by_id(unidade.subsecional_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subsecional não encontrada"
            )
        
        unidade_dict = unidade.model_dump()
        db_unidade = self.repository.create(unidade_dict)
        return UnidadeResponse.model_validate(db_unidade)

    def obter_unidade(self, unidade_id: int) -> UnidadeResponse:
        db_unidade = self.repository.get_by_id(unidade_id)
        if not db_unidade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unidade não encontrada"
            )
        return UnidadeResponse.model_validate(db_unidade)

    def listar_unidades(self, skip: int = 0, limit: int = 100) -> List[UnidadeResponse]:
        unidades = self.repository.get_all(skip=skip, limit=limit)
        return [UnidadeResponse.model_validate(u) for u in unidades]

    def listar_unidades_por_subsecional(self, subsecional_id: int) -> List[UnidadeResponse]:
        unidades = self.repository.get_by_subsecional(subsecional_id)
        return [UnidadeResponse.model_validate(u) for u in unidades]

    def atualizar_unidade(self, unidade_id: int, unidade: UnidadeUpdate) -> UnidadeResponse:
        db_unidade = self.repository.get_by_id(unidade_id)
        if not db_unidade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unidade não encontrada"
            )
        
        # Validar subsecional se fornecido
        if unidade.subsecional_id and not self.subsecional_repo.get_by_id(unidade.subsecional_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subsecional não encontrada"
            )
        
        update_dict = unidade.model_dump(exclude_unset=True)
        updated_unidade = self.repository.update(db_unidade, update_dict)
        return UnidadeResponse.model_validate(updated_unidade)

    def deletar_unidade(self, unidade_id: int) -> bool:
        db_unidade = self.repository.get_by_id(unidade_id)
        if not db_unidade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unidade não encontrada"
            )
        return self.repository.delete(db_unidade)

