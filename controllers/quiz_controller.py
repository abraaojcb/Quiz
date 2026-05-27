from models.quiz_model import QuizModel
from utils.json_db import read_data, write_data

QUIZ_FILE = 'data/quizzes.json'
TEMA_FILE = 'data/temas.json'

class QuizController:

    # CREATE
    @staticmethod
    def criar_quiz(dados, usuario):
        titulo = dados.get("titulo")
        descricao = dados.get("descricao", "")
        tema_id = dados.get("tema_id")
        dificuldade = dados.get("dificuldade", "easy")
        publico = dados.get("publico", True)

        if not titulo:
            return {"erro": "Título é obrigatório!"}, 400

        if not tema_id:
            return {"erro": "tema_id é obrigatório!"}, 400

        # 🔥 valida se tema existe (agora via JSON)
        temas = read_data(TEMA_FILE)
        tema = next((t for t in temas if t["id"] == tema_id), None)

        if not tema:
            return {"erro": "Tema não encontrado!"}, 404

        if dificuldade not in ["easy", "medium", "hard"]:
            return {"erro": "Dificuldade inválida!"}, 400

        quizzes = read_data(QUIZ_FILE)

        novo_quiz = QuizModel.criar_molde_quiz(
            titulo,
            descricao,
            tema_id,
            usuario["user_id"],
            dificuldade,
            publico
        )

        quizzes.append(novo_quiz)
        write_data(QUIZ_FILE, quizzes)

        return {
            "mensagem": "Quiz criado com sucesso!",
            "id": novo_quiz["id"]
        }, 201

    # GET ALL
    @staticmethod
    def listar_quizzes():
        quizzes = read_data(QUIZ_FILE)
        return quizzes, 200

    # GET BY ID
    @staticmethod
    def buscar_quiz_por_id(id):
        quizzes = read_data(QUIZ_FILE)

        quiz = next((q for q in quizzes if q["id"] == id), None)

        if not quiz:
            return {"erro": "Quiz não encontrado!"}, 404

        return quiz, 200

    # UPDATE
    @staticmethod
    def atualizar_quiz(id, dados):
        quizzes = read_data(QUIZ_FILE)

        quiz = next((q for q in quizzes if q["id"] == id), None)

        if not quiz:
            return {"erro": "Quiz não encontrado!"}, 404

        if "titulo" in dados:
            quiz["titulo"] = dados["titulo"]

        if "descricao" in dados:
            quiz["descricao"] = dados["descricao"]

        if "dificuldade" in dados:
            if dados["dificuldade"] not in ["easy", "medium", "hard"]:
                return {"erro": "Dificuldade inválida!"}, 400
            quiz["dificuldade"] = dados["dificuldade"]

        if "publico" in dados:
            quiz["publico"] = dados["publico"]

        if "tema_id" in dados:
            temas = read_data(TEMA_FILE)
            tema = next((t for t in temas if t["id"] == dados["tema_id"]), None)

            if not tema:
                return {"erro": "Tema não encontrado!"}, 404

            quiz["tema_id"] = dados["tema_id"]

        write_data(QUIZ_FILE, quizzes)

        return {"mensagem": "Quiz atualizado com sucesso!"}, 200

    # DELETE
    @staticmethod
    def deletar_quiz(id):
        quizzes = read_data(QUIZ_FILE)

        novos_quizzes = [q for q in quizzes if q["id"] != id]

        if len(quizzes) == len(novos_quizzes):
            return {"erro": "Quiz não encontrado!"}, 404

        write_data(QUIZ_FILE, novos_quizzes)

        return {"mensagem": "Quiz deletado com sucesso!"}, 200