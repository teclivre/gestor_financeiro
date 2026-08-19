from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class TransacaoCreate(BaseModel):
    categoria_id: int | None = None
    descricao: str = Field(..., min_length=1, max_length=255)
    valor: Decimal = Field(..., gt=0)
    data: date
    tipo: str = Field(..., pattern="^(receita|despesa)$")


class TransacaoUpdate(BaseModel):
    categoria_id: int | None = None
    descricao: str | None = Field(default=None, min_length=1, max_length=255)
    valor: Decimal | None = Field(default=None, gt=0)
    data: date | None = None
    tipo: str | None = Field(default=None, pattern="^(receita|despesa)$")


class TransacaoResponse(BaseModel):
    id: int
    user_id: int
    categoria_id: int | None = None
    descricao: str
    valor: Decimal
    data: date
    tipo: str

    class Config:
        from_attributes = True
