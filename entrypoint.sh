#!/bin/sh

# Aplica migrations antes de iniciar a API
flask db upgrade

# Inicia a aplicação
exec python app.py
