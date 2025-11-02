import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs, unquote


load_dotenv()


# Verificar se DATABASE_URL está definida (suporta PostgreSQL e MySQL)
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Decompor a DATABASE_URL para extrair componentes
    parsed_url = urlparse(DATABASE_URL)
    
    # Extrair componentes da URL
    DB_SCHEME = parsed_url.scheme  # postgresql ou mysql
    DB_USER = unquote(parsed_url.username) if parsed_url.username else None
    DB_PASS = unquote(parsed_url.password) if parsed_url.password else None
    DB_HOST = parsed_url.hostname or "127.0.0.1"
    DB_PORT = parsed_url.port or (5432 if "postgresql" in DB_SCHEME else 3306)
    DB_NAME = parsed_url.path.lstrip('/')  # Remove a barra inicial
    
    # Extrair parâmetros de query (como sslmode, charset, etc.)
    query_params = parse_qs(parsed_url.query)
    
    # Para MySQL, garantir o uso do driver pymysql se não especificado
    if DB_SCHEME == "mysql":
        if not DATABASE_URL.startswith("mysql+pymysql"):
            # Converter mysql:// para mysql+pymysql://
            DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
    elif DB_SCHEME == "postgresql":
        # DATABASE_URL PostgreSQL já está no formato correto
        pass
else:
    # Fallback para variáveis individuais (MySQL por padrão)
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "middleware_oab")
    
    # Construir DATABASE_URL a partir das variáveis individuais
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"


# Criar engine com pool_pre_ping para detectar conexões perdidas
# Adicionar timeout para evitar loading infinito
connect_args = {}
if DATABASE_URL and "postgresql" in DATABASE_URL:
    connect_args = {"connect_timeout": 10}  # Timeout de 10 segundos para PostgreSQL
else:
    connect_args = {"connect_timeout": 10}  # Timeout de 10 segundos para MySQL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args=connect_args,
    pool_timeout=20,  # Timeout de 20 segundos para obter conexão do pool
    pool_recycle=3600,  # Reciclar conexões após 1 hora
)

# Criar SessionLocal para usar como dependência
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)