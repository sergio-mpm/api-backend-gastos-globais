from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from app.schemas import *
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)