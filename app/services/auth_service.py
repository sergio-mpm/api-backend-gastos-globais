from app.services.usuario_service import UsuarioService
from flask_jwt_extended import create_access_token
from datetime import timedelta
from werkzeug.security import check_password_hash

service_usuario = UsuarioService()


class AuthService:
    def authenticate(self, cpf: str, senha: str) -> str:
        """
        Autentica o usuário e retorna um JWT
        """
        try:
            usuario = service_usuario.obter_usuario(cpf)
        except ValueError:
            raise ValueError("CPF e/ou senha inválidos")

        # Verificação segura:
        if not usuario or not check_password_hash(usuario.senha, senha):
            raise ValueError("CPF e/ou senha inválidos")

        # Geração do Token
        access_token = create_access_token(
            identity=cpf,
            expires_delta=timedelta(hours=2)
        )

        return access_token