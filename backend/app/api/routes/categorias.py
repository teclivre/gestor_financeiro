from fastapi import APIRouter, HTTPException, Query, status

from app.api.dependencies import CurrentUser, DBSession
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaResponse, CategoriaUpdate

router = APIRouter()


@router.get("", response_model=list[CategoriaResponse])
def list_categorias(
    db: DBSession,
    current_user: CurrentUser,
    tipo: str | None = Query(default=None, pattern="^(receita|despesa)$"),
) -> list[Categoria]:
    query = db.query(Categoria).filter(Categoria.user_id == current_user.id)
    if tipo is not None:
        query = query.filter(Categoria.tipo == tipo)
    return query.order_by(Categoria.nome.asc()).all()


@router.post("", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def create_categoria(
    categoria_in: CategoriaCreate,
    db: DBSession,
    current_user: CurrentUser,
) -> Categoria:
    categoria = Categoria(
        user_id=current_user.id,
        nome=categoria_in.nome.strip(),
        tipo=categoria_in.tipo,
        icone=categoria_in.icone,
    )
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


@router.put("/{categoria_id}", response_model=CategoriaResponse)
def update_categoria(
    categoria_id: int,
    categoria_in: CategoriaUpdate,
    db: DBSession,
    current_user: CurrentUser,
) -> Categoria:
    categoria = (
        db.query(Categoria)
        .filter(Categoria.id == categoria_id, Categoria.user_id == current_user.id)
        .first()
    )
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada para o usuário autenticado.",
        )

    categoria.nome = categoria_in.nome.strip()
    categoria.tipo = categoria_in.tipo
    categoria.icone = categoria_in.icone
    db.commit()
    db.refresh(categoria)
    return categoria


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(
    categoria_id: int,
    db: DBSession,
    current_user: CurrentUser,
) -> None:
    categoria = (
        db.query(Categoria)
        .filter(Categoria.id == categoria_id, Categoria.user_id == current_user.id)
        .first()
    )
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada para o usuário autenticado.",
        )

    db.delete(categoria)
    db.commit()
    return None
