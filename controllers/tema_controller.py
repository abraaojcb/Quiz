from models.tema_model import TemaModel
from utils.json_db import read_data, write_data

FILE_PATH = 'data/temas.json'

class TemaController:

    @staticmethod
    def criar_tema(dados):
        nome = dados.get("nome")
        descricao = dados.get("descricao", "")

        if not nome:
            return {"erro": "Nome do tema é obrigatório!"}, 400

        nome_formatado = nome.strip().lower()

        temas = read_data(FILE_PATH)

        # 🔍 verifica se já existe
        tema_existente = next((t for t in temas if t["nome"] == nome_formatado), None)
        if tema_existente:
            return {"erro": "Este tema já existe!"}, 409

        novo_tema = TemaModel.criar_molde_tema(nome_formatado, descricao)

        temas.append(novo_tema)
        write_data(FILE_PATH, temas)

        return {
            "mensagem": "Tema criado com sucesso!",
            "id": novo_tema["id"]
        }, 201

    @staticmethod
    def listar_temas():
        temas = read_data(FILE_PATH)

        return temas, 200

    @staticmethod
    def buscar_tema_por_id(id):
        temas = read_data(FILE_PATH)

        tema = next((t for t in temas if t["id"] == id), None)

        if not tema:
            return {"erro": "Tema não encontrado!"}, 404

        return tema, 200

    @staticmethod
    def atualizar_tema(id, dados):
        temas = read_data(FILE_PATH)

        tema = next((t for t in temas if t["id"] == id), None)

        if not tema:
            return {"erro": "Tema não encontrado!"}, 404

        # 🔄 valida nome duplicado
        if "nome" in dados:
            nome_formatado = dados["nome"].strip().lower()

            existente = next(
                (t for t in temas if t["nome"] == nome_formatado and t["id"] != id),
                None
            )

            if existente:
                return {"erro": "Já existe outro tema com esse nome!"}, 409

            tema["nome"] = nome_formatado

        if "descricao" in dados:
            tema["descricao"] = dados["descricao"]

        write_data(FILE_PATH, temas)

        return {"mensagem": "Tema atualizado com sucesso!"}, 200

    @staticmethod
    def deletar_tema(id):
        temas = read_data(FILE_PATH)

        novos_temas = [t for t in temas if t["id"] != id]

        if len(temas) == len(novos_temas):
            return {"erro": "Tema não encontrado!"}, 404

        write_data(FILE_PATH, novos_temas)

        return {"mensagem": "Tema deletado com sucesso!"}, 200