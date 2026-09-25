from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify
from app.services.despesa_service import DespesaService
from app.services.auth_service import AuthService
from app.services.usuario_service import UsuarioService
from app.schemas.error_schema import ErrorSchema
from app.schemas.despesa_schema import (
    DespesaDeleteSchema,
    DespesaSchema,
    DespesaTotalSchema,
    DespesaUpdateSchema,
    DespesaViewSchema,
    DespesaBuscaSchema,
    DespesaViewTipoTotalSchema,
    DespesaViewMoedaTotalSchema,
    DespesaViewUsuarioTotalSchema,
    ListagemDespesasSchema,
    TipoTotalPathSchema,
    MoedaTotalPathSchema,
    UsuarioTotalPathSchema,
    ListaMoedasSchema,
    ListaTotaisPorMoedaSchema,
    TotalPorMoedaSchema,
    ListaTotaisConvertidosSchema,
    TotalConvertidoSchema
)
import requests


despesa_tag = Tag(
    name="Despesa",
    description="Operações de registros, consultas, atualizações e exclusões de despesas"
)

despesa_bp = APIBlueprint(
    "despesas",
    __name__,
    url_prefix="/despesas",
    abp_tags=[despesa_tag]
)

service_despesa = DespesaService()
service_auth = AuthService()
service_usuario = UsuarioService()



# =========================
# CRIAR DESPESA
# =========================
@despesa_bp.post(
    "/criar",
    responses={200: DespesaViewSchema, 400: ErrorSchema}
)
def criar_despesa(body: DespesaSchema):
    """
    Cria uma nova despesa
    """
    
    try:
        despesa = service_despesa.criar_despesa(body.model_dump())
        resultado = DespesaViewSchema (
            id = despesa.id,
            nome = despesa.nome,
            valor = despesa.valor,
            moeda = despesa.moeda,
            tipo = despesa.tipo,
            data_despesa = despesa.data_despesa,
            comentario = despesa.comentario,
            responsavel = service_usuario.obter_nome_usuario_por_cpf(despesa.cpf),
            cpf = despesa.cpf
        )
        return resultado.model_dump(), 200
    except ValueError as e:
        return {"message": str(e)}, 400


# =========================
# LISTAR TODAS
# =========================
@despesa_bp.get(
    "/getallexpenses",
    responses={200: ListagemDespesasSchema, 400: ErrorSchema}
)
def listar_despesas():
    """
    Lista todas as despesas
    """
    try:
        despesas = service_despesa.listar_despesas()
        listagem_despesas_nome = service_despesa.serializar_lista_nome_responsavel_despesa(despesas)
        listagem_despesas = ListagemDespesasSchema(despesas=listagem_despesas_nome)
        return listagem_despesas.model_dump(), 200
    except ValueError as e:
        return {"message": str(e)}, 400


# =========================
# BUSCAR POR ID
# =========================
@despesa_bp.get(
    "/<int:id>",
    responses={200: DespesaViewSchema, 404: ErrorSchema}
)
def buscar_despesa(path: DespesaBuscaSchema):
    """
    Retorna uma despesa pelo ID
    """
    try:
        despesa = service_despesa.buscar_despesa(path.id)
        resultado = service_despesa.serializar_nome_responsavel_despesa(despesa, despesa.cpf)
        return DespesaViewSchema.model_validate(resultado).model_dump(), 200
    except ValueError as e:
        return {"message": str(e)}, 404


# =========================
# ATUALIZAR DESPESA
# =========================
@despesa_bp.put(
    "/<int:id>",
    responses={200: DespesaViewSchema, 404: ErrorSchema}
)
def atualizar_despesa(path: DespesaBuscaSchema, body: DespesaUpdateSchema):
    """
    Atualiza uma despesa parcialmente
    """
    try:
        despesa = service_despesa.atualizar_despesa(
            path.id,
            body.model_dump(exclude_unset=True)
        )
        resultado = service_despesa.serializar_nome_responsavel_despesa(despesa, despesa.cpf)
        return DespesaViewSchema.model_validate(resultado).model_dump(), 200
    except ValueError as e:
        return {"message": str(e)}, 404


# =========================
# EXCLUIR DESPESA
# =========================
@despesa_bp.delete(
    "/<int:id>",
    responses={200: DespesaDeleteSchema, 404: ErrorSchema}
)
def excluir_despesa(path: DespesaBuscaSchema):
    """
    Exclui uma despesa
    """
    try:
        service_despesa.excluir_despesa(path.id)
        resultado = DespesaDeleteSchema (
            id=path.id,
            message="Despesa excluída com sucesso"
        )
        return resultado.model_dump(), 200
    except ValueError as e:
        return {"message": str(e)}, 404


# =========================
# LISTAR MOEDAS - EXTERNO
# =========================
@despesa_bp.get(
    "/moedas",
    responses={200: ListaMoedasSchema, 404: ErrorSchema}
)
def listar_moedas():
    url = "https://api.frankfurter.dev/v1/currencies"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        currencies = response.json()
        return ListaMoedasSchema(moedas=list(currencies.keys())).model_dump(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# TOTAIS
# =========================
@despesa_bp.get(
    "/total",
    responses={200: DespesaTotalSchema, 404: ErrorSchema}
)
def total_despesas():
    """
    Retorna o valor total das despesas
    """
    try:
        resultado_despesas_total = DespesaTotalSchema (
            total=service_despesa.calcula_despesas_totais()
        )
        return resultado_despesas_total.model_dump(), 200
    except ValueError as e:
        return {"message": str(e)}, 404


@despesa_bp.get(
        "/total/usuario/<string:cpf>",
        responses={200: DespesaViewUsuarioTotalSchema}
)
def total_por_usuario(path: UsuarioTotalPathSchema):
    """
    Total de despesas por usuário
    """
    resultado_usuario_total = DespesaViewUsuarioTotalSchema (
        nome=service_usuario.obter_nome_usuario_por_cpf(path.cpf),
        total=service_despesa.calcula_despesas_totais_por_usuario(path.cpf)
    )
    return resultado_usuario_total.model_dump(), 200


@despesa_bp.get(
        "/total/tipo/<string:tipo>",
        responses={200: DespesaViewTipoTotalSchema}
)
def total_por_tipo(path: TipoTotalPathSchema):
    """
    Total de despesas por tipo
    """
    resultado_tipo_total = DespesaViewTipoTotalSchema (
        tipo = path.tipo,
        total = service_despesa.calcula_despesas_totais_por_tipo(path.tipo)
    )
    return resultado_tipo_total.model_dump(), 200


@despesa_bp.get(
    "/total/moeda/<string:moeda>",
    responses={200: DespesaViewMoedaTotalSchema}
)
def total_por_moeda(path: MoedaTotalPathSchema):
    """
    Total de despesas por moeda
    """
    resultado_moeda_total = DespesaViewMoedaTotalSchema (
        moeda = path.moeda,
        total = service_despesa.calcula_despesas_totais_por_moeda(path.moeda)
    )
    return resultado_moeda_total.model_dump(), 200


@despesa_bp.get(
    "/total/moedas",
    responses={200: ListaTotaisPorMoedaSchema, 404: ErrorSchema}
)
def total_por_todas_moedas():
    """
    Retorna o total de despesas agrupado por moeda
    """
    try:
        totais = service_despesa.calcula_totais_por_moeda()
        resultado = ListaTotaisPorMoedaSchema(
            totais=[TotalPorMoedaSchema(**item) for item in totais]
        )
        return resultado.model_dump(), 200
    except ValueError as e:
        return {"message": str(e)}, 404


@despesa_bp.get(
    "/total/conversao",
    responses={200: ListaTotaisConvertidosSchema, 404: ErrorSchema}
)
def total_convertido_para_brl():
    """
    Retorna os totais agrupados por moeda convertidos para BRL
    """
    try:
        totais = service_despesa.calcula_totais_convertidos_para_moeda("BRL")
        resultado = ListaTotaisConvertidosSchema(
            totais=[TotalConvertidoSchema(**item) for item in totais]
        )
        return resultado.model_dump(), 200
    except ValueError as e:
        return {"message": str(e)}, 404


@despesa_bp.get(
    "/total/conversao/<string:moeda>",
    responses={200: ListaTotaisConvertidosSchema, 404: ErrorSchema}
)
def total_convertido_para_moeda(path: MoedaTotalPathSchema):
    """
    Retorna os totais agrupados por moeda convertidos para a moeda especificada
    """
    try:
        totais = service_despesa.calcula_totais_convertidos_para_moeda(path.moeda)
        resultado = ListaTotaisConvertidosSchema(
            totais=[TotalConvertidoSchema(**item) for item in totais]
        )
        return resultado.model_dump(), 200
    except ValueError as e:
        return {"message": str(e)}, 404