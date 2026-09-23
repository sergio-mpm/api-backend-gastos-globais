from flask_jwt_extended import jwt_required
from flask_openapi3 import APIBlueprint, Tag
from app.services.usuario_service import UsuarioService
from app.schemas.error_schema import ErrorSchema
from app.schemas.usuario_schema import (
    ListagemUsuariosSchema,
    UsuarioSchema,
    UsuarioViewSchema,
    UsuarioBuscaSchema
)


usuario_tag = Tag(
    name="Usuario",
    description="Operações de registros, consultas, atualizações e exclusões de usuários"
)

usuario_bp = APIBlueprint(
    "usuarios",
    __name__,
    url_prefix="/usuarios",
    abp_tags=[usuario_tag]
)

service_usuario = UsuarioService()


@usuario_bp.post(
    "/cadastrar",
    responses={200: UsuarioViewSchema, 400: ErrorSchema}
)
def cadastrar_usuario(body: UsuarioSchema):
    try:
        usuario = service_usuario.criar_usuario(body.model_dump())
        return UsuarioViewSchema.model_validate(usuario).model_dump(), 200
    except ValueError as e:
        return {"message": str(e)}, 400
    

@usuario_bp.get(
    "/<string:cpf>",
    security=[{"bearerAuth": []}],
    responses={200: UsuarioViewSchema, 404: ErrorSchema}
)
@jwt_required()
def consultar_usuario(path: UsuarioBuscaSchema):
    try:
        usuario = service_usuario.obter_usuario(path.cpf)
        return UsuarioViewSchema.model_validate(usuario).model_dump(), 200
    except ValueError as e:
        return {"message": str(e)}, 404
    

@usuario_bp.put(
    "/<string:cpf>",
    responses={200: UsuarioViewSchema, 404: ErrorSchema}
)
@jwt_required()
def atualizar_usuario(path: UsuarioBuscaSchema, body: UsuarioSchema):
    try:
        usuario = service_usuario.atualiza_cadastro_usuario(
            path.cpf,
            body.model_dump(exclude_unset=True)
        )
        return UsuarioViewSchema.model_validate(usuario).model_dump(), 200
    except ValueError as e:
        return {"message": str(e)}, 404
    

@usuario_bp.delete(
    "/<string:cpf>",
    responses={204: None, 404: ErrorSchema}
)
@jwt_required()
def excluir_usuario(path: UsuarioBuscaSchema):
    try:
        service_usuario.excluir_usuario(path.cpf)
        return {"message": "Usuario Excluído com sucesso" }, 204
    except ValueError as e:
        return {"message": str(e)}, 404