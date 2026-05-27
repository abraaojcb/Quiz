from models.sala_model import SalaModel
from utils.json_db import read_data, write_data

SALA_FILE = 'data/salas.json'
QUIZ_FILE = 'data/quizzes.json'

class SalaController:
    @staticmethod
    def criar_sala(dados, usuario):
        nome = dados.get("nome")
        quiz_id = dados.get("quiz_id")
        
        # Valida se o quiz existe
        quizzes = read_data(QUIZ_FILE)
        if not any(q["id"] == quiz_id for q in quizzes):
            return {"erro": "Quiz não encontrado!"}, 404
            
        salas = read_data(SALA_FILE)
        nova_sala = SalaModel.criar_molde_sala(nome, usuario["user_id"], quiz_id)
        
        salas.append(nova_sala)
        write_data(SALA_FILE, salas)
        
        return {
            "mensagem": "Sala criada!",
            "codigo": nova_sala["codigo"],
            "sala_id": nova_sala["id"]
        }, 201

    @staticmethod
    def listar_salas():
        return read_data(SALA_FILE), 200

    @staticmethod
    def entrar_na_sala(dados, usuario):
        codigo = dados.get("codigo")
        if not codigo:
            return {"erro": "O código da sala é obrigatório!"}, 400
            
        salas = read_data(SALA_FILE)
        # Busca a sala que tenha o código enviado (ex: 59ABS)
        sala = next((s for s in salas if s["codigo"] == codigo.upper()), None)
        
        if not sala:
            return {"erro": "Sala não encontrada!"}, 404
            
        if sala["status"] != "aberta":
            return {"erro": "Esta sala não está mais aceitando jogadores!"}, 400

        # Verifica se o usuário já está na sala para não duplicar
        if usuario["user_id"] not in sala["participantes"]:
            sala["participantes"].append(usuario["user_id"])
            write_data(SALA_FILE, salas)
            
        return {
            "mensagem": f"Você entrou na sala {sala['nome']}!",
            "sala_id": sala["id"]
        }, 200
    
    @staticmethod
    def iniciar_partida(sala_id, usuario):
        salas = read_data(SALA_FILE)
        sala = next((s for s in salas if s["id"] == sala_id), None)

        if not sala:
            return {"erro": "Sala não encontrada!"}, 404
            
        # 🔒 Segurança: Só o dono da sala pode iniciar
        if sala["dono_id"] != usuario["user_id"]:
            return {"erro": "Apenas o dono da sala pode iniciar a partida!"}, 403

        sala["status"] = "jogando"
        write_data(SALA_FILE, salas)

        return {"mensagem": "A partida começou! Boa sorte aos competidores."}, 200
    
    @staticmethod
    def finalizar_sala(sala_id, usuario):
        salas = read_data(SALA_FILE)
        sala = next((s for s in salas if s["id"] == sala_id), None)

        if not sala:
            return {"erro": "Sala não encontrada!"}, 404
            
        # Apenas o dono pode fechar a sala
        if sala["dono_id"] != usuario["user_id"]:
            return {"erro": "Apenas o dono pode finalizar a sala!"}, 403

        sala["status"] = "finalizada"
        write_data(SALA_FILE, salas)

        return {"mensagem": "A sala foi fechada! Confira o ranking final."}, 200