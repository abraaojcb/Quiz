import jwt
import datetime

SECRET_KEY = "sua_chave_secreta"

def gerar_token(usuario):
    payload = {
        "user_id": usuario["id"],  # 🔥 corrigido aqui
        "email": usuario["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token