from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from ..extensions import db
from ..models import base


class Usuario(db.Model):

    __tablename__ = "usuarios"

    cpf = db.Column(db.String(11), primary_key=True, nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    senha = db.Column(db.String(255), nullable=False)
    data_nascimento = db.Column(db.DateTime)

    despesas = db.relationship(
        "Despesa",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )


    def __init__(self, cpf:str, nome:str, email:str, senha:str, data_nascimento:DateTime):
        """
            instancia um usuario no sistema

            Arguments:
                Cpf: cpf da pessoa e identificados unico no sistema
                nome: nome do usuario
                email: email do usuario no sistema
                senha: senha do usuario para autenticacao
                data_nascimento: data de nascimento do usuario para identificar idade
        """
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.senha = senha
        self.data_nascimento = data_nascimento

    def to_dict(self):
        return {
            "cpf": self.cpf,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "data_nascimento": self.data_nascimento,
            "despesas": self.despesas
        }