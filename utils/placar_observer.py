# utils/placar_observer.py
from utils.observer import SalaObserver
from controllers.ranking_controller import RankingController

class PlacarSalaObserver(SalaObserver):
    def update(self, sala_id: str, dados_atualizacao: dict) -> None:
        # Executado automaticamente pelo Subject!
        print(f"\n📢 [DESIGN PATTERN - OBSERVER]: Atividade detectada na Sala {sala_id}!")
        print(f"🔹 Detalhe: {dados_atualizacao['mensagem']}")
        
        # Recalcula o ranking da sala imediatamente usando a lógica existente
        ranking_atualizado, _ = RankingController.obter_ranking_sala(sala_id)
        
        # Cospe o placar atualizado no terminal na hora
        print(f"📊 [RANKING DA SALA ATUALIZADO AO VIVO]:")
        for jogador in ranking_atualizado.get("ranking", []):
            print(f"   👤 {jogador['nome']} -> {jogador['pontuacao']} pontos")
        print("-" * 50 + "\n")

# Deixa a instância pronta para uso do app.py
placar_sala_observer = PlacarSalaObserver()