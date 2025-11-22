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
    
    Raises:
        ValueError: Se a unidade não pertencer à subsecional informada
    """
    garantir_tabelas_existem()
    objetos = []
    erros = []
    
    for idx, sala_data in enumerate(salas):
        try:
            # Validar se subsecional existe
            subsecional_id = sala_data.get("subsecional_id")
            unidade_id = sala_data.get("unidade_id")
            
            if subsecional_id is None or unidade_id is None:
                erros.append(f"Sala {idx + 1}: subsecional_id e unidade_id são obrigatórios")
                continue
            
            # Verificar se a subsecional existe
            subsecional = db.query(Subsecional).filter(
                Subsecional.subsecional_id == subsecional_id
            ).first()
            
            if not subsecional:
                erros.append(f"Sala {idx + 1}: Subsecional com ID {subsecional_id} não encontrada")
                continue
            
            # Verificar se a unidade existe
            unidade = db.query(Unidade).filter(
                Unidade.unidade_id == unidade_id
            ).first()
            
            if not unidade:
                erros.append(f"Sala {idx + 1}: Unidade com ID {unidade_id} não encontrada")
                continue
            
            # VALIDAÇÃO CRÍTICA: Verificar se a unidade pertence à subsecional
            if unidade.subsecional_id != subsecional_id:
                erros.append(
                    f"Sala {idx + 1}: A unidade {unidade_id} não pertence à subsecional {subsecional_id}. "
                    f"A unidade pertence à subsecional {unidade.subsecional_id}"
                )
                continue
            
            # Remover ID explícito se existir (deixar o banco gerar automaticamente)
            data_clean = {k: v for k, v in sala_data.items() if k != "coworking_id"}
            obj = Sala_coworking(**data_clean)
            db.add(obj)
            objetos.append(obj)
        except IntegrityError:
            db.rollback()
            erros.append(f"Sala {idx + 1}: Erro de integridade (possível duplicação)")
            continue
        except Exception as e:
            db.rollback()
            erros.append(f"Sala {idx + 1}: Erro inesperado - {str(e)}")
            continue
    
    if erros and not objetos:
        # Se nenhum objeto foi criado e há erros, levantar exceção
        raise ValueError(f"Erro ao popular salas de coworking:\n" + "\n".join(erros))
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        
        if erros:
            # Se alguns objetos foram criados mas houve erros, retornar com aviso
            print(f"⚠️ Aviso: {len(objetos)} sala(s) criada(s), mas {len(erros)} erro(s) ocorreram:")
            for erro in erros:
                print(f"  - {erro}")
        
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
    
    Raises:
        ValueError: Se a sala de coworking não existir
    """
    garantir_tabelas_existem()
    objetos = []
    erros = []
    
    for idx, computador_data in enumerate(computadores):
        try:
            # Validar se coworking_id existe
            coworking_id = computador_data.get("coworking_id")
            
            if coworking_id is None:
                erros.append(f"Computador {idx + 1}: coworking_id é obrigatório")
                continue
            
            # Verificar se a sala de coworking existe
            sala = db.query(Sala_coworking).filter(
                Sala_coworking.coworking_id == coworking_id
            ).first()
            
            if not sala:
                erros.append(f"Computador {idx + 1}: Sala de coworking com ID {coworking_id} não encontrada")
                continue
            
            # Remover ID explícito se existir (deixar o banco gerar automaticamente)
            data_clean = {k: v for k, v in computador_data.items() if k != "computador_id"}
            obj = Computador(**data_clean)
            db.add(obj)
            objetos.append(obj)
        except IntegrityError:
            db.rollback()
            erros.append(f"Computador {idx + 1}: Erro de integridade (possível duplicação de IP ou tombamento)")
            continue
        except Exception as e:
            db.rollback()
            erros.append(f"Computador {idx + 1}: Erro inesperado - {str(e)}")
            continue
    
    if erros and not objetos:
        # Se nenhum objeto foi criado e há erros, levantar exceção
        raise ValueError(f"Erro ao popular computadores:\n" + "\n".join(erros))
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        
        if erros:
            # Se alguns objetos foram criados mas houve erros, retornar com aviso
            print(f"⚠️ Aviso: {len(objetos)} computador(es) criado(s), mas {len(erros)} erro(s) ocorreram:")
            for erro in erros:
                print(f"  - {erro}")
        
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
    
    Raises:
        ValueError: Se o cadastro não existir
    """
    garantir_tabelas_existem()
    objetos = []
    erros = []
    
    for idx, usuario_data in enumerate(usuarios):
        try:
            # Validar se cadastro_id existe
            cadastro_id = usuario_data.get("cadastro_id")
            
            if cadastro_id is None:
                erros.append(f"Usuário advogado {idx + 1}: cadastro_id é obrigatório")
                continue
            
            # Verificar se o cadastro existe
            cadastro = db.query(Cadastro).filter(
                Cadastro.cadastro_id == cadastro_id
            ).first()
            
            if not cadastro:
                erros.append(f"Usuário advogado {idx + 1}: Cadastro com ID {cadastro_id} não encontrado")
                continue
            
            # Remover ID explícito se existir (deixar o banco gerar automaticamente)
            data_clean = {k: v for k, v in usuario_data.items() if k != "usuario_id"}
            obj = Usuario_advogado(**data_clean)
            db.add(obj)
            objetos.append(obj)
        except IntegrityError:
            db.rollback()
            erros.append(f"Usuário advogado {idx + 1}: Erro de integridade (possível duplicação de registro_oab)")
            continue
        except Exception as e:
            db.rollback()
            erros.append(f"Usuário advogado {idx + 1}: Erro inesperado - {str(e)}")
            continue
    
    if erros and not objetos:
        # Se nenhum objeto foi criado e há erros, levantar exceção
        raise ValueError(f"Erro ao popular usuários advogados:\n" + "\n".join(erros))
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        
        if erros:
            # Se alguns objetos foram criados mas houve erros, retornar com aviso
            print(f"⚠️ Aviso: {len(objetos)} usuário(s) advogado(s) criado(s), mas {len(erros)} erro(s) ocorreram:")
            for erro in erros:
                print(f"  - {erro}")
        
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
    
    Raises:
        ValueError: Se o cadastro não existir
    """
    garantir_tabelas_existem()
    objetos = []
    erros = []
    
    for idx, analista_data in enumerate(analistas):
        try:
            # Validar se cadastro_id existe
            cadastro_id = analista_data.get("cadastro_id")
            
            if cadastro_id is None:
                erros.append(f"Analista de TI {idx + 1}: cadastro_id é obrigatório")
                continue
            
            # Verificar se o cadastro existe
            cadastro = db.query(Cadastro).filter(
                Cadastro.cadastro_id == cadastro_id
            ).first()
            
            if not cadastro:
                erros.append(f"Analista de TI {idx + 1}: Cadastro com ID {cadastro_id} não encontrado")
                continue
            
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
            erros.append(f"Analista de TI {idx + 1}: Erro de integridade (possível duplicação de usuário)")
            continue
        except Exception as e:
            db.rollback()
            erros.append(f"Analista de TI {idx + 1}: Erro inesperado - {str(e)}")
            continue
    
    if erros and not objetos:
        # Se nenhum objeto foi criado e há erros, levantar exceção
        raise ValueError(f"Erro ao popular analistas de TI:\n" + "\n".join(erros))
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        
        if erros:
            # Se alguns objetos foram criados mas houve erros, retornar com aviso
            print(f"⚠️ Aviso: {len(objetos)} analista(s) de TI criado(s), mas {len(erros)} erro(s) ocorreram:")
            for erro in erros:
                print(f"  - {erro}")
        
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
    
    Raises:
        ValueError: Se o cadastro não existir
    """
    garantir_tabelas_existem()
    objetos = []
    erros = []
    
    for idx, admin_data in enumerate(administradores):
        try:
            # Validar se cadastro_id existe
            cadastro_id = admin_data.get("cadastro_id")
            
            if cadastro_id is None:
                erros.append(f"Administrador {idx + 1}: cadastro_id é obrigatório")
                continue
            
            # Verificar se o cadastro existe
            cadastro = db.query(Cadastro).filter(
                Cadastro.cadastro_id == cadastro_id
            ).first()
            
            if not cadastro:
                erros.append(f"Administrador {idx + 1}: Cadastro com ID {cadastro_id} não encontrado")
                continue
            
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
            erros.append(f"Administrador {idx + 1}: Erro de integridade (possível duplicação de usuário)")
            continue
        except Exception as e:
            db.rollback()
            erros.append(f"Administrador {idx + 1}: Erro inesperado - {str(e)}")
            continue
    
    if erros and not objetos:
        # Se nenhum objeto foi criado e há erros, levantar exceção
        raise ValueError(f"Erro ao popular administradores de sala:\n" + "\n".join(erros))
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        
        if erros:
            # Se alguns objetos foram criados mas houve erros, retornar com aviso
            print(f"⚠️ Aviso: {len(objetos)} administrador(es) criado(s), mas {len(erros)} erro(s) ocorreram:")
            for erro in erros:
                print(f"  - {erro}")
        
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
    
    Raises:
        ValueError: Se computador, usuário ou administrador não existirem
    """
    garantir_tabelas_existem()
    objetos = []
    erros = []
    
    for idx, sessao_data in enumerate(sessoes):
        try:
            # Validar campos obrigatórios
            computador_id = sessao_data.get("computador_id")
            usuario_id = sessao_data.get("usuario_id")
            administrador_id = sessao_data.get("administrador_id")
            
            if computador_id is None:
                erros.append(f"Sessão {idx + 1}: computador_id é obrigatório")
                continue
            
            if usuario_id is None:
                erros.append(f"Sessão {idx + 1}: usuario_id é obrigatório")
                continue
            
            if administrador_id is None:
                erros.append(f"Sessão {idx + 1}: administrador_id é obrigatório")
                continue
            
            # Verificar se o computador existe
            computador = db.query(Computador).filter(
                Computador.computador_id == computador_id
            ).first()
            
            if not computador:
                erros.append(f"Sessão {idx + 1}: Computador com ID {computador_id} não encontrado")
                continue
            
            # Verificar se o usuário advogado existe
            usuario = db.query(Usuario_advogado).filter(
                Usuario_advogado.usuario_id == usuario_id
            ).first()
            
            if not usuario:
                erros.append(f"Sessão {idx + 1}: Usuário advogado com ID {usuario_id} não encontrado")
                continue
            
            # Verificar se o administrador existe
            administrador = db.query(Administrador_sala_coworking).filter(
                Administrador_sala_coworking.admin_id == administrador_id
            ).first()
            
            if not administrador:
                erros.append(f"Sessão {idx + 1}: Administrador com ID {administrador_id} não encontrado")
                continue
            
            # Remover ID explícito se existir (deixar o banco gerar automaticamente)
            data_clean = {k: v for k, v in sessao_data.items() if k != "sessao_id"}
            obj = Sessao(**data_clean)
            db.add(obj)
            objetos.append(obj)
        except IntegrityError:
            db.rollback()
            erros.append(f"Sessão {idx + 1}: Erro de integridade")
            continue
        except Exception as e:
            db.rollback()
            erros.append(f"Sessão {idx + 1}: Erro inesperado - {str(e)}")
            continue
    
    if erros and not objetos:
        # Se nenhum objeto foi criado e há erros, levantar exceção
        raise ValueError(f"Erro ao popular sessões:\n" + "\n".join(erros))
    
    try:
        db.commit()
        for obj in objetos:
            db.refresh(obj)
        
        if erros:
            # Se alguns objetos foram criados mas houve erros, retornar com aviso
            print(f"⚠️ Aviso: {len(objetos)} sessão(ões) criada(s), mas {len(erros)} erro(s) ocorreram:")
            for erro in erros:
                print(f"  - {erro}")
        
        return objetos
    except IntegrityError as e:
        db.rollback()
        raise e

