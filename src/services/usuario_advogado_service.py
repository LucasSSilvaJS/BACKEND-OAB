from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.usuario_advogado_repository import UsuarioAdvogadoRepository
from src.repositories.cadastro_repository import CadastroRepository
from src.schemas.usuario_advogado import UsuarioAdvogadoCreate, UsuarioAdvogadoUpdate, UsuarioAdvogadoResponse


class UsuarioAdvogadoService:
    def __init__(self, db: Session):
        self.repository = UsuarioAdvogadoRepository(db)
        self.cadastro_repo = CadastroRepository(db)

    def criar_usuario(self, usuario: UsuarioAdvogadoCreate) -> UsuarioAdvogadoResponse:
        # Validar cadastro
        if not self.cadastro_repo.get_by_id(usuario.cadastro_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cadastro não encontrado"
            )
        
        # Verificar se registro OAB já existe
        if self.repository.get_by_registro_oab(usuario.registro_oab):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registro OAB já cadastrado"
            )
        
        usuario_dict = usuario.model_dump()
        db_usuario = self.repository.create(usuario_dict)
        return UsuarioAdvogadoResponse.model_validate(db_usuario)

    def obter_usuario(self, usuario_id: int) -> UsuarioAdvogadoResponse:
        db_usuario = self.repository.get_by_id(usuario_id)
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário advogado não encontrado"
            )
        return UsuarioAdvogadoResponse.model_validate(db_usuario)

    def listar_usuarios(self, skip: int = 0, limit: int = 100) -> List[UsuarioAdvogadoResponse]:
        usuarios = self.repository.get_all(skip=skip, limit=limit)
        return [UsuarioAdvogadoResponse.model_validate(u) for u in usuarios]

    def atualizar_usuario(self, usuario_id: int, usuario: UsuarioAdvogadoUpdate) -> UsuarioAdvogadoResponse:
        db_usuario = self.repository.get_by_id(usuario_id)
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário advogado não encontrado"
            )
        
        # Verificar se novo registro OAB já existe
        if usuario.registro_oab and usuario.registro_oab != db_usuario.registro_oab:
            if self.repository.get_by_registro_oab(usuario.registro_oab):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Registro OAB já cadastrado"
                )
        
        update_dict = usuario.model_dump(exclude_unset=True)
        updated_usuario = self.repository.update(db_usuario, update_dict)
        return UsuarioAdvogadoResponse.model_validate(updated_usuario)

    def deletar_usuario(self, usuario_id: int) -> bool:
        db_usuario = self.repository.get_by_id(usuario_id)
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário advogado não encontrado"
            )
        return self.repository.delete(db_usuario)

