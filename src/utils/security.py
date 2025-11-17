import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt

# Configurações JWT
SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas


def _preprocess_password(password: str) -> str:
    """
    Preprocessa a senha antes de passar para bcrypt.
    Bcrypt tem limite de 72 bytes, então aplicamos SHA-256 primeiro
    para garantir que sempre teremos 64 bytes (32 bytes em hex).
    """
    password_bytes = password.encode('utf-8')
    sha256_hash = hashlib.sha256(password_bytes).hexdigest()
    return sha256_hash


def hash_password(password: str) -> str:
    """
    Hasheia uma senha usando SHA-256 + bcrypt.
    Isso garante compatibilidade com senhas de qualquer tamanho,
    já que bcrypt tem limite de 72 bytes.
    
    Args:
        password: Senha em texto plano
    
    Returns:
        Hash bcrypt da senha pré-processada com SHA-256
    """
    preprocessed = _preprocess_password(password)
    # Aplica bcrypt diretamente, usando salt gerado automaticamente
    password_bytes = preprocessed.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde ao hash.
    Aplica o mesmo pré-processamento (SHA-256) antes da verificação.
    
    Args:
        plain: Senha em texto plano
        hashed: Hash bcrypt da senha
    
    Returns:
        True se a senha corresponde ao hash, False caso contrário
    """
    try:
        preprocessed = _preprocess_password(plain)
        password_bytes = preprocessed.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token JWT com os dados fornecidos.
    
    Args:
        data: Dicionário com os dados a serem incluídos no token
        expires_delta: Tempo de expiração do token (opcional)
    
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verifica e decodifica um token JWT.
    
    Args:
        token: Token JWT a ser verificado
    
    Returns:
        Dicionário com os dados do token se válido, None caso contrário
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None