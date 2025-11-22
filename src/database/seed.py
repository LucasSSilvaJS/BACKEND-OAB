"""
Funções para popular o banco de dados em massa.
Cada função recebe um array de objetos e insere todos de uma vez.
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database.base import Base
from src.database.connection import engine
from src.entities.cadastro import Cadastro
from src.entities.subsecional import Subsecional
from src.entities.unidade import Unidade
from src.entities.sala_coworking import Sala_coworking
from src.entities.computador import Computador
from src.entities.usuario_advogado import Usuario_advogado
from src.entities.analista_de_ti import Analista_de_ti
from src.entities.administrador_sala_coworking import Administrador_sala_coworking
from src.entities.sessao import Sessao
from src.utils.security import hash_password


def garantir_tabelas_existem():
    """
    Garante que todas as tabelas existam no banco de dados.
    Cria as tabelas se elas não existirem.
    """
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"⚠️ Aviso: Erro ao criar tabelas: {e}")


def popular_cadastros(db: Session, cadastros: List[Dict[str, Any]]) -> List[Cadastro]:
    """
    Popula o banco com múltiplos cadastros.
    
    Args:
        db: Sessão do banco de dados
        cadastros: Lista de dicionários com os dados dos cadastros
                  Exemplo: [{"nome": "João", "email": "joao@email.com", "cpf": "12345678901", ...}, ...]
    
    Returns:
        Lista de objetos Cadastro criados
    """
    garantir_tabelas_existem()
    objetos = []
    for cadastro_data in cadastros:
        try:
            # Remover ID explícito se existir (deixar o banco gerar automaticamente)
            data_clean = {k: v for k, v in cadastro_data.items() if k != "cadastro_id"}
            obj = Cadastro(**data_clean)
            db.add(obj)
            objetos.append(obj)
        except IntegrityError:
            db.rollback()
            continue
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        return objetos
    except IntegrityError as e:
        db.rollback()
        raise e


def popular_subsecionais(db: Session, subsecionais: List[Dict[str, Any]]) -> List[Subsecional]:
    """
    Popula o banco com múltiplas subseccionais.
    
    Args:
        db: Sessão do banco de dados
        subsecionais: Lista de dicionários com os dados das subseccionais
                     Exemplo: [{"nome": "Subsecional 1"}, {"nome": "Subsecional 2"}, ...]
    
    Returns:
        Lista de objetos Subsecional criados
    """
    garantir_tabelas_existem()
    objetos = []
    for subsecional_data in subsecionais:
        try:
            # Remover ID explícito se existir (deixar o banco gerar automaticamente)
            data_clean = {k: v for k, v in subsecional_data.items() if k != "subsecional_id"}
            obj = Subsecional(**data_clean)
            db.add(obj)
            objetos.append(obj)
        except IntegrityError:
            db.rollback()
            continue
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        return objetos
    except IntegrityError as e:
        db.rollback()
        raise e


def popular_unidades(db: Session, unidades: List[Dict[str, Any]]) -> List[Unidade]:
    """
    Popula o banco com múltiplas unidades.
    
    Args:
        db: Sessão do banco de dados
        unidades: Lista de dicionários com os dados das unidades
                  Exemplo: [{"nome": "Unidade 1", "hierarquia": "SEDE", "subsecional_id": 1}, ...]
    
    Returns:
        Lista de objetos Unidade criados
    """
    garantir_tabelas_existem()
    objetos = []
    for unidade_data in unidades:
        try:
            # Remover ID explícito se existir (deixar o banco gerar automaticamente)
            data_clean = {k: v for k, v in unidade_data.items() if k != "unidade_id"}
            obj = Unidade(**data_clean)
            db.add(obj)
            objetos.append(obj)
        except IntegrityError:
            db.rollback()
            continue
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        return objetos
    except IntegrityError as e:
        db.rollback()
        raise e


def popular_salas_coworking(db: Session, salas: List[Dict[str, Any]]) -> List[Sala_coworking]:
    """
    Popula o banco com múltiplas salas de coworking.
    
    Args:
        db: Sessão do banco de dados
        salas: Lista de dicionários com os dados das salas
               Exemplo: [{"nome_da_sala": "Sala 1", "subsecional_id": 1, "unidade_id": 1}, ...]
    
    Returns:
        Lista de objetos Sala_coworking criados
    """
    garantir_tabelas_existem()
    objetos = []
    for sala_data in salas:
        try:
            # Remover ID explícito se existir (deixar o banco gerar automaticamente)
            data_clean = {k: v for k, v in sala_data.items() if k != "coworking_id"}
            obj = Sala_coworking(**data_clean)
            db.add(obj)
            objetos.append(obj)
        except IntegrityError:
            db.rollback()
            continue
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        return objetos
    except IntegrityError as e:
        db.rollback()
        raise e


def popular_computadores(db: Session, computadores: List[Dict[str, Any]]) -> List[Computador]:
    """
    Popula o banco com múltiplos computadores.
    
    Args:
        db: Sessão do banco de dados
        computadores: Lista de dicionários com os dados dos computadores
                      Exemplo: [{"ip_da_maquina": "192.168.1.1", "numero_de_tombamento": "T001", "coworking_id": 1}, ...]
    
    Returns:
        Lista de objetos Computador criados
    """
    garantir_tabelas_existem()
    objetos = []
    for computador_data in computadores:
        try:
            # Remover ID explícito se existir (deixar o banco gerar automaticamente)
            data_clean = {k: v for k, v in computador_data.items() if k != "computador_id"}
            obj = Computador(**data_clean)
            db.add(obj)
            objetos.append(obj)
        except IntegrityError:
            db.rollback()
            continue
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        return objetos
    except IntegrityError as e:
        db.rollback()
        raise e


def popular_usuarios_advogados(db: Session, usuarios: List[Dict[str, Any]]) -> List[Usuario_advogado]:
    """
    Popula o banco com múltiplos usuários advogados.
    
    Args:
        db: Sessão do banco de dados
        usuarios: Lista de dicionários com os dados dos usuários
                  Exemplo: [{"cadastro_id": 1, "registro_oab": "12345", "codigo_de_seguranca": "ABC123", "adimplencia_oab": True}, ...]
    
    Returns:
        Lista de objetos Usuario_advogado criados
    """
    garantir_tabelas_existem()
    objetos = []
    for usuario_data in usuarios:
        try:
            # Remover ID explícito se existir (deixar o banco gerar automaticamente)
            data_clean = {k: v for k, v in usuario_data.items() if k != "usuario_id"}
            obj = Usuario_advogado(**data_clean)
            db.add(obj)
            objetos.append(obj)
        except IntegrityError:
            db.rollback()
            continue
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        return objetos
    except IntegrityError as e:
        db.rollback()
        raise e


def popular_analistas_ti(db: Session, analistas: List[Dict[str, Any]]) -> List[Analista_de_ti]:
    """
    Popula o banco com múltiplos analistas de TI.
    
    Args:
        db: Sessão do banco de dados
        analistas: Lista de dicionários com os dados dos analistas
                   Exemplo: [{"cadastro_id": 1, "usuario": "analista1", "senha": "senha123"}, ...]
    
    Returns:
        Lista de objetos Analista_de_ti criados
    """
    garantir_tabelas_existem()
    objetos = []
    for analista_data in analistas:
        try:
            # Remover ID explícito se existir (deixar o banco gerar automaticamente)
            data_clean = {k: v for k, v in analista_data.items() if k != "analista_id"}
            # Hash da senha se fornecida
            if "senha" in data_clean:
                data_clean["senha"] = hash_password(data_clean["senha"])
            obj = Analista_de_ti(**data_clean)
            db.add(obj)
            objetos.append(obj)
        except IntegrityError:
            db.rollback()
            continue
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        return objetos
    except IntegrityError as e:
        db.rollback()
        raise e


def popular_administradores_sala(db: Session, administradores: List[Dict[str, Any]]) -> List[Administrador_sala_coworking]:
    """
    Popula o banco com múltiplos administradores de sala.
    
    Args:
        db: Sessão do banco de dados
        administradores: Lista de dicionários com os dados dos administradores
                         Exemplo: [{"cadastro_id": 1, "usuario": "admin1", "senha": "senha123"}, ...]
    
    Returns:
        Lista de objetos Administrador_sala_coworking criados
    """
    garantir_tabelas_existem()
    objetos = []
    for admin_data in administradores:
        try:
            # Remover ID explícito se existir (deixar o banco gerar automaticamente)
            data_clean = {k: v for k, v in admin_data.items() if k != "admin_id"}
            # Hash da senha se fornecida
            if "senha" in data_clean:
                data_clean["senha"] = hash_password(data_clean["senha"])
            obj = Administrador_sala_coworking(**data_clean)
            db.add(obj)
            objetos.append(obj)
        except IntegrityError:
            db.rollback()
            continue
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        return objetos
    except IntegrityError as e:
        db.rollback()
        raise e


def popular_sessoes(db: Session, sessoes: List[Dict[str, Any]]) -> List[Sessao]:
    """
    Popula o banco com múltiplas sessões.
    
    Args:
        db: Sessão do banco de dados
        sessoes: Lista de dicionários com os dados das sessões
                 Exemplo: [{"data": "2025-01-01", "inicio_de_sessao": "2025-01-01T08:00:00", 
                          "computador_id": 1, "usuario_id": 1, "administrador_id": 1}, ...]
    
    Returns:
        Lista de objetos Sessao criados
    """
    garantir_tabelas_existem()
    objetos = []
    for sessao_data in sessoes:
        try:
            # Remover ID explícito se existir (deixar o banco gerar automaticamente)
            data_clean = {k: v for k, v in sessao_data.items() if k != "sessao_id"}
            obj = Sessao(**data_clean)
            db.add(obj)
            objetos.append(obj)
        except IntegrityError:
            db.rollback()
            continue
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        return objetos
    except IntegrityError as e:
        db.rollback()
        raise e

