from app.models.despesa import Despesa
from app.models.usuario import Usuario
from app.services.cambio_service import CambioService
from app.extensions import db
from datetime import datetime
from sqlalchemy import func

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

    def listar_despesas_por_usuario(self, cpf: str):
        return Despesa.query.filter(Despesa.cpf==cpf).all()

    def lista_despesa_por_moeda(self, moeda:str):
        return Despesa.query.filter(Despesa.moeda==moeda).all()

    def listar_despesas_por_tipo(self, tipo: str):
        return Despesa.query.filter(Despesa.tipo==tipo).all()
    
    def lista_despesas_por_data(self, data_despesa: datetime):
        return Despesa.query.filter(Despesa.data_despesa==data_despesa).all()
    
    def listar_por_periodo(self, data_inicio: datetime, data_fim: datetime):
        return (Despesa.query.filter(Despesa.data_despesa.between(data_inicio, data_fim)).all())
    
    def excluir_despesa(self, id: int) -> None:
        despesa = Despesa.query.get(id)
        if not despesa:
            raise ValueError("Despesa não encontrada")
        
        db.session.delete(despesa)
        db.session.commit()

    def converte_despesa(self, despesa: Despesa, moeda_destino: str):
        return cambio_service.converter_moeda(despesa.valor, despesa.moeda, moeda_destino)