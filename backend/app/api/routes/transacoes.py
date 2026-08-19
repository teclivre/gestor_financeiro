from decimal import Decimal

from fastapi import APIRouter, HTTPException, Query, status

from app.api.dependencies import CurrentUser, DBSession
from app.models.categoria import Categoria
from app.models.transacao import Transacao
from app.schemas.transacao import TransacaoCreate, TransacaoResponse, TransacaoUpdate

router = APIRouter()


@router.get("", response_model=list[TransacaoResponse])
def list_transacoes(
    db: DBSession,
    current_user: CurrentUser,
    categoria_id: int | None = Query(default=None),
    tipo: str | None = Query(default=None, pattern="^(receita|despesa)$"),
) -> list[Transacao]:
    query = db.query(Transacao).filter(Transacao.user_id == current_user.id)

    if categoria_id is not None:
        query = query.filter(Transacao.categoria_id == categoria_id)
    if tipo is not None:
        query = query.filter(Transacao.tipo == tipo)

    return query.order_by(Transacao.data.desc(), Transacao.id.desc()).all()


@router.post("", response_model=TransacaoResponse, status_code=status.HTTP_201_CREATED)
def create_transacao(
    transacao_in: TransacaoCreate,
    db: DBSession,
    current_user: CurrentUser,
) -> Transacao:
    if transacao_in.categoria_id is not None:
        categoria = (
            db.query(Categoria)
            .filter(Categoria.id == transacao_in.categoria_id, Categoria.user_id == current_user.id)
            .first()
        )
        if categoria is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Categoria não pertence ao usuário autenticado.",
            )

    transacao = Transacao(
        user_id=current_user.id,
        categoria_id=transacao_in.categoria_id,
        descricao=transacao_in.descricao.strip(),
        valor=Decimal(str(transacao_in.valor)),
        data=transacao_in.data,
        tipo=transacao_in.tipo,
    )
    db.add(transacao)
    db.commit()
    db.refresh(transacao)
    return transacao


@router.put("/{transacao_id}", response_model=TransacaoResponse)
def update_transacao(
    transacao_id: int,
    transacao_in: TransacaoUpdate,
    db: DBSession,
    current_user: CurrentUser,
) -> Transacao:
    transacao = (
        db.query(Transacao)
        .filter(Transacao.id == transacao_id, Transacao.user_id == current_user.id)
        .first()
    )
    if transacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transação não encontrada para o usuário autenticado.",
        )

    if transacao_in.categoria_id is not None:
        categoria = (
            db.query(Categoria)
            .filter(Categoria.id == transacao_in.categoria_id, Categoria.user_id == current_user.id)
            .first()
        )
        if categoria is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Categoria não pertence ao usuário autenticado.",
            )
        transacao.categoria_id = transacao_in.categoria_id

    if transacao_in.descricao is not None:
        transacao.descricao = transacao_in.descricao.strip()
    if transacao_in.valor is not None:
        transacao.valor = Decimal(str(transacao_in.valor))
    if transacao_in.data is not None:
        transacao.data = transacao_in.data
    if transacao_in.tipo is not None:
        transacao.tipo = transacao_in.tipo

    db.commit()
    db.refresh(transacao)
    return transacao


@router.delete("/{transacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transacao(
    transacao_id: int,
    db: DBSession,
    current_user: CurrentUser,
) -> None:
    transacao = (
        db.query(Transacao)
        .filter(Transacao.id == transacao_id, Transacao.user_id == current_user.id)
        .first()
    )
    if transacao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transação não encontrada para o usuário autenticado.",
        )

    db.delete(transacao)
    db.commit()
    return None
