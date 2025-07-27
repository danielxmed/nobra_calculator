"""
nobra_calculator - API Principal

API modular para cálculos e scores médicos desenvolvida com FastAPI.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importações
sys.path.insert(0, str(Path(__file__).parent))

from app import __version__, __description__
from app.routers import scores_router, health_router

# Configuração da aplicação FastAPI
app = FastAPI(
    title="nobra_calculator",
    description=__description__,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configuração de CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para capturar erros não tratados
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Handler global para capturar exceções não tratadas
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "Erro interno do servidor",
            "details": {
                "path": str(request.url),
                "method": request.method,
                "error": str(exc) if app.debug else "Erro interno"
            }
        }
    )

# Registra os routers
app.include_router(health_router)
app.include_router(scores_router)

# Endpoint raiz
@app.get("/")
async def root():
    """
    Endpoint raiz da API
    
    Returns:
        Dict: Informações básicas da API
    """
    return {
        "name": "nobra_calculator",
        "description": __description__,
        "version": __version__,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "api": "/api"
    }

# Evento de inicialização
@app.on_event("startup")
async def startup_event():
    """
    Evento executado na inicialização da aplicação
    """
    print(f"🚀 nobra_calculator v{__version__} iniciada!")
    print("📋 Documentação disponível em: /docs")
    print("🔍 Redoc disponível em: /redoc")
    print("❤️  Health check disponível em: /health")

# Evento de finalização
@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento executado no shutdown da aplicação
    """
    print("👋 nobra_calculator finalizando...")

if __name__ == "__main__":
    # Configuração para execução local
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Reload automático durante desenvolvimento
        log_level="info"
    )
