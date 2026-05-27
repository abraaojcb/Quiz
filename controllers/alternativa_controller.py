from models.alternativa_model import AnswerOptionModel
from utils.json_db import read_data, write_data

ANSWER_FILE = 'data/alternativas.json'
QUESTION_FILE = 'data/perguntas.json'

class AnswerOptionController:

    # CREATE
    @staticmethod
    def criar_alternativa(dados):
        pergunta_id = dados.get("pergunta_id")
        texto = dados.get("texto")
        correta = dados.get("correta", False)

        if not pergunta_id or not texto:
            return {"erro": "pergunta_id e texto são obrigatórios!"}, 400

        texto = texto.strip()

        # 🔥 valida se pergunta existe (JSON)
        perguntas = read_data(QUESTION_FILE)
        pergunta = next((p for p in perguntas if p["id"] == pergunta_id), None)

        if not pergunta:
            return {"erro": "Pergunta não encontrada!"}, 404

        alternativas = read_data(ANSWER_FILE)

        # 🔒 evita duplicata
        existente = next(
            (a for a in alternativas if a["pergunta_id"] == pergunta_id and a["texto"] == texto),
            None
        )
        if existente:
            return {"erro": "Essa alternativa já existe!"}, 409

        # 🚨 regra: só 1 correta
        if correta:
            ja_existe_correta = next(
                (a for a in alternativas if a["pergunta_id"] == pergunta_id and a["correta"] is True),
                None
            )
            if ja_existe_correta:
                return {
                    "erro": "Já existe uma alternativa correta para essa pergunta!"
                }, 409

        nova = AnswerOptionModel.criar_molde_alternativa(
            pergunta_id,
            texto,
            correta
        )

        alternativas.append(nova)
        write_data(ANSWER_FILE, alternativas)

        return {
            "mensagem": "Alternativa criada com sucesso!",
            "id": nova["id"]
        }, 201

    # READ ALL
    @staticmethod
    def listar_alternativas():
        alternativas = read_data(ANSWER_FILE)
        return alternativas, 200

    # READ ONE
    @staticmethod
    def buscar_alternativa_por_id(id):
        alternativas = read_data(ANSWER_FILE)

        alt = next((a for a in alternativas if a["id"] == id), None)

        if not alt:
            return {"erro": "Alternativa não encontrada!"}, 404

        return alt, 200

    # UPDATE
    @staticmethod
    def atualizar_alternativa(id, dados):
        alternativas = read_data(ANSWER_FILE)

        alt = next((a for a in alternativas if a["id"] == id), None)
        if not alt:
            return {"erro": "Alternativa não encontrada!"}, 404

        if "texto" in dados:
            alt["texto"] = dados["texto"].strip()

        if "correta" in dados:
            if dados["correta"] is True:
                ja_existe = next(
                    (a for a in alternativas 
                     if a["pergunta_id"] == alt["pergunta_id"] 
                     and a["correta"] is True 
                     and a["id"] != id),
                    None
                )
                if ja_existe:
                    return {"erro": "Já existe outra alternativa correta!"}, 409

            alt["correta"] = dados["correta"]

        if "pergunta_id" in dados:
            perguntas = read_data(QUESTION_FILE)
            pergunta = next((p for p in perguntas if p["id"] == dados["pergunta_id"]), None)

            if not pergunta:
                return {"erro": "Pergunta não encontrada!"}, 404

            alt["pergunta_id"] = dados["pergunta_id"]

        write_data(ANSWER_FILE, alternativas)

        return {"mensagem": "Alternativa atualizada com sucesso!"}, 200

    # DELETE
    @staticmethod
    def deletar_alternativa(id):
        alternativas = read_data(ANSWER_FILE)

        novas = [a for a in alternativas if a["id"] != id]

        if len(alternativas) == len(novas):
            return {"erro": "Alternativa não encontrada!"}, 404

        write_data(ANSWER_FILE, novas)

        return {"mensagem": "Alternativa deletada com sucesso!"}, 200