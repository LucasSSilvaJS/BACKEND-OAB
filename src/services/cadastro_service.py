from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.cadastro_repository import CadastroRepository
from src.schemas.cadastro import CadastroCreate, CadastroUpdate, CadastroResponse


class CadastroService:
    def __init__(self, db: Session):
        self.repository = CadastroRepository(db)

    def criar_cadastro(self, cadastro: CadastroCreate) -> CadastroResponse:
        # Verificar se email já existe
        if self.repository.get_by_email(cadastro.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        
        # Verificar se CPF já existe
        if self.repository.get_by_cpf(cadastro.cpf):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF já cadastrado"
            )
        
        cadastro_dict = cadastro.model_dump()
        db_cadastro = self.repository.create(cadastro_dict)
        return CadastroResponse.model_validate(db_cadastro)

    def obter_cadastro(self, cadastro_id: int) -> CadastroResponse:
        db_cadastro = self.repository.get_by_id(cadastro_id)
        if not db_cadastro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cadastro não encontrado"
            )
        return CadastroResponse.model_validate(db_cadastro)

    def listar_cadastros(self, skip: int = 0, limit: int = 100) -> List[CadastroResponse]:
        cadastros = self.repository.get_all(skip=skip, limit=limit)
        return [CadastroResponse.model_validate(c) for c in cadastros]

    def atualizar_cadastro(self, cadastro_id: int, cadastro: CadastroUpdate) -> CadastroResponse:
        db_cadastro = self.repository.get_by_id(cadastro_id)
        if not db_cadastro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cadastro não encontrado"
            )
        
        # Verificar se novo email já existe
        if cadastro.email and cadastro.email != db_cadastro.email:
            if self.repository.get_by_email(cadastro.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado"
                )
        
        update_dict = cadastro.model_dump(exclude_unset=True)
        updated_cadastro = self.repository.update(db_cadastro, update_dict)
        return CadastroResponse.model_validate(updated_cadastro)

    def deletar_cadastro(self, cadastro_id: int) -> bool:
        db_cadastro = self.repository.get_by_id(cadastro_id)
        if not db_cadastro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cadastro não encontrado"
            )
        return self.repository.delete(db_cadastro)

    def obter_por_email(self, email: str) -> Optional[CadastroResponse]:
        db_cadastro = self.repository.get_by_email(email)
        if db_cadastro:
            return CadastroResponse.model_validate(db_cadastro)
        return None

    def obter_por_cpf(self, cpf: str) -> Optional[CadastroResponse]:
        db_cadastro = self.repository.get_by_cpf(cpf)
        if db_cadastro:
            return CadastroResponse.model_validate(db_cadastro)
        return None

