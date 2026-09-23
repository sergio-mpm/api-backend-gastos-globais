from flask_openapi3 import APIBlueprint, Tag
from app.schemas.error_schema import ErrorSchema
from app.services.auth_service import AuthService
from app.schemas.auth_schema import AuthSchema, TokenResponseSchema


auth_tag = Tag(
    name="Autenticação",
    description="Operações de autenticação via JWT"
)

auth_bp = APIBlueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    abp_tags=[auth_tag]
)

auth_service = AuthService()


@auth_bp.post(
    "/login",
    summary="Login de usuário",
    responses={200: TokenResponseSchema, 401: ErrorSchema}
)
def login(body: AuthSchema):
    """
    Realiza login e retorna token JWT
    """
    try:
        token = auth_service.authenticate(
            body.cpf,
            body.senha
        )

        return {
            "access_token": token,
            "token_type": "Bearer"
        }

    except ValueError as e:
        return {"message": str(e)}, 401