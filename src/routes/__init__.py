from src.routes.cadastro_router import router as cadastro_router
from src.routes.sessao_router import router as sessao_router
from src.routes.computador_router import router as computador_router
from src.routes.sala_coworking_router import router as sala_coworking_router
from src.routes.unidade_router import router as unidade_router
from src.routes.subsecional_router import router as subsecional_router
from src.routes.usuario_advogado_router import router as usuario_advogado_router
from src.routes.analista_ti_router import router as analista_ti_router
from src.routes.administrador_sala_router import router as administrador_sala_router

__all__ = [
    "cadastro_router",
    "sessao_router",
    "computador_router",
    "sala_coworking_router",
    "unidade_router",
    "subsecional_router",
    "usuario_advogado_router",
    "analista_ti_router",
    "administrador_sala_router",
]

