import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.connection import engine
from src.database.base import Base

# Importar todos os routers
from src.routes import (
    cadastro_router,
    sessao_router,
    computador_router,
    sala_coworking_router,
    unidade_router,
    subsecional_router,
    usuario_advogado_router,
    analista_ti_router,
    administrador_sala_router,
)
from src.routes.auth_router import router as auth_router
from src.routes.dashboard_router import router as dashboard_router
from src.routes.relatorio_router import router as relatorio_router
from src.routes.seed_router import router as seed_router

# Importar todas as entities para garantir que as tabelas sejam criadas
from src.entities import (
    Cadastro,
    Usuario_advogado,
    Analista_de_ti,
    Administrador_sala_coworking,
    Computador,
    Sala_coworking,
    Sessao,
    Unidade,
    Subsecional,
    Sessoes_analistas,
)

app = FastAPI(
    title="Middleware OAB API",
    description="""
    API REST para gerenciamento de salas de coworking da OAB.
    
    ## Funcionalidades
    
    Esta API permite gerenciar:
    
    * **Cadastros**: Gerenciamento de cadastros de pessoas (advogados, analistas, administradores)
    * **Sessões**: Controle de sessões de uso de computadores
    * **Computadores**: Cadastro e gerenciamento de computadores
    * **Salas de Coworking**: Gerenciamento de salas de coworking
    * **Unidades**: Gerenciamento de unidades (SEDE ou FILIAL)
    * **Subsecionais**: Gerenciamento de subsecionais
    * **Usuários Advogados**: Gerenciamento de usuários advogados
    
    ## Documentação Interativa
    
    Esta documentação é gerada automaticamente pelo Swagger/OpenAPI.
    Você pode testar os endpoints diretamente da interface.
    """,
    version="1.0.0",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Servidor de desenvolvimento (localhost)"
        },
        {
            "url": api_url,
            "description": "Servidor de produção"
        }
    ] if (api_url := os.getenv("API_URL")) else [
        {
            "url": "http://localhost:8000",
            "description": "Servidor de desenvolvimento"
        }
    ],
    contact={
        "name": "Suporte OAB",
        "email": "suporte@oab.org.br",
    },
    license_info={
        "name": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todos os routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(relatorio_router, prefix="/api/v1")
app.include_router(cadastro_router, prefix="/api/v1")
app.include_router(sessao_router, prefix="/api/v1")
app.include_router(computador_router, prefix="/api/v1")
app.include_router(sala_coworking_router, prefix="/api/v1")
app.include_router(unidade_router, prefix="/api/v1")
app.include_router(subsecional_router, prefix="/api/v1")
app.include_router(usuario_advogado_router, prefix="/api/v1")
app.include_router(analista_ti_router, prefix="/api/v1")
app.include_router(administrador_sala_router, prefix="/api/v1")
app.include_router(seed_router, prefix="/api/v1")


@app.get(
    "/",
    summary="Endpoint raiz",
    description="Endpoint inicial da API. Retorna informações básicas sobre a API.",
    tags=["Geral"]
)
def root():
    """
    Endpoint raiz da API.
    
    Retorna informações básicas sobre a API e links para documentação.
    """
    return {
        "mensagem": "Bem-vindo à API do Middleware OAB",
        "versao": "1.0.0",
        "documentacao": "/docs",
        "documentacao_alternativa": "/redoc",
        "health_check": "/health"
    }


@app.get(
    "/health",
    summary="Health Check",
    description="Verifica o status da API. Útil para monitoramento e balanceadores de carga.",
    tags=["Geral"]
)
def health_check():
    """
    Endpoint de verificação de saúde da API.
    
    Retorna o status da API. Use este endpoint para verificar se a API está funcionando corretamente.
    """
    return {"status": "ok", "mensagem": "API está funcionando corretamente"}


@app.on_event("startup")
async def startup_event():
    """
    Evento executado quando a aplicação inicia.
    Cria as tabelas do banco de dados se não existirem.
    """
    try:
        # Criar tabelas apenas se a conexão for bem-sucedida
        # Usar run_in_executor para não bloquear o loop de eventos
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        def create_tables():
            Base.metadata.create_all(bind=engine)
        
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            await loop.run_in_executor(executor, create_tables)
        print("✅ Tabelas do banco de dados verificadas/criadas com sucesso")
    except Exception as e:
        print(f"⚠️ Aviso: Não foi possível criar tabelas automaticamente: {e}")
        print("💡 Certifique-se de que o banco de dados está acessível e configurado corretamente")

