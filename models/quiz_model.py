import datetime
import uuid

class QuizModel:
    @staticmethod
    def criar_molde_quiz(
        titulo,
        descricao,
        tema_id,
        criado_por,
        dificuldade="easy",
        publico=True
    ):
        return {
            "id": str(uuid.uuid4()),
            "titulo": titulo,
            "descricao": descricao,
            "tema_id": tema_id,
            "criado_por": criado_por,
            "dificuldade": dificuldade,
            "publico": publico,
        }