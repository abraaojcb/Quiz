import datetime
import uuid

class RespostaModel:
    @staticmethod
    def criar_molde_resposta(tentativa_id, pergunta_id, alternativa_id, correta):
        return {
            "id": str(uuid.uuid4()),
            "tentativa_id": tentativa_id,
            "pergunta_id": pergunta_id,
            "alternativa_id": alternativa_id,
            "correta": correta,
            "data_resposta": datetime.datetime.now().isoformat()
        }