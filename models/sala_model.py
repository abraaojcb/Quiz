import uuid
import random
import string

class SalaModel:
    @staticmethod
    def gerar_codigo():
        # Gera um código de 5 letras/números (ex: AB123)
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    @staticmethod
    def criar_molde_sala(nome, dono_id, quiz_id):
        return {
            "id": str(uuid.uuid4()),
            "nome": nome,
            "codigo": SalaModel.gerar_codigo(),
            "dono_id": dono_id,
            "quiz_id": quiz_id,
            "status": "aberta", # aberta, jogando, finalizada
            "participantes": [dono_id] # O dono já começa na sala
        }