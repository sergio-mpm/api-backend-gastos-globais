from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import DateTime
from ..models.usuario import Usuario
from datetime import datetime

class UsuarioSchema(BaseModel):
    cpf: str
    nome: str
    email: Optional[str] = None
    senha: str
    despesas: Optional[List[dict]] = []

    model_config = {
        "from_attributes": True
    }


class UsuarioBuscaSchema(BaseModel):
    cpf: str = "12345678900"


class UsuarioViewSchema(BaseModel):
    cpf: str
    nome: str
    email: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class ListagemUsuariosSchema(BaseModel):
    usuarios: List[UsuarioViewSchema]


def apresenta_usuario(usuarios: List[Usuario]):
    result = []
    for usuario in usuarios:
        result.append({
            "cpf": usuario.cpf,
            "nome": usuario.nome
        })

    return {"usuarios": result}