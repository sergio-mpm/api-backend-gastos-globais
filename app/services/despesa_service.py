from app.models.despesa import Despesa
from app.models.usuario import Usuario
from app.services.cambio_service import CambioService
from app.extensions import db
from datetime import datetime
from sqlalchemy import func
import requests

cambio_service = CambioService()

class DespesaService:
    def criar_despesa(self, data: dict) -> Despesa:
        if data["valor"] <= 0:
            raise ValueError("Valor da despesa inválido. Deve ser maior que zero.")

        usuario = Usuario.query.get(data["cpf"])
        if not usuario:
            raise ValueError("Usuário não encontrado. Não é possível criar despesa para um usuário inexistente.")

        despesa = Despesa(
            nome=data["nome"],
            valor=data["valor"],
            moeda=data["moeda"],
            tipo=data["tipo"],
            comentario=data.get("comentario", ""),
            cpf=data["cpf"],
            data_despesa=data.get("data_despesa", datetime.now())
        )

        db.session.add(despesa)
        db.session.commit()

        return despesa

    def listar_despesas(self):
        return Despesa.query.all()

    def buscar_despesa(self, id: int):
        despesa = Despesa.query.get(id)
        if not despesa:
            raise ValueError("Despesa não encontrada")
        return despesa

    def atualizar_despesa(self, id: int, data: dict):
        despesa = self.buscar_despesa(id)
        for campo in ["nome", "valor", "moeda", "tipo", "comentario", "data_despesa"]:
            if campo in data:
                setattr(despesa, campo, data[campo])
        db.session.commit()
        return despesa

    def listar_despesas_por_usuario(self, cpf: str):
        return Despesa.query.filter(Despesa.cpf == cpf).all()

    def lista_despesa_por_moeda(self, moeda: str):
        return Despesa.query.filter(Despesa.moeda == moeda).all()

    def listar_despesas_por_tipo(self, tipo: str):
        return Despesa.query.filter(Despesa.tipo == tipo).all()

    def lista_despesas_por_data(self, data_despesa: datetime):
        return Despesa.query.filter(Despesa.data_despesa == data_despesa).all()

    def listar_por_periodo(self, data_inicio: datetime, data_fim: datetime):
        return Despesa.query.filter(Despesa.data_despesa.between(data_inicio, data_fim)).all()

    def serializar_nome_responsavel_despesa(self, despesa: Despesa, cpf_responsavel: str):
        usuario = Usuario.query.get(cpf_responsavel)
        return {
            "id": despesa.id,
            "nome": despesa.nome,
            "valor": despesa.valor,
            "moeda": despesa.moeda,
            "tipo": despesa.tipo,
            "data_despesa": despesa.data_despesa,
            "comentario": despesa.comentario,
            "responsavel": usuario.nome if usuario else None,
            "cpf": despesa.cpf,
        }

    def serializar_lista_nome_responsavel_despesa(self, despesas):
        return [
            self.serializar_nome_responsavel_despesa(despesa, despesa.cpf)
            for despesa in despesas
        ]

    def calcula_despesas_totais(self):
        total = db.session.query(func.coalesce(func.sum(Despesa.valor), 0)).scalar() or 0
        return float(total)

    def calcula_despesas_totais_por_usuario(self, cpf: str):
        total = (
            db.session.query(func.coalesce(func.sum(Despesa.valor), 0))
            .filter(Despesa.cpf == cpf)
            .scalar() or 0
        )
        return float(total)

    def calcula_despesas_totais_por_tipo(self, tipo: str):
        total = (
            db.session.query(func.coalesce(func.sum(Despesa.valor), 0))
            .filter(Despesa.tipo == tipo)
            .scalar() or 0
        )
        return float(total)

    def calcula_despesas_totais_por_moeda(self, moeda: str):
        total = (
            db.session.query(func.coalesce(func.sum(Despesa.valor), 0))
            .filter(Despesa.moeda == moeda)
            .scalar() or 0
        )
        return float(total)

    def calcula_totais_por_moeda(self):
        registros = (
            db.session.query(Despesa.moeda, func.coalesce(func.sum(Despesa.valor), 0).label("total"))
            .group_by(Despesa.moeda)
            .all()
        )
        return [
            {"moeda": moeda, "total": float(total)}
            for moeda, total in registros
        ]

    def calcula_totais_convertidos_para_moeda(self, moeda_destino: str = "BRL"):
        totais = self.calcula_totais_por_moeda()
        if not totais:
            return []

        moedas = [item["moeda"] for item in totais]
        symbols = ",".join(moeda.upper() for moeda in moedas if moeda.upper() != moeda_destino.upper())

        if not symbols:
            return [
                {
                    "moeda": item["moeda"],
                    "totalOriginal": round(float(item["total"]), 2),
                    "totalConvertido": round(float(item["total"]), 2)
                }
                for item in totais
            ]

        url = f"https://api.frankfurter.dev/v1/latest?base={moeda_destino.upper()}&symbols={symbols}"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        dados = response.json()
        taxas = dados.get("rates", {})

        resultados = []
        for item in totais:
            moeda = item["moeda"].upper()
            total_original = float(item["total"])
            if moeda == moeda_destino.upper():
                total_convertido = total_original
            else:
                taxa = float(taxas.get(moeda, 0) or 0)
                total_convertido = round(total_original / taxa, 2) if taxa else 0.0

            resultados.append({
                "moeda": item["moeda"],
                "totalOriginal": round(total_original, 2),
                "totalConvertido": round(total_convertido, 2)
            })

        return resultados

    def excluir_despesa(self, id: int) -> None:
        despesa = Despesa.query.get(id)
        if not despesa:
            raise ValueError("Despesa não encontrada")

        db.session.delete(despesa)
        db.session.commit()

    def converte_despesa(self, despesa: Despesa, moeda_destino: str):
        return cambio_service.converter_moeda(despesa.valor, despesa.moeda, moeda_destino)