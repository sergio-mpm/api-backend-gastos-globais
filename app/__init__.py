from flask_jwt_extended import JWTManager
from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate
from .security import bearer_auth

def create_app():
    info = Info(
        title="GastosGlobaisAPI",
        version="1.0.0",
        description="API para controle de despesas globais, permitindo o registro e gerenciamento de despesas globais por usuarios diversos"
    )
    security_schemes = {"bearerAuth": bearer_auth}
    app = OpenAPI(__name__, info=info, doc_prefix="/v1", security_schemes=security_schemes)

    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": "*"}})

    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import usuario, despesa
    