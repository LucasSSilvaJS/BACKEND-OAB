# Como Usar o Sistema de Autenticação

Este documento explica como usar o sistema de autenticação nas rotas da API.

## Endpoints de Login

### Login de Advogado
```
POST /api/v1/auth/login/advogado
Body: {
    "registro_oab": "123456",
    "codigo_de_seguranca": "ABC123"
}
```

### Login de Administrador
```
POST /api/v1/auth/login/administrador
Body: {
    "usuario": "admin",
    "senha": "senha123"
}
```

### Login de Analista
```
POST /api/v1/auth/login/analista
Body: {
    "usuario": "analista",
    "senha": "senha123"
}
```

## Protegendo Rotas

Para proteger uma rota, adicione a dependência de autenticação:

```python
from src.routes.auth_dependencies import (
    get_current_user,
    require_advogado,
    require_administrador,
    require_analista,
    require_any_user  # Qualquer usuário autenticado
)

# Exemplo: Qualquer usuário autenticado pode acessar
@router.get("/endpoint")
def meu_endpoint(
    current_user: AuthUser = Depends(require_any_user),
    db: Session = Depends(get_db)
):
    # Seu código aqui
    pass

# Exemplo: Apenas advogados podem acessar
@router.get("/endpoint")
def meu_endpoint(
    current_user: AuthUser = Depends(require_advogado),
    db: Session = Depends(get_db)
):
    # Seu código aqui
    pass

# Exemplo: Administradores ou Analistas podem acessar
@router.get("/endpoint")
def meu_endpoint(
    current_user: AuthUser = Depends(require_administrador_or_analista),
    db: Session = Depends(get_db)
):
    # Seu código aqui
    pass
```

## Usando o Token

Após fazer login, você receberá um token. Use este token no header das requisições:

```
Authorization: Bearer <seu_token_aqui>
```

## Dependências Disponíveis

- `require_any_user`: Qualquer usuário autenticado (ADVOGADO, ADMINISTRADOR ou ANALISTA)
- `require_advogado`: Apenas advogados
- `require_administrador`: Apenas administradores
- `require_analista`: Apenas analistas
- `require_advogado_or_administrador`: Advogados ou administradores
- `require_advogado_or_analista`: Advogados ou analistas
- `require_administrador_or_analista`: Administradores ou analistas

