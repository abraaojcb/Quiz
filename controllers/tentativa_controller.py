from models.tentativa_model import TentativaModel
from utils.json_db import read_data, write_data
import datetime

TENTATIVA_FILE = 'data/tentativas.json'
QUIZ_FILE = 'data/quizzes.json'
USER_FILE = 'data/users.json'

class TentativaController:
    
    @staticmethod
    def iniciar_tentativa(dados, usuario):
        quiz_id = dados.get("quiz_id")
        
        # Valida se o quiz existe nos arquivos JSON
        quizzes = read_data(QUIZ_FILE)
        quiz = next((q for q in quizzes if q["id"] == quiz_id), None)
        if not quiz:
            return {"erro": "Quiz não encontrado!"}, 404
            
        tentativas = read_data(TENTATIVA_FILE)
        
        # Usa o molde para criar a estrutura
        nova = TentativaModel.criar_molde_tentativa(usuario["user_id"], quiz_id)
        
        tentativas.append(nova)
        write_data(TENTATIVA_FILE, tentativas)
        
        return {
            "mensagem": "Partida iniciada com sucesso!", 
            "id_tentativa": nova["id"]
        }, 201

    @staticmethod
    def listar_minhas_tentativas(usuario):
        tentativas = read_data(TENTATIVA_FILE)
        # Filtra apenas as tentativas do usuário logado
        minhas = [t for t in tentativas if t["usuario_id"] == usuario["user_id"]]
        return minhas, 200

    @staticmethod
    def finalizar_tentativa(id_tentativa, usuario):
        tentativas = read_data(TENTATIVA_FILE)
        
        # Busca a tentativa específica
        tentativa = next((t for t in tentativas if t["id"] == id_tentativa), None)
        
        if not tentativa or tentativa["usuario_id"] != usuario["user_id"]:
            return {"erro": "Tentativa não encontrada!"}, 404
            
        if tentativa.get("status") == "finalizado":
            return {"erro": "Esta partida já foi finalizada!"}, 400

        # Atualiza o status
        tentativa["status"] = "finalizado"
        tentativa["data_fim"] = datetime.datetime.now().isoformat()
        
        # 🔥 ATUALIZAÇÃO DE XP NO JSON DE USUÁRIOS
        usuarios = read_data(USER_FILE)
        for u in usuarios:
            if u["id"] == usuario["user_id"]:
                u["xp_total"] = u.get("xp_total", 0) + tentativa["pontuacao"]
                break
        
        write_data(USER_FILE, usuarios)
        write_data(TENTATIVA_FILE, tentativas)
        
        return {
            "mensagem": "Partida finalizada e XP computado!",
            "pontos_ganhos": tentativa["pontuacao"]
        }, 200