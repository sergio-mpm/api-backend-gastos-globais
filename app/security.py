from flask_openapi3.models import SecurityScheme

bearer_auth = {
    "bearerAuth": SecurityScheme(
        type="http",
        scheme="bearer",
        bearerFormat="JWT"
    )
}