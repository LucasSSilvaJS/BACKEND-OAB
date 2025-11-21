from typing import Optional, List
from datetime import date, datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.sessao_repository import SessaoRepository
from src.repositories.computador_repository import ComputadorRepository
from src.repositories.usuario_advogado_repository import UsuarioAdvogadoRepository
from src.repositories.administrador_sala_repository import AdministradorSalaRepository
from src.schemas.sessao import SessaoCreate, SessaoUpdate, SessaoResponse


class SessaoService:
    def __init__(self, db: Session):
        self.repository = SessaoRepository(db)
        self.computador_repo = ComputadorRepository(db)
        self.usuario_repo = UsuarioAdvogadoRepository(db)
        self.admin_repo = AdministradorSalaRepository(db)

    def criar_sessao(self, sessao: SessaoCreate) -> SessaoResponse:
        # Validar computador
        if not self.computador_repo.get_by_id(sessao.computador_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Computador não encontrado"
            )
        
        # Verificar se computador já está em uso
        sessao_existente = self.repository.get_by_computador(sessao.computador_id)
        if sessao_existente and sessao_existente.ativado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Computador já está em uso"
            )
        
        # Validar usuário
        if not self.usuario_repo.get_by_id(sessao.usuario_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Validar administrador
        if not self.admin_repo.get_by_id(sessao.administrador_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador não encontrado"
            )
        
        sessao_dict = sessao.model_dump(exclude={"analista_ids"})
        db_sessao = self.repository.create(sessao_dict, analista_ids=sessao.analista_ids)
        return SessaoResponse.model_validate(db_sessao)

    def obter_sessao(self, sessao_id: int) -> SessaoResponse:
        db_sessao = self.repository.get_by_id(sessao_id)
        if not db_sessao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessão não encontrada"
            )
        return SessaoResponse.model_validate(db_sessao)

    def listar_sessoes(self, skip: int = 0, limit: int = 100, administrador_id: Optional[int] = None) -> List[SessaoResponse]:
        if administrador_id is not None:
            sessoes = self.repository.get_by_administrador_paginado(administrador_id, skip=skip, limit=limit)
        else:
            sessoes = self.repository.get_all(skip=skip, limit=limit)
        return [SessaoResponse.model_validate(s) for s in sessoes]

    def listar_sessoes_ativas(self) -> List[SessaoResponse]:
        sessoes = self.repository.get_ativas()
        return [SessaoResponse.model_validate(s) for s in sessoes]

    def listar_sessoes_por_usuario(self, usuario_id: int) -> List[SessaoResponse]:
        sessoes = self.repository.get_by_usuario(usuario_id)
        return [SessaoResponse.model_validate(s) for s in sessoes]

    def listar_sessoes_por_data(self, data: date) -> List[SessaoResponse]:
        sessoes = self.repository.get_por_data(data)
        return [SessaoResponse.model_validate(s) for s in sessoes]

    def atualizar_sessao(self, sessao_id: int, sessao: SessaoUpdate) -> SessaoResponse:
        db_sessao = self.repository.get_by_id(sessao_id)
        if not db_sessao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessão não encontrada"
            )
        
        # Validar computador se fornecido
        if sessao.computador_id and sessao.computador_id != db_sessao.computador_id:
            if not self.computador_repo.get_by_id(sessao.computador_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Computador não encontrado"
                )
            # Verificar se novo computador já está em uso
            sessao_existente = self.repository.get_by_computador(sessao.computador_id)
            if sessao_existente and sessao_existente.ativado and sessao_existente.sessao_id != sessao_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Computador já está em uso"
                )
        
        update_dict = sessao.model_dump(exclude_unset=True, exclude={"analista_ids"})
        updated_sessao = self.repository.update(
            db_sessao, 
            update_dict, 
            analista_ids=sessao.analista_ids
        )
        return SessaoResponse.model_validate(updated_sessao)

    def finalizar_sessao(self, sessao_id: int) -> SessaoResponse:
        db_sessao = self.repository.get_by_id(sessao_id)
        if not db_sessao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessão não encontrada"
            )
        
        if db_sessao.final_de_sessao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sessão já foi finalizada"
            )
        
        finalizada = self.repository.finalizar_sessao(db_sessao, datetime.now())
        return SessaoResponse.model_validate(finalizada)

    def desativar_sessao(self, sessao_id: int) -> SessaoResponse:
        db_sessao = self.repository.get_by_id(sessao_id)
        if not db_sessao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessão não encontrada"
            )
        
        if not db_sessao.ativado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sessão já está desativada"
            )
        
        desativada = self.repository.desativar_sessao(db_sessao)
        return SessaoResponse.model_validate(desativada)

    def deletar_sessao(self, sessao_id: int) -> bool:
        db_sessao = self.repository.get_by_id(sessao_id)
        if not db_sessao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessão não encontrada"
            )
        return self.repository.delete(db_sessao)

