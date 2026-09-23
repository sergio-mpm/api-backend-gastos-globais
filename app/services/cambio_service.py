from app.models.despesa import Despesa
from app.extensions import db
import requests


BASE_URL = "https://api.frankfurter.dev/v1"


class CambioService:
    @staticmethod
    def converter_moeda(valor: float, moeda_origem: str, moeda_destino: str) -> dict:
        """
        Converte um valor de uma moeda para outra usando a Frankfurter API.

        Args:
            valor (float): Quantia a ser convertida.
            moeda_origem (str): Código da moeda de origem (ex: 'EUR', 'USD', 'BRL').
            moeda_destino (str): Código da moeda de destino (ex: 'BRL', 'USD', 'EUR').

        Returns:
            dict: Dicionário com informações da conversão.
        """
        url = f"{BASE_URL}/latest"
        params = {
            "amount": valor,
            "from": moeda_origem.upper(),
            "to": moeda_destino.upper()
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Erro ao consultar API de câmbio: {e}")

        dados = response.json()

        return {
            "valor_original": valor,
            "moeda_origem": moeda_origem.upper(),
            "moeda_destino": moeda_destino.upper(),
            "valor_convertido": dados["rates"][moeda_destino.upper()],
            "data": dados["date"]
        }