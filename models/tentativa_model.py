import datetime
import uuid

class TentativaModel:
    @staticmethod
    def criar_molde_tentativa(usuario_id, quiz_id):
        return {
            "id": str(uuid.uuid4()),
            "usuario_id": usuario_id,
            "quiz_id": quiz_id,
            "pontuacao": 0,
            "status": "em_andamento",
            "data_inicio": datetime.datetime.now().isoformat()
        }