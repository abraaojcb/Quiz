import datetime
import uuid

class QuestionModel:
    @staticmethod
    def criar_molde_pergunta(quiz_id, enunciado, tipo, dificuldade):
        return {
            "id": str(uuid.uuid4()),
            "quiz_id": quiz_id,
            "enunciado": enunciado.strip(),
            "tipo": tipo,
            "dificuldade": dificuldade,
            "data_criacao": datetime.datetime.now().isoformat()
        }