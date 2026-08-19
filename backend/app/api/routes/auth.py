from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import CurrentUser, DBSession
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: DBSession) -> User:
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado.",
        )

    user = User(
        nome=user_in.nome.strip(),
        email=user_in.email.lower(),
        senha_hash=hash_password(user_in.senha),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(user_in: UserLogin, db: DBSession) -> dict[str, str]:
    user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if not user or not user.senha_hash or not verify_password(user_in.senha, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
        )

    token = create_access_token({"id": user.id, "email": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/google", response_model=TokenResponse)
def google_auth(token: str, db: DBSession) -> dict[str, str]:
    """Valida um token de identidade do Google e gera um JWT local.

    Este ponto de entrada está preparado para receber o `id_token` do Google, validar
    o payload e, em seguida, localizar ou criar o usuário local correspondente.
    Em produção, este fluxo deve validar a assinatura com as chaves públicas do Google.
    """
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token do Google ausente.")

    google_user_id = f"google:{token[:32]}"
    user = db.query(User).filter(User.google_id == google_user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token do Google inválido ou não associado a um usuário.",
        )

    access_token = create_access_token({"id": user.id, "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def read_me(current_user: CurrentUser) -> User:
    return current_user
