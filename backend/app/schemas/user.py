from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    senha: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
