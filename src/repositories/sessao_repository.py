from typing import Optional, List
from datetime import date, datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from src.entities.sessao import Sessao
from src.entities.analista_de_ti import Analista_de_ti
from src.entities.computador import Computador
from src.entities.sala_coworking import Sala_coworking
from src.entities.subsecional import Subsecional
from src.entities.unidade import Unidade
from src.entities.usuario_advogado import Usuario_advogado
from src.entities.cadastro import Cadastro
from src.repositories.base_repository import BaseRepository
from src.schemas.filtro_sessao import FiltroSessao, OrdenacaoData


class SessaoRepository(BaseRepository[Sessao]):
    def __init__(self, db: Session):
        super().__init__(Sessao, db)

    def get_by_id(self, sessao_id: int) -> Optional[Sessao]:
        return self.db.query(Sessao).options(
            joinedload(Sessao.computador).joinedload(Computador.sala).joinedload(Sala_coworking.subsecional),
            joinedload(Sessao.computador).joinedload(Computador.sala).joinedload(Sala_coworking.unidade).joinedload(Unidade.subsecional)
        ).filter(Sessao.sessao_id == sessao_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Sessao]:
        return self.db.query(Sessao).options(
            joinedload(Sessao.computador).joinedload(Computador.sala).joinedload(Sala_coworking.subsecional),
            joinedload(Sessao.computador).joinedload(Computador.sala).joinedload(Sala_coworking.unidade).joinedload(Unidade.subsecional)
        ).offset(skip).limit(limit).all()

    def get_by_usuario(self, usuario_id: int) -> List[Sessao]:
        return self.db.query(Sessao).options(
            joinedload(Sessao.computador).joinedload(Computador.sala).joinedload(Sala_coworking.subsecional),
            joinedload(Sessao.computador).joinedload(Computador.sala).joinedload(Sala_coworking.unidade).joinedload(Unidade.subsecional)
        ).filter(Sessao.usuario_id == usuario_id).all()

    def get_by_computador(self, computador_id: int) -> Optional[Sessao]:
        return self.db.query(Sessao).filter(Sessao.computador_id == computador_id).first()

    def get_by_administrador(self, administrador_id: int) -> List[Sessao]:
        return self.db.query(Sessao).filter(Sessao.administrador_id == administrador_id).all()

    def get_by_administrador_paginado(self, administrador_id: int, skip: int = 0, limit: int = 100) -> List[Sessao]:
        return self.db.query(Sessao).options(
            joinedload(Sessao.computador).joinedload(Computador.sala).joinedload(Sala_coworking.subsecional),
            joinedload(Sessao.computador).joinedload(Computador.sala).joinedload(Sala_coworking.unidade).joinedload(Unidade.subsecional)
        ).filter(Sessao.administrador_id == administrador_id).offset(skip).limit(limit).all()

    def get_ativas(self) -> List[Sessao]:
        return self.db.query(Sessao).options(
            joinedload(Sessao.computador).joinedload(Computador.sala).joinedload(Sala_coworking.subsecional),
            joinedload(Sessao.computador).joinedload(Computador.sala).joinedload(Sala_coworking.unidade).joinedload(Unidade.subsecional)
        ).filter(Sessao.ativado == True).all()

    def get_por_data(self, data: date) -> List[Sessao]:
        return self.db.query(Sessao).options(
            joinedload(Sessao.computador).joinedload(Computador.sala).joinedload(Sala_coworking.subsecional),
            joinedload(Sessao.computador).joinedload(Computador.sala).joinedload(Sala_coworking.unidade).joinedload(Unidade.subsecional)
        ).filter(Sessao.data == data).all()

    def filtrar_sessoes(self, filtros: FiltroSessao) -> List[Sessao]:
        """Método robusto para filtrar sessões com múltiplos critérios"""
        # Inicializar query base
        query = self.db.query(Sessao)
        
        # Flags para controlar joins necessários (evitar duplicatas)
        ja_fez_join_computador = False
        ja_fez_join_usuario = False
        
        # Aplicar filtros
        filtros_aplicados = []
        
        # Filtro por administrador
        if filtros.administrador_id is not None:
            filtros_aplicados.append(Sessao.administrador_id == filtros.administrador_id)
        
        # Filtro por data específica (campo 'data' da sessão)
        if filtros.data_especifica is not None:
            filtros_aplicados.append(Sessao.data == filtros.data_especifica)
        
        # Filtro por hora de início (DateTime) - usado junto com data_especifica
        if filtros.inicio is not None:
            filtros_aplicados.append(Sessao.inicio_de_sessao == filtros.inicio)
        
        # Filtro por hora de finalização (DateTime) - usado junto com data_especifica
        if filtros.finalizacao is not None:
            filtros_aplicados.append(Sessao.final_de_sessao == filtros.finalizacao)
        
        # Filtro por IP do computador (busca parcial) - precisa de join explícito
        if filtros.ip_computador:
            if not ja_fez_join_computador:
                query = query.join(Computador, Sessao.computador_id == Computador.computador_id)
                ja_fez_join_computador = True
            filtros_aplicados.append(
                Computador.ip_da_maquina.ilike(f"%{filtros.ip_computador}%")
            )
        
        # Filtro por sessões ativas
        if filtros.apenas_ativas is not None:
            if filtros.apenas_ativas:
                # Apenas sessões ativas (ativado=True e final_de_sessao IS NULL)
                filtros_aplicados.append(
                    and_(
                        Sessao.ativado == True,
                        Sessao.final_de_sessao.is_(None)
                    )
                )
            else:
                # Apenas sessões inativas (ativado=False OU final_de_sessao IS NOT NULL)
                filtros_aplicados.append(
                    or_(
                        Sessao.ativado == False,
                        Sessao.final_de_sessao.isnot(None)
                    )
                )
        
        # Aplicar todos os filtros
        if filtros_aplicados:
            query = query.filter(and_(*filtros_aplicados))
        
        # Ordenação
        if filtros.ordenar_por_usuario:
            # Precisamos fazer join com usuário e cadastro para ordenar por nome
            if not ja_fez_join_usuario:
                query = query.join(Usuario_advogado, Sessao.usuario_id == Usuario_advogado.usuario_id)
                ja_fez_join_usuario = True
            query = query.join(Cadastro, Usuario_advogado.cadastro_id == Cadastro.cadastro_id)
            query = query.order_by(Cadastro.nome.asc())
        elif filtros.ordenar_por_data == OrdenacaoData.MAIS_RECENTE_PRIMEIRO:
            # Mais recente primeiro (DESC)
            query = query.order_by(Sessao.inicio_de_sessao.desc())
        elif filtros.ordenar_por_data == OrdenacaoData.MAIS_ANTIGA_PRIMEIRO:
            # Mais antiga primeiro (ASC)
            query = query.order_by(Sessao.inicio_de_sessao.asc())
        
        # Paginação
        query = query.offset(filtros.skip).limit(filtros.limit)
        
        # Carregar relacionamentos necessários com joinedload (para evitar N+1 queries)
        # Usar distinct() para evitar duplicatas causadas por joins
        query = query.distinct().options(
            joinedload(Sessao.computador).joinedload(Computador.sala).joinedload(Sala_coworking.subsecional),
            joinedload(Sessao.computador).joinedload(Computador.sala).joinedload(Sala_coworking.unidade).joinedload(Unidade.subsecional),
            joinedload(Sessao.usuario).joinedload(Usuario_advogado.cadastro)
        )
        
        return query.all()

    def create(self, obj_in: dict, analista_ids: Optional[List[int]] = None) -> Sessao:
        db_obj = Sessao(**obj_in)
        if analista_ids:
            analistas = self.db.query(Analista_de_ti).filter(
                Analista_de_ti.analista_id.in_(analista_ids)
            ).all()
            db_obj.analistas = analistas
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: Sessao, obj_in: dict, analista_ids: Optional[List[int]] = None) -> Sessao:
        for field, value in obj_in.items():
            if field != "analista_ids":
                setattr(db_obj, field, value)
        
        if analista_ids is not None:
            analistas = self.db.query(Analista_de_ti).filter(
                Analista_de_ti.analista_id.in_(analista_ids)
            ).all()
            db_obj.analistas = analistas
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def finalizar_sessao(self, sessao: Sessao, final_de_sessao: datetime) -> Sessao:
        sessao.final_de_sessao = final_de_sessao
        sessao.ativado = False
        self.db.commit()
        self.db.refresh(sessao)
        return sessao

    def desativar_sessao(self, sessao: Sessao) -> Sessao:
        sessao.ativado = False
        self.db.commit()
        self.db.refresh(sessao)
        return sessao

    def delete(self, db_obj: Sessao) -> bool:
        return super().delete(db_obj)

