import datetime
import uuid

from utils.json_db import read_data, write_data

FILE_PATH = "data/users.json"

class UserModel:

    @staticmethod
    def criar_molde_usuario(nome, email, senha_criptografada, codigo_otp, avatar_url=""):
        return {
            "id": str(uuid.uuid4()),
            "nome": nome.strip(),
            "email": email.strip().lower(),
            "senha": senha_criptografada,
            "data_criacao": datetime.datetime.now().isoformat(),
            "avatar_url": avatar_url,
            "nivel": 1,
            "xp_total": 0,
            "is_verified": False,
            "otp_code": codigo_otp
        }

    @staticmethod
    def buscar_por_email(email):
        usuarios = read_data(FILE_PATH)

        return next(
            (u for u in usuarios if u["email"] == email.strip().lower()),
            None
        )

    @staticmethod
    def salvar_usuario(usuario):
        usuarios = read_data(FILE_PATH)

        usuarios.append(usuario)

        write_data(FILE_PATH, usuarios)

    @staticmethod
    def atualizar_usuario(user_id, novos_dados):
        usuarios = read_data(FILE_PATH)

        for usuario in usuarios:
            if usuario["id"] == user_id:
                usuario.update(novos_dados)
                break

        write_data(FILE_PATH, usuarios)