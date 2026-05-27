from functools import wraps
from flask import request, jsonify
import jwt

SECRET_KEY = "sua_chave_secreta"

def token_obrigatorio(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        print("🔥 Middleware executando")  # DEBUG

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"erro": "Token não fornecido!"}), 401

        partes = auth_header.split(" ")

        if len(partes) != 2 or partes[0] != "Bearer":
            return jsonify({"erro": "Formato do token inválido!"}), 401

        token = partes[1]

        try:
            dados = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            print("ERRO TOKEN:", e)  # DEBUG
            return jsonify({"erro": "Token inválido ou expirado!"}), 401

        return f(dados, *args, **kwargs)

    return decorator