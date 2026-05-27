import datetime
import uuid

class AnswerOptionModel:
    @staticmethod
    def criar_molde_alternativa(pergunta_id, texto, correta):
        return {
            "id": str(uuid.uuid4()),
            "pergunta_id": pergunta_id,
            "texto": texto.strip(),
            "correta": correta,
            "data_criacao": datetime.datetime.now().isoformat()
        }