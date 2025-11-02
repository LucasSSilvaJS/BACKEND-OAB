from sqlalchemy.orm import Session
from src.database.connection import SessionLocal


def get_db():
    """
    Dependência para obter uma sessão do banco de dados.
    
    Cria uma nova sessão do banco de dados para cada requisição
    e fecha automaticamente após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

