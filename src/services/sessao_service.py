from typing import Optional, List
from datetime import date, datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.sessao_repository import SessaoRepository
from src.repositories.computador_repository import ComputadorRepository
from src.repositories.usuario_advogado_repository import UsuarioAdvogadoRepository
from src.repositories.administrador_sala_repository import AdministradorSalaRepository
from src.schemas.sessao import SessaoCreate, SessaoUpdate, SessaoResponse
from src.schemas.filtro_sessao import FiltroSessao


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
        # Recarregar a sessão com as relações
        db_sessao = self.repository.get_by_id(db_sessao.sessao_id)
        return self._sessao_to_response(db_sessao)

    def obter_sessao(self, sessao_id: int) -> SessaoResponse:
        db_sessao = self.repository.get_by_id(sessao_id)
        if not db_sessao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessão não encontrada"
            )
        return self._sessao_to_response(db_sessao)

    def _sessao_to_response(self, sessao) -> SessaoResponse:
        """Converte uma sessão em SessaoResponse com informações relacionadas."""
        response_dict = {
            "sessao_id": sessao.sessao_id,
            "data": sessao.data,
            "inicio_de_sessao": sessao.inicio_de_sessao,
            "final_de_sessao": sessao.final_de_sessao,
            "ativado": sessao.ativado,
            "computador_id": sessao.computador_id,
            "usuario_id": sessao.usuario_id,
            "administrador_id": sessao.administrador_id,
            "sala_coworking": None,
            "unidade": None,
            "subsecional": None
        }
        
        # Adicionar informações da sala, unidade e subseccional se disponíveis
        if sessao.computador and sessao.computador.sala:
            sala = sessao.computador.sala
            response_dict["sala_coworking"] = {
                "coworking_id": sala.coworking_id,
                "nome_da_sala": sala.nome_da_sala
            }
            
            if sala.unidade:
                response_dict["unidade"] = {
                    "unidade_id": sala.unidade.unidade_id,
                    "nome": sala.unidade.nome
                }
                
                # Tentar buscar subseccional através da unidade
                if sala.unidade.subsecional:
                    response_dict["subsecional"] = {
                        "subsecional_id": sala.unidade.subsecional.subsecional_id,
                        "nome": sala.unidade.subsecional.nome
                    }
            
            # Se não achou pela unidade, tentar direto pela sala
            if not response_dict["subsecional"] and sala.subsecional:
                response_dict["subsecional"] = {
                    "subsecional_id": sala.subsecional.subsecional_id,
                    "nome": sala.subsecional.nome
                }
        
        return SessaoResponse.model_validate(response_dict)

    def listar_sessoes(self, filtros: FiltroSessao) -> List[SessaoResponse]:
        """Lista sessões com filtros robustos"""
        sessoes = self.repository.filtrar_sessoes(filtros)
        return [self._sessao_to_response(s) for s in sessoes]

    def listar_sessoes_ativas(self) -> List[SessaoResponse]:
        sessoes = self.repository.get_ativas()
        return [self._sessao_to_response(s) for s in sessoes]

    def listar_sessoes_por_usuario(self, usuario_id: int) -> List[SessaoResponse]:
        sessoes = self.repository.get_by_usuario(usuario_id)
        return [self._sessao_to_response(s) for s in sessoes]

    def listar_sessoes_por_data(self, data: date) -> List[SessaoResponse]:
        sessoes = self.repository.get_por_data(data)
        return [self._sessao_to_response(s) for s in sessoes]

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
        # Recarregar a sessão com as relações
        updated_sessao = self.repository.get_by_id(updated_sessao.sessao_id)
        return self._sessao_to_response(updated_sessao)

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
        # Recarregar a sessão com as relações
        finalizada = self.repository.get_by_id(finalizada.sessao_id)
        return self._sessao_to_response(finalizada)

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
        # Recarregar a sessão com as relações
        desativada = self.repository.get_by_id(desativada.sessao_id)
        return self._sessao_to_response(desativada)

    def deletar_sessao(self, sessao_id: int) -> bool:
        db_sessao = self.repository.get_by_id(sessao_id)
        if not db_sessao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessão não encontrada"
            )
        return self.repository.delete(db_sessao)

