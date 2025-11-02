from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.computador_repository import ComputadorRepository
from src.schemas.computador import ComputadorCreate, ComputadorUpdate, ComputadorResponse


class ComputadorService:
    def __init__(self, db: Session):
        self.repository = ComputadorRepository(db)

    def criar_computador(self, computador: ComputadorCreate) -> ComputadorResponse:
        # Verificar se IP já existe
        if self.repository.get_by_ip(computador.ip_da_maquina):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="IP já cadastrado"
            )
        
        # Verificar se número de tombamento já existe
        if self.repository.get_by_tombamento(computador.numero_de_tombamento):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Número de tombamento já cadastrado"
            )
        
        computador_dict = computador.model_dump()
        db_computador = self.repository.create(computador_dict)
        return ComputadorResponse.model_validate(db_computador)

    def obter_computador(self, computador_id: int) -> ComputadorResponse:
        db_computador = self.repository.get_by_id(computador_id)
        if not db_computador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Computador não encontrado"
            )
        return ComputadorResponse.model_validate(db_computador)

    def listar_computadores(self, skip: int = 0, limit: int = 100) -> List[ComputadorResponse]:
        computadores = self.repository.get_all(skip=skip, limit=limit)
        return [ComputadorResponse.model_validate(c) for c in computadores]

    def listar_computadores_por_coworking(self, coworking_id: int) -> List[ComputadorResponse]:
        computadores = self.repository.get_by_coworking(coworking_id)
        return [ComputadorResponse.model_validate(c) for c in computadores]

    def atualizar_computador(self, computador_id: int, computador: ComputadorUpdate) -> ComputadorResponse:
        db_computador = self.repository.get_by_id(computador_id)
        if not db_computador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Computador não encontrado"
            )
        
        # Verificar se novo IP já existe
        if computador.ip_da_maquina and computador.ip_da_maquina != db_computador.ip_da_maquina:
            if self.repository.get_by_ip(computador.ip_da_maquina):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="IP já cadastrado"
                )
        
        # Verificar se novo número de tombamento já existe
        if computador.numero_de_tombamento and computador.numero_de_tombamento != db_computador.numero_de_tombamento:
            if self.repository.get_by_tombamento(computador.numero_de_tombamento):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Número de tombamento já cadastrado"
                )
        
        update_dict = computador.model_dump(exclude_unset=True)
        updated_computador = self.repository.update(db_computador, update_dict)
        return ComputadorResponse.model_validate(updated_computador)

    def deletar_computador(self, computador_id: int) -> bool:
        db_computador = self.repository.get_by_id(computador_id)
        if not db_computador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Computador não encontrado"
            )
        return self.repository.delete(db_computador)

