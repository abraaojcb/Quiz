from models.pergunta_model import QuestionModel
from utils.json_db import read_data, write_data

QUESTION_FILE = 'data/perguntas.json'
QUIZ_FILE = 'data/quizzes.json'

class QuestionController:

    # CREATE
    @staticmethod
    def criar_pergunta(dados):
        quiz_id = dados.get("quiz_id")
        enunciado = dados.get("enunciado")
        tipo = dados.get("tipo")
        dificuldade = dados.get("dificuldade", "easy")

        # validações básicas
        if not quiz_id or not enunciado or not tipo:
            return {"erro": "quiz_id, enunciado e tipo são obrigatórios!"}, 400

        # 🔥 valida se quiz existe (JSON agora)
        quizzes = read_data(QUIZ_FILE)
        quiz = next((q for q in quizzes if q["id"] == quiz_id), None)

        if not quiz:
            return {"erro": "Quiz não encontrado!"}, 404

        # valida tipo
        if tipo not in ["multipla_escolha", "verdadeiro_falso"]:
            return {"erro": "Tipo inválido!"}, 400

        # valida dificuldade
        if dificuldade not in ["easy", "medium", "hard"]:
            return {"erro": "Dificuldade inválida!"}, 400

        perguntas = read_data(QUESTION_FILE)

        nova_pergunta = QuestionModel.criar_molde_pergunta(
            quiz_id,
            enunciado,
            tipo,
            dificuldade
        )

        perguntas.append(nova_pergunta)
        write_data(QUESTION_FILE, perguntas)

        return {
            "mensagem": "Pergunta criada com sucesso!",
            "id": nova_pergunta["id"]
        }, 201

    # READ ALL
    @staticmethod
    def listar_perguntas():
        perguntas = read_data(QUESTION_FILE)
        return perguntas, 200

    # READ ONE
    @staticmethod
    def buscar_pergunta_por_id(id):
        perguntas = read_data(QUESTION_FILE)

        pergunta = next((p for p in perguntas if p["id"] == id), None)

        if not pergunta:
            return {"erro": "Pergunta não encontrada!"}, 404

        return pergunta, 200

    # UPDATE
    @staticmethod
    def atualizar_pergunta(id, dados):
        perguntas = read_data(QUESTION_FILE)

        pergunta = next((p for p in perguntas if p["id"] == id), None)

        if not pergunta:
            return {"erro": "Pergunta não encontrada!"}, 404

        if "enunciado" in dados:
            pergunta["enunciado"] = dados["enunciado"]

        if "tipo" in dados:
            if dados["tipo"] not in ["multipla_escolha", "verdadeiro_falso"]:
                return {"erro": "Tipo inválido!"}, 400
            pergunta["tipo"] = dados["tipo"]

        if "dificuldade" in dados:
            if dados["dificuldade"] not in ["easy", "medium", "hard"]:
                return {"erro": "Dificuldade inválida!"}, 400
            pergunta["dificuldade"] = dados["dificuldade"]

        if "quiz_id" in dados:
            quizzes = read_data(QUIZ_FILE)
            quiz = next((q for q in quizzes if q["id"] == dados["quiz_id"]), None)

            if not quiz:
                return {"erro": "Quiz não encontrado!"}, 404

            pergunta["quiz_id"] = dados["quiz_id"]

        write_data(QUESTION_FILE, perguntas)

        return {"mensagem": "Pergunta atualizada com sucesso!"}, 200

    # DELETE
    @staticmethod
    def deletar_pergunta(id):
        perguntas = read_data(QUESTION_FILE)

        novas_perguntas = [p for p in perguntas if p["id"] != id]

        if len(perguntas) == len(novas_perguntas):
            return {"erro": "Pergunta não encontrada!"}, 404

        write_data(QUESTION_FILE, novas_perguntas)

        return {"mensagem": "Pergunta deletada com sucesso!"}, 200