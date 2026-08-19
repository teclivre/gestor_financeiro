from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.categorias import router as categorias_router
from app.api.routes.transacoes import router as transacoes_router

app = FastAPI(
    title="Gestor Financeiro Pessoal",
    version="0.1.0",
    description=(
        "Backend multi-tenant para gestão financeira pessoal com isolamento por "
        "user_id e autenticação JWT."
    ),
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(categorias_router, prefix="/categorias", tags=["categorias"])
app.include_router(transacoes_router, prefix="/transacoes", tags=["transacoes"])


@app.get("/healthz")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
