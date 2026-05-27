from utils.json_db import read_data

class RankingController:
    @staticmethod
    def obter_ranking_global():
        usuarios = read_data('data/users.json')
        
        # Ordena por XP
        ordenados = sorted(usuarios, key=lambda u: u.get("xp_total", 0), reverse=True)
        
        ranking = []
        for i, u in enumerate(ordenados[:10]):
            ranking.append({
                "posicao": i + 1,
                "nome": u.get("nome"),
                "xp": u.get("xp_total", 0),
                "nivel": u.get("nivel", 1)
            })
        return {"ranking": ranking}, 200

    @staticmethod
    def obter_ranking_por_quiz(quiz_id):
        # Aqui você faria a lógica de filtrar tentativas.json por quiz_id
        # e pegar as maiores pontuações.
        pass
    
    @staticmethod
    def obter_ranking_sala(sala_id):
        from utils.json_db import read_data
        
        salas = read_data('data/salas.json')
        tentativas = read_data('data/tentativas.json')
        usuarios = read_data('data/users.json')

        # 1. Acha a sala
        sala = next((s for s in salas if s["id"] == sala_id), None)
        if not sala:
            return {"erro": "Sala não encontrada!"}, 404

        # 2. Lista para guardar os resultados dos participantes
        resultados = []

        for p_id in sala["participantes"]:
            # Busca a tentativa desse participante para o quiz da sala
            # Pegamos a tentativa mais recente dele (caso ele tenha jogado mais de uma vez)
            tentativa = next((t for t in reversed(tentativas) 
                            if t["usuario_id"] == p_id and t["quiz_id"] == sala["quiz_id"]), None)
            
            # Busca o nome do usuário
            user = next((u for u in usuarios if u["id"] == p_id), None)
            nome = user["nome"] if user else "Desconhecido"
            
            resultados.append({
                "nome": nome,
                "pontuacao": tentativa["pontuacao"] if tentativa else 0
            })

        # 3. Ordena os resultados da sala pela pontuação
        ranking_sala = sorted(resultados, key=lambda x: x["pontuacao"], reverse=True)

        return {
            "sala": sala["nome"],
            "ranking": ranking_sala
        }, 200