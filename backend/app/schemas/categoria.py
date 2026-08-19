from pydantic import BaseModel, Field


class CategoriaCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=150)
    tipo: str = Field(..., pattern="^(receita|despesa)$")
    icone: str | None = Field(default=None, max_length=50)


class CategoriaUpdate(CategoriaCreate):
    pass


class CategoriaResponse(BaseModel):
    id: int
    user_id: int
    nome: str
    tipo: str
    icone: str | None = None

    class Config:
        from_attributes = True
