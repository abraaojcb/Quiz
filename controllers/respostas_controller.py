# controllers/respostas_controller.py
from utils.json_db import read_data, write_data
from models.resposta_model import RespostaModel
from utils.observer import motor_de_notificacoes

RESPOSTA_FILE = 'data/respostas.json'
ANSWER_FILE = 'data/alternativas.json'
TENTATIVA_FILE = 'data/tentativas.json'

# Helper: Função isolada apenas para achar a sala (Deixa o código organizado!)
def _encontrar_sala_ativa(quiz_id):
    salas = read_data('data/salas.json')
    sala = next((s for s in salas if s["quiz_id"] == quiz_id and s["status"] == "jogando"), None)
    return sala["id"] if sala else None


class RespostasController:
    @staticmethod
    def salvar_resposta(dados):
        tentativa_id = dados.get("tentativa_id")
        pergunta_id = dados.get("pergunta_id")
        alternativa_id = dados.get("alternativa_id")

        # 1. Carrega as alternativas para conferir a correta
        alternativas = read_data(ANSWER_FILE)
        alternativa = next((a for a in alternativas if a["id"] == alternativa_id), None)
        
        if not alternativa:
            return {"erro": "Alternativa não encontrada no sistema!"}, 404

        e_correta = alternativa.get("correta", False)

        # 2. Registra a resposta no arquivo JSON
        respostas = read_data(RESPOSTA_FILE)
        nova_resposta = RespostaModel.criar_molde_resposta(
            tentativa_id, pergunta_id, alternativa_id, e_correta
        )
        respostas.append(nova_resposta)
        write_data(RESPOSTA_FILE, respostas)

        # 3. Se estiver correta, soma 10 pontos na TENTATIVA
        if e_correta:
            tentativas = read_data(TENTATIVA_FILE)
            sala_id_alvo = None
            
            for t in tentativas:
                if t["id"] == tentativa_id:
                    t["pontuacao"] = t.get("pontuacao", 0) + 10
                    
                    # Usa a função organizadora que criamos lá em cima!
                    sala_id_alvo = _encontrar_sala_ativa(t["quiz_id"])
                    break
            
            # Salva o arquivo com o nome correto (Mapeado no Item 1)
            write_data(TENTATIVA_FILE, tentativas)

            # 🚨 Se estiver jogando em uma sala multiplayer, o MOTOR chama o Observer
            if sala_id_alvo:
                motor_de_notificacoes.notify(
                    sala_id=sala_id_alvo,
                    dados_atualizacao={
                        "mensagem": "Um jogador acertou uma questão e o placar mudou!",
                        "tentativa_id": tentativa_id
                    }
                )

        return {
            "correta": e_correta,
            "mensagem": "Resposta registrada!",
            "pontos_ganhos": 10 if e_correta else 0
        }, 201