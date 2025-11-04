from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.administrador_sala_repository import AdministradorSalaRepository
from src.repositories.cadastro_repository import CadastroRepository
from src.schemas.administrador_sala import (
    AdministradorSalaCreate,
    AdministradorSalaUpdate,
    AdministradorSalaResponse
)
from src.utils.security import hash_password


class AdministradorSalaService:
    def __init__(self, db: Session):
        self.repository = AdministradorSalaRepository(db)
        self.cadastro_repo = CadastroRepository(db)

    def criar_administrador(self, administrador: AdministradorSalaCreate) -> AdministradorSalaResponse:
        # Validar cadastro
        if not self.cadastro_repo.get_by_id(administrador.cadastro_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cadastro não encontrado"
            )
        
        # Verificar se usuário já existe
        if self.repository.get_by_usuario(administrador.usuario):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário já cadastrado"
            )
        
        administrador_dict = administrador.model_dump()
        # Hash da senha
        administrador_dict["senha"] = hash_password(administrador_dict["senha"])
        db_administrador = self.repository.create(administrador_dict)
        return AdministradorSalaResponse.model_validate(db_administrador)

    def obter_administrador(self, admin_id: int) -> AdministradorSalaResponse:
        db_administrador = self.repository.get_by_id(admin_id)
        if not db_administrador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador não encontrado"
            )
        return AdministradorSalaResponse.model_validate(db_administrador)

    def listar_administradores(self, skip: int = 0, limit: int = 100) -> List[AdministradorSalaResponse]:
        administradores = self.repository.get_all(skip=skip, limit=limit)
        return [AdministradorSalaResponse.model_validate(a) for a in administradores]

    def atualizar_administrador(
        self,
        admin_id: int,
        administrador: AdministradorSalaUpdate
    ) -> AdministradorSalaResponse:
        db_administrador = self.repository.get_by_id(admin_id)
        if not db_administrador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador não encontrado"
            )
        
        # Verificar se novo usuário já existe
        if administrador.usuario and administrador.usuario != db_administrador.usuario:
            if self.repository.get_by_usuario(administrador.usuario):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Usuário já cadastrado"
                )
        
        update_dict = administrador.model_dump(exclude_unset=True)
        # Hash da senha se fornecida
        if "senha" in update_dict:
            update_dict["senha"] = hash_password(update_dict["senha"])
        
        updated_administrador = self.repository.update(db_administrador, update_dict)
        return AdministradorSalaResponse.model_validate(updated_administrador)

    def deletar_administrador(self, admin_id: int) -> bool:
        db_administrador = self.repository.get_by_id(admin_id)
        if not db_administrador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador não encontrado"
            )
        return self.repository.delete(db_administrador)

