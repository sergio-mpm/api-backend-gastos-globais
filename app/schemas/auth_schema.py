from pydantic import BaseModel
from typing import Optional, List


class AuthSchema(BaseModel):
    cpf: str = "12345678900"
    senha: str = "senha123"


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"
