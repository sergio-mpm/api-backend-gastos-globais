from flask import Flask, jsonify, request, redirect, send_from_directory
from flask_cors import CORS
import os
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from app.schemas import *
from app import create_app

app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/ping")
def index():
    return jsonify({"message": "Bem-vindo à API de Gastos Globais!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)