from pydantic import BaseModel
from typing import Optional, List
from marshmallow import Schema, fields
from datetime import datetime

from ..models.despesa import Despesa

from app.schemas import usuario_schema


class DespesaSchema(BaseModel):
    nome: str = "Cachorro Quente"
    valor: float = "25.99"
    moeda: str = "BRL"
    tipo: str = "Alimentação"
    data_despesa: datetime = datetime.now
    cpf: str = "12345678900"
    comentario: str = "Lanche da tarde"
    
    model_config = {
        "from_attributes": True
    }


class DespesaViewSchema(BaseModel):
    id: int
    nome: str
    valor: float
    moeda: str
    tipo: str
    data_despesa: datetime
    comentario: str | None = None
    responsavel: str | None = None
    cpf: str
    
    model_config = {
        "from_attributes": True
    }


class DespesaTotalSchema(BaseModel):
    total: float


class DespesaBuscaSchema(BaseModel):
    id: int = 1


class ListagemDespesasSchema(BaseModel):
    despesas: List[DespesaViewSchema]


class UsuarioTotalPathSchema(BaseModel):
    cpf: str = "12345678900"


class TipoTotalPathSchema(BaseModel):
    tipo: str = "Alimentação"


class DespesaViewUsuarioTotalSchema(BaseModel):
    nome: str = "João da Silva"
    total: float


class DespesaViewTipoTotalSchema(BaseModel):
    tipo: str
    total: float


class DespesaViewMoedaTotalSchema(BaseModel):
    moeda: str
    total: float


class DespesaDeleteSchema(BaseModel):
    id: int
    message: str


def apresenta_despesas(despesas: List[Despesa]) -> dict:
    return {
        "despesas": [
            {
                "id": d.id,
                "nome": d.nome,
                "valor": d.valor,
                "moeda": d.moeda,
                "tipo": d.tipo,
                "data_despesa": d.data_despesa,
                "comentario": getattr(d, "comentario", None),
                "cpf_responsavel": getattr(d.cpf, "nome", None)
            }
            for d in despesas
        ]
    }

def get_nome_responsavel(self, obj):
    return obj.responsavel.nome


class DespesaUpdateSchema(BaseModel):
    nome: str = "Dogão"
    valor: float = "35.99"
    moeda: str = "BRL"
    tipo: str = "Alimentação"
    data_despesa: datetime = datetime.now
    comentario: str | None = None
    responsavel: str | None = None


def apresenta_despesa(despesa: Despesa) -> dict:
    return {
        "id": despesa.id,
        "nome": despesa.nome,
        "valor": despesa.valor,
        "tipo": despesa.tipo,
        "data_despesa": despesa.data_despesa,
        "comentario": getattr(despesa, "comentario", None),
        "responsavel": getattr(despesa.responsavel, "nome", None)
    }
