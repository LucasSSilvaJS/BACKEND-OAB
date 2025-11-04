from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.analista_ti_repository import AnalistaTIRepository
from src.repositories.cadastro_repository import CadastroRepository
from src.schemas.analista_de_ti import AnalistaTCreate, AnalistaTUpdate, AnalistaTResponse
from src.utils.security import hash_password


class AnalistaTIService:
    def __init__(self, db: Session):
        self.repository = AnalistaTIRepository(db)
        self.cadastro_repo = CadastroRepository(db)

    def criar_analista(self, analista: AnalistaTCreate) -> AnalistaTResponse:
        # Validar cadastro
        if not self.cadastro_repo.get_by_id(analista.cadastro_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cadastro não encontrado"
            )
        
        # Verificar se usuário já existe
        if self.repository.get_by_usuario(analista.usuario):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário já cadastrado"
            )
        
        analista_dict = analista.model_dump()
        # Hash da senha
        analista_dict["senha"] = hash_password(analista_dict["senha"])
        db_analista = self.repository.create(analista_dict)
        return AnalistaTResponse.model_validate(db_analista)

    def obter_analista(self, analista_id: int) -> AnalistaTResponse:
        db_analista = self.repository.get_by_id(analista_id)
        if not db_analista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analista de TI não encontrado"
            )
        return AnalistaTResponse.model_validate(db_analista)

    def listar_analistas(self, skip: int = 0, limit: int = 100) -> List[AnalistaTResponse]:
        analistas = self.repository.get_all(skip=skip, limit=limit)
        return [AnalistaTResponse.model_validate(a) for a in analistas]

    def atualizar_analista(self, analista_id: int, analista: AnalistaTUpdate) -> AnalistaTResponse:
        db_analista = self.repository.get_by_id(analista_id)
        if not db_analista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analista de TI não encontrado"
            )
        
        # Verificar se novo usuário já existe
        if analista.usuario and analista.usuario != db_analista.usuario:
            if self.repository.get_by_usuario(analista.usuario):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Usuário já cadastrado"
                )
        
        update_dict = analista.model_dump(exclude_unset=True)
        # Hash da senha se fornecida
        if "senha" in update_dict:
            update_dict["senha"] = hash_password(update_dict["senha"])
        
        updated_analista = self.repository.update(db_analista, update_dict)
        return AnalistaTResponse.model_validate(updated_analista)

    def deletar_analista(self, analista_id: int) -> bool:
        db_analista = self.repository.get_by_id(analista_id)
        if not db_analista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analista de TI não encontrado"
            )
        return self.repository.delete(db_analista)

