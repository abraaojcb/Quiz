# client_qt.py
import sys
import requests
import json
import os
import uuid
import random
import string
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QHBoxLayout, 
                             QMessageBox, QStackedWidget, QListWidget,
                             QComboBox, QFrame, QTabWidget, QTextEdit)
from PyQt6.QtCore import Qt

BASE_URL = "http://127.0.0.1:5000"
TOKEN_USUARIO = None
ID_USUARIO_LOGADO = None

QUIZIFY_STYLE = """
QWidget {
    background-color: #0b0a12;
    color: #e2e1e9;
    font-family: "Segoe UI", system-ui, sans-serif;
    font-size: 13px;
}

QMainWindow, QDialog, QMessageBox {
    background-color: #0b0a12;
}

QLabel#lblMainHeader {
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
}

QLineEdit, QComboBox {
    background-color: #11101f;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 11px 15px;
    color: #ffffff;
}

QLineEdit:focus, QComboBox:focus {
    border-color: #6366f1;
}

QListWidget {
    background-color: #11101f;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 6px;
}

QListWidget::item {
    background-color: #151426;
    border-radius: 6px;
    padding: 12px;
    margin-bottom: 4px;
    color: #e2e1e9;
}

QListWidget::item:selected {
    background-color: #1b1938;
    color: #818cf8;
    border-left: 3px solid #6366f1;
}

QFrame#sidebarArea {
    background-color: #07060c;
    border-right: 1px solid rgba(255, 255, 255, 0.02);
}

QPushButton#btnMenu {
    background-color: transparent;
    border: none;
    border-radius: 6px;
    padding: 11px 16px;
    color: #716e87;
    font-weight: 600;
    text-align: left;
}

QPushButton#btnMenu:hover {
    color: #e2e1e9;
    background-color: rgba(255, 255, 255, 0.01);
}

QPushButton#btnMenu:checked {
    background-color: rgba(99, 102, 241, 0.08);
    color: #818cf8;
}

QPushButton#btnPrimary {
    background-color: #6366f1;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
}

QPushButton#btnPrimary:hover {
    background-color: #4f46e5;
}

QPushButton#btnSecondary {
    background-color: #151426;
    color: #a78bfa;
    border: 1px solid rgba(124, 58, 237, 0.3);
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
}

QPushButton#btnSecondary:hover {
    background-color: #1b1938;
    border-color: #6366f1;
}

QPushButton#btnDanger {
    background-color: transparent;
    border: 1px solid rgba(239, 68, 68, 0.2);
    color: #f87171;
    border-radius: 8px;
    padding: 10px 16px;
}

QTabWidget::pane {
    border: none;
    background-color: #11101f;
}

QTabBar::tab {
    background-color: #07060c;
    color: #716e87;
    padding: 10px 20px;
    border-radius: 6px;
    margin-right: 4px;
    font-weight: bold;
}

QTabBar::tab:selected {
    background-color: #6366f1;
    color: white;
}

QFrame#cardPergunta {
    background-color: #11101f;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 35px;
}

QPushButton#btnAnswer {
    background-color: #151426;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 15px;
    color: #e2e1e9;
    text-align: center;
}

QPushButton#btnAnswer:hover {
    border-color: #6366f1;
    background-color: #1b1938;
}

QFrame#hudGameBar {
    background-color: #151426;
    border-radius: 12px;
    padding: 12px 20px;
}
"""

def carregar_json_local(caminho):
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except: return []
    return []

def salvar_json_local(caminho, dados):
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def gerar_codigo_sala():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def garantir_arquivo(caminho, padrao):
    pasta = os.path.dirname(caminho)
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta)
    if not os.path.exists(caminho):
        salvar_json_local(caminho, padrao)

# Inicializadores Automáticos dos JSONs locais
garantir_arquivo("data/quizzes.json", [])
garantir_arquivo("data/perguntas.json", [])
garantir_arquivo("data/alternativas.json", [])
garantir_arquivo("data/tentativas.json", [])
garantir_arquivo("data/users.json", [])
garantir_arquivo("data/salas.json", [])


class TelaAutenticacao(QWidget):
    def __init__(self, callback_sucesso):
        super().__init__()
        self.callback_sucesso = callback_sucesso
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 60, 50, 60)

        card_auth = QFrame()
        card_auth.setStyleSheet("background-color: #11101f; border-radius: 12px;")
        layout_card = QVBoxLayout(card_auth)
        layout_card.setContentsMargins(30, 30, 30, 30)

        lbl_logo = QLabel("QuizArena")
        lbl_logo.setStyleSheet("font-size: 32px; font-weight: bold; color: white; margin-bottom: 5px;")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_card.addWidget(lbl_logo)

        lbl_sub = QLabel("// plataforma de quizzes interativos")
        lbl_sub.setStyleSheet("color: #6366f1; font-family: monospace; margin-bottom: 20px;")
        lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_card.addWidget(lbl_sub)

        self.abas_auth = QTabWidget()
        self.aba_login = QWidget()
        self.aba_cadastro = QWidget()

        self.abas_auth.addTab(self.aba_login, "Entrar")
        self.abas_auth.addTab(self.aba_cadastro, "Cadastrar")

        self.configurar_sub_aba_login()
        self.configurar_sub_aba_cadastro()

        layout_card.addWidget(self.abas_auth)
        layout.addWidget(card_auth)
        self.setLayout(layout)

    def configurar_sub_aba_login(self):
        layout = QVBoxLayout(self.aba_login)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 15, 0, 0)
        
        self.txt_login_email = QLineEdit()
        self.txt_login_email.setPlaceholderText("E-mail")
        self.txt_login_senha = QLineEdit()
        self.txt_login_senha.setPlaceholderText("Senha")
        self.txt_login_senha.setEchoMode(QLineEdit.EchoMode.Password)
        
        btn = QPushButton("Entrar na conta →")
        btn.setObjectName("btnPrimary")
        btn.clicked.connect(self.executar_login)
        
        layout.addWidget(self.txt_login_email)
        layout.addWidget(self.txt_login_senha)
        layout.addWidget(btn)

    def configurar_sub_aba_cadastro(self):
        layout = QVBoxLayout(self.aba_cadastro)
        layout.setContentsMargins(0, 15, 0, 0)

        self.stack_cadastro = QStackedWidget()
        layout.addWidget(self.stack_cadastro)

        self.widget_etapa_dados = QWidget()
        layout_dados = QVBoxLayout(self.widget_etapa_dados)
        layout_dados.setSpacing(12)
        layout_dados.setContentsMargins(0, 0, 0, 0)

        self.txt_cad_nome = QLineEdit()
        self.txt_cad_nome.setPlaceholderText("Nome de usuário")
        self.txt_cad_email = QLineEdit()
        self.txt_cad_email.setPlaceholderText("E-mail")
        self.txt_cad_senha = QLineEdit()
        self.txt_cad_senha.setPlaceholderText("Senha")
        self.txt_cad_senha.setEchoMode(QLineEdit.EchoMode.Password)

        self.txt_cad_token = QLineEdit()
        self.txt_cad_token.setPlaceholderText("Token de Autenticação API (Opcional)")
        
        btn_cad = QPushButton("Criar conta →")
        btn_cad.setObjectName("btnPrimary")
        btn_cad.clicked.connect(self.executar_cadastro)

        layout_dados.addWidget(self.txt_cad_nome)
        layout_dados.addWidget(self.txt_cad_email)
        layout_dados.addWidget(self.txt_cad_senha)
        layout_dados.addWidget(self.txt_cad_token)
        layout_dados.addWidget(btn_cad)

        self.widget_etapa_otp = QWidget()
        layout_otp = QVBoxLayout(self.widget_etapa_otp)
        layout_otp.setSpacing(12)
        layout_otp.setContentsMargins(0, 0, 0, 0)

        lbl_aviso_otp = QLabel("<b>Quase lá! Insira o código enviado ao e-mail:</b>")
        lbl_aviso_otp.setStyleSheet("color: #a78bfa;")
        self.txt_ver_codigo = QLineEdit()
        self.txt_ver_codigo.setPlaceholderText("Código de Ativação (OTP)")

        btn_confirmar_otp = QPushButton("Confirmar Código de Ativação →")
        btn_confirmar_otp.setObjectName("btnPrimary")
        btn_confirmar_otp.clicked.connect(self.executar_verificacao)

        layout_otp.addWidget(lbl_aviso_otp)
        layout_otp.addWidget(self.txt_ver_codigo)
        layout_otp.addWidget(btn_confirmar_otp)

        self.stack_cadastro.addWidget(self.widget_etapa_dados)
        self.stack_cadastro.addWidget(self.widget_etapa_otp)
        self.stack_cadastro.setCurrentWidget(self.widget_etapa_dados)

    def executar_login(self):
        global TOKEN_USUARIO, ID_USUARIO_LOGADO
        email = self.txt_login_email.text().strip()
        senha = self.txt_login_senha.text().strip()
        try:
            res = requests.post(f"{BASE_URL}/login", json={"email": email, "senha": senha})
            if res.status_code == 200:
                TOKEN_USUARIO = res.json().get("token")
                ID_USUARIO_LOGADO = res.json().get("usuario", {}).get("id")
                self.callback_sucesso()
            else:
                QMessageBox.critical(self, "Erro", res.json().get("erro", "Falha de Login."))
        except:
            user = next((u for u in carregar_json_local("data/users.json") if u["email"] == email), None)
            if user:
                TOKEN_USUARIO = "mock-token-front-active"
                ID_USUARIO_LOGADO = user["id"]
                self.callback_sucesso()

    def executar_cadastro(self):
        global TOKEN_USUARIO
        nome = self.txt_cad_nome.text().strip()
        self.email_temporario_cadastro = self.txt_cad_email.text().strip()
        senha = self.txt_cad_senha.text().strip()
        token_digitado = self.txt_cad_token.text().strip()
        
        if not nome or not self.email_temporario_cadastro or not senha:
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos para cadastrar!")
            return

        if token_digitado:
            TOKEN_USUARIO = token_digitado

        try:
            headers = {"Authorization": f"Bearer {TOKEN_USUARIO}"} if TOKEN_USUARIO else {}
            res = requests.post(f"{BASE_URL}/cadastro", json={"nome": nome, "email": self.email_temporario_cadastro, "senha": senha}, headers=headers)
            QMessageBox.information(self, "Cadastro", res.json().get("mensagem", "Processado! Verifique seu e-mail."))
            self.stack_cadastro.setCurrentWidget(self.widget_etapa_otp)
        except:
            usuarios = carregar_json_local("data/users.json")
            usuarios.append({"id": str(uuid.uuid4()), "nome": nome, "email": self.email_temporario_cadastro, "xp_total": 0, "otp_code": "1234", "is_verified": False})
            salvar_json_local("data/users.json", usuarios)
            QMessageBox.information(self, "Modo Offline", "Usuário pré-cadastrado! Digite o código simulado '1234'.")
            self.stack_cadastro.setCurrentWidget(self.widget_etapa_otp)

    def executar_verificacao(self):
        codigo = self.txt_ver_codigo.text().strip()
        if not codigo: return
        try:
            res = requests.post(f"{BASE_URL}/verificar", json={"email": self.email_temporario_cadastro, "codigo": codigo})
            QMessageBox.information(self, "Ativação", res.json().get("mensagem", "Sua conta foi verificada!"))
            self.txt_login_email.setText(self.email_temporario_cadastro)
            self.stack_cadastro.setCurrentWidget(self.widget_etapa_dados)
            self.abas_auth.setCurrentIndex(0)
        except:
            usuarios = carregar_json_local("data/users.json")
            verificado = False
            for u in usuarios:
                if u["email"] == self.email_temporario_cadastro and u.get("otp_code") == codigo:
                    u["is_verified"] = True
                    verificado = True
                    break
            if verificado:
                salvar_json_local("data/users.json", usuarios)
                QMessageBox.information(self, "Sucesso", "Conta ativada com sucesso localmente! Faça o login.")
                self.txt_login_email.setText(self.email_temporario_cadastro)
                self.stack_cadastro.setCurrentWidget(self.widget_etapa_dados)
                self.abas_auth.setCurrentIndex(0)
            else:
                QMessageBox.critical(self, "Erro", "Código OTP incorreto.")


class TelaPartidaQuiz(QWidget):
    def __init__(self, quiz_id, perguntas, alternativas, callback_fim, sala_codigo_ativo=None):
        super().__init__()
        self.quiz_id = quiz_id
        self.perguntas = perguntas
        self.alternativas = alternativas
        self.callback_fim = callback_fim
        self.sala_codigo_ativo = sala_codigo_ativo  # Sabe se os pontos vêm de uma sala multiplayer
        self.indice_atual = 0
        self.respostas_certas_contador = 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(20)

        self.hud_bar = QFrame()
        self.hud_bar.setObjectName("hudGameBar")
        layout_hud = QHBoxLayout(self.hud_bar)
        
        self.lbl_score_total = QLabel("🪙 Pontos: 0")
        self.lbl_score_total.setStyleSheet("font-weight: bold; font-size: 14px; color: #f59e0b;")
        
        self.lbl_progresso_questoes = QLabel("Progresso: 0 / 0")
        self.lbl_progresso_questoes.setStyleSheet("font-weight: bold; color: #818cf8;")
        self.lbl_progresso_questoes.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout_hud.addWidget(self.lbl_score_total)
        layout_hud.addStretch()
        layout_hud.addWidget(self.lbl_progresso_questoes)
        layout.addWidget(self.hud_bar)

        self.card = QFrame()
        self.card.setObjectName("cardPergunta")
        layout_card = QVBoxLayout(self.card)
        self.lbl_enunciado = QLabel("")
        self.lbl_enunciado.setWordWrap(True)
        self.lbl_enunciado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_enunciado.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        layout_card.addWidget(self.lbl_enunciado)
        layout.addWidget(self.card)

        self.botoes_alternativas = []
        for i in range(4):
            btn = QPushButton("")
            btn.setObjectName("btnAnswer")
            btn.clicked.connect(lambda checked, idx=i: self.validar_resposta(idx))
            layout.addWidget(btn)
            self.botoes_alternativas.append(btn)

        self.setLayout(layout)
        self.renderizar_pergunta()

    def renderizar_pergunta(self):
        if self.indice_atual >= len(self.perguntas):
            self.finalizar_jogo()
            return

        self.lbl_progresso_questoes.setText(f"Questão: {self.indice_atual + 1} / {len(self.perguntas)}")
        self.lbl_score_total.setText(f"🪙 Pontos: {self.respostas_certas_contador * 10}")

        self.pergunta_atual = self.perguntas[self.indice_atual]
        self.lbl_enunciado.setText(self.pergunta_atual.get("enunciado"))
        self.alts_atuais = [a for a in self.alternativas if a.get("pergunta_id") == self.pergunta_atual["id"]]
        
        for i, btn in enumerate(self.botoes_alternativas):
            if i < len(self.alts_atuais):
                btn.setText(self.alts_atuais[i].get("texto"))
                btn.show()
            else:
                btn.hide()

    def validar_resposta(self, idx_selecionado):
        if idx_selecionado >= len(self.alts_atuais): return
        alt = self.alts_atuais[idx_selecionado]
        
        if alt.get("correta") is True:
            QMessageBox.information(self, "Resultado", "✨ RESPOSTA CORRETA!")
            self.respostas_certas_contador += 1
            
            # Atualiza XP Global
            usuarios = carregar_json_local("data/users.json")
            for u in usuarios:
                if u["id"] == ID_USUARIO_LOGADO: u["xp_total"] = u.get("xp_total", 0) + 10
            salvar_json_local("data/users.json", usuarios)

            # 🛠️ MULTIPLAYER COMPETITIVO: Atualiza pontuação da sala local em tempo real
            if self.sala_codigo_ativo:
                salas = carregar_json_local("data/salas.json")
                for s in salas:
                    if s["codigo"] == self.sala_codigo_ativo:
                        for player in s["players"]:
                            if player["id"] == ID_USUARIO_LOGADO:
                                player["pontuacao"] = self.respostas_certas_contador * 10
                salvar_json_local("data/salas.json", salas)
        else:
            QMessageBox.critical(self, "Resultado", "❌ RESPOSTA INCORRETA!")
        
        self.indice_atual += 1
        self.renderizar_pergunta()

    def finalizar_jogo(self):
        tentativas = carregar_json_local("data/tentativas.json")
        tentativas.append({"id": str(uuid.uuid4()), "usuario_id": ID_USUARIO_LOGADO, "quiz_id": self.quiz_id, "pontuacao": self.respostas_certas_contador * 10, "status": "finalizado", "data_inicio": datetime.now().isoformat()})
        salvar_json_local("data/tentativas.json", tentativas)
        QMessageBox.information(self, "Fim da Partida", f"🎉 Quiz Concluído! Você computou {self.respostas_certas_contador * 10} pontos.")
        self.callback_fim()


class TelaDashboardJogo(QWidget):
    def __init__(self, callback_logout, callback_iniciar_partida):
        super().__init__()
        self.callback_logout = callback_logout
        self.callback_iniciar_partida = callback_iniciar_partida
        self.perguntas_temporarias_lote = []
        self.indices_perguntas_edicao = [] 
        self.id_quiz_sendo_modificado = None
        self.indice_pergunta_atual_edicao = 0 
        self.sala_codigo_conectada_lobby = None # Segura o código da sala ativa para o ranking do lobby
        self.init_ui()

    def init_ui(self):
        layout_principal = QHBoxLayout()
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebarArea")
        layout_sidebar = QVBoxLayout(sidebar)
        layout_sidebar.setContentsMargins(16, 30, 16, 30)
        layout_sidebar.setSpacing(4)

        lbl_logo = QLabel("QuizArena")
        lbl_logo.setStyleSheet("font-size: 22px; font-weight: bold; color: #ffffff; padding-left: 12px; margin-bottom: 25px;")
        layout_sidebar.addWidget(lbl_logo)

        lbl_cat_geral = QLabel("GERAL")
        lbl_cat_geral.setStyleSheet("font-size: 10px; font-weight: bold; color: #4c4966; padding-left: 12px; margin-top: 5px; margin-bottom: 4px;")
        layout_sidebar.addWidget(lbl_cat_geral)

        self.btn_nav_dashboard = QPushButton("  Dashboard")
        self.btn_nav_ranking = QPushButton("  Ranking")
        layout_sidebar.addWidget(self.btn_nav_dashboard)
        layout_sidebar.addWidget(self.btn_nav_ranking)

        lbl_cat_jogar = QLabel("JOGAR")
        lbl_cat_jogar.setStyleSheet("font-size: 10px; font-weight: bold; color: #4c4966; padding-left: 12px; margin-top: 15px; margin-bottom: 4px;")
        layout_sidebar.addWidget(lbl_cat_jogar)

        self.btn_nav_salas = QPushButton("  Salas Multiplayer")
        self.btn_nav_salas.setObjectName("btnMenu")
        self.btn_nav_salas.setCheckable(True)
        self.btn_nav_salas.clicked.connect(lambda: self.mudar_tela(4))
        layout_sidebar.addWidget(self.btn_nav_salas)

        lbl_cat_gerenciar = QLabel("GERENCIAR")
        lbl_cat_gerenciar.setStyleSheet("font-size: 10px; font-weight: bold; color: #4c4966; padding-left: 12px; margin-top: 15px; margin-bottom: 4px;")
        layout_sidebar.addWidget(lbl_cat_gerenciar)

        self.btn_nav_quizzes = QPushButton("  Criar um Quiz")
        self.btn_nav_historico = QPushButton("  Minhas Partidas")
        layout_sidebar.addWidget(self.btn_nav_quizzes)
        layout_sidebar.addWidget(self.btn_nav_historico)

        for btn in [self.btn_nav_dashboard, self.btn_nav_ranking, self.btn_nav_quizzes, self.btn_nav_historico]:
            btn.setObjectName("btnMenu")
            btn.setCheckable(True)

        self.btn_nav_dashboard.setChecked(True)
        self.btn_nav_dashboard.clicked.connect(lambda: self.mudar_tela(0))
        self.btn_nav_ranking.clicked.connect(lambda: self.mudar_tela(1))
        self.btn_nav_quizzes.clicked.connect(lambda: self.mudar_tela(2))
        self.btn_nav_historico.clicked.connect(lambda: self.mudar_tela(3))

        layout_sidebar.addStretch()

        btn_logout = QPushButton("Sair da Conta")
        btn_logout.setObjectName("btnDanger")
        btn_logout.clicked.connect(self.callback_logout)
        layout_sidebar.addWidget(btn_logout)

        layout_principal.addWidget(sidebar, stretch=1)

        self.container_telas = QStackedWidget()
        self.pag_dashboard = QWidget()
        self.pag_ranking = QWidget()
        self.pag_quizzes = QWidget()
        self.pag_historico = QWidget()
        self.pag_salas = QWidget() 

        self.container_telas.addWidget(self.pag_dashboard)
        self.container_telas.addWidget(self.pag_ranking)
        self.container_telas.addWidget(self.pag_quizzes)
        self.container_telas.addWidget(self.pag_historico)
        self.container_telas.addWidget(self.pag_salas)

        self.configurar_pag_dashboard()
        self.configurar_pag_ranking()
        self.configurar_pag_quizzes()
        self.configurar_pag_historico()
        self.configurar_pag_salas() 

        layout_principal.addWidget(self.container_telas, stretch=4)
        self.setLayout(layout_principal)

    def mudar_tela(self, indice):
        botoes = [self.btn_nav_dashboard, self.btn_nav_ranking, self.btn_nav_quizzes, self.btn_nav_historico, self.btn_nav_salas]
        for i, btn in enumerate(botoes):
            btn.setChecked(i == indice)
        self.container_telas.setCurrentIndex(indice)
        if indice == 2 and self.id_quiz_sendo_modificado is None:
            self.resetar_formulario_quiz()
        if indice == 4:
            self.atualizar_salas()

    def resetar_formulario_quiz(self):
        self.perguntas_temporarias_lote = []
        self.indices_perguntas_edicao = []
        self.id_quiz_sendo_modificado = None
        self.indice_pergunta_atual_edicao = 0
        self.txt_novo_titulo.clear()
        self.txt_enunciado.clear()
        self.txt_alt_a.clear()
        self.txt_alt_b.clear()
        self.txt_alt_c.clear()
        self.txt_alt_d.clear()
        self.cb_alternativa_correta.setCurrentIndex(0)
        self.lbl_pergunta_contagem.setText("<b>Configurar Pergunta 1 (Obrigatória):</b>")
        self.btn_remover_pergunta_editor.hide()

    def configurar_pag_dashboard(self):
        layout = QVBoxLayout(self.pag_dashboard)
        layout.setContentsMargins(35, 35, 35, 35)
        lbl = QLabel("Dashboard")
        lbl.setObjectName("lblMainHeader")
        layout.addWidget(lbl)
        
        lbl_sub = QLabel("Quizzes recentes")
        lbl_sub.setStyleSheet("color: #716e87; margin-bottom: 15px;")
        layout.addWidget(lbl_sub)

        self.lista_quizzes_visuais = QListWidget()
        layout.addWidget(self.lista_quizzes_visuais)

        layout_botoes = QHBoxLayout()
        btn_editar_lote = QPushButton("✏️ Editar Quiz Selecionado")
        btn_editar_lote.clicked.connect(self.abrir_editor_lote_completo)
        btn_excluir = QPushButton("❌ Excluir Quiz Selecionado")
        btn_excluir.clicked.connect(self.excluir_quiz_selecionado)
        layout_botoes.addWidget(btn_editar_lote)
        layout_botoes.addWidget(btn_excluir)
        layout.addLayout(layout_botoes)

        btn_iniciar = QPushButton("Iniciar Partida")
        btn_iniciar.setObjectName("btnPrimary")
        btn_iniciar.clicked.connect(self.jogar_quiz_selecionado)
        layout.addWidget(btn_iniciar)
        self.atualizar_quizzes()

    def atualizar_quizzes(self):
        self.lista_quizzes_visuais.clear()
        for q in carregar_json_local("data/quizzes.json"):
            self.lista_quizzes_visuais.addItem(f"📝 {q['titulo']} [{q['dificuldade'].upper()}] - ID: {q['id']}")

    def jogar_quiz_selecionado(self):
        item = self.lista_quizzes_visuais.currentItem()
        if not item: return
        quiz_id = item.text().split(" - ID: ")[1].strip()
        perguntas = [p for p in carregar_json_local("data/perguntas.json") if p["quiz_id"] == quiz_id]
        if perguntas:
            self.callback_iniciar_partida(quiz_id, perguntas, carregar_json_local("data/alternativas.json"), None)
        else:
            QMessageBox.warning(self, "Aviso", "Esse quiz contêiner ainda não possui perguntas vinculadas!")

    def abrir_editor_lote_completo(self):
        item = self.lista_quizzes_visuais.currentItem()
        if not item: return

        self.id_quiz_sendo_modificado = item.text().split(" - ID: ")[1].strip()
        quizzes = carregar_json_local("data/quizzes.json")
        quiz = next((q for q in quizzes if q["id"] == self.id_quiz_sendo_modificado), None)

        if quiz:
            self.txt_novo_titulo.setText(quiz["titulo"])
            self.cb_dificuldade.setCurrentText(quiz["dificuldade"])
            todas_perguntas = carregar_json_local("data/perguntas.json")
            self.indices_perguntas_edicao = [p for p in todas_perguntas if p["quiz_id"] == self.id_quiz_sendo_modificado]

            if not self.indices_perguntas_edicao:
                QMessageBox.warning(self, "Aviso", "Este quiz não possui perguntas salvas.")
                return

            self.indice_pergunta_atual_edicao = 0
            self.mudar_tela(2) 
            self.carregar_pergunta_lote_no_formulario()

    def carregar_pergunta_lote_no_formulario(self):
        if self.indice_pergunta_atual_edicao >= len(self.indices_perguntas_edicao):
            quizzes = carregar_json_local("data/quizzes.json")
            for q in quizzes:
                if q["id"] == self.id_quiz_sendo_modificado:
                    q["titulo"] = self.txt_novo_titulo.text().strip()
                    q["dificuldade"] = self.cb_dificuldade.currentText()
            salvar_json_local("data/quizzes.json", quizzes)

            QMessageBox.information(self, "Concluído", "Todas as perguntas desse quiz foram salvas!")
            self.resetar_formulario_quiz()
            self.mudar_tela(0)
            self.atualizar_quizzes()
            return

        self.btn_remover_pergunta_editor.show() 
        perg = self.indices_perguntas_edicao[self.indice_pergunta_atual_edicao]
        self.lbl_pergunta_contagem.setText(f"<b>Modificando Pergunta {self.indice_pergunta_atual_edicao + 1} de {len(self.indices_perguntas_edicao)}:</b>")
        self.txt_enunciado.setText(perg["enunciado"])

        alts = [a for a in carregar_json_local("data/alternativas.json") if a["pergunta_id"] == perg["id"]]
        if len(alts) >= 4:
            self.txt_alt_a.setText(alts[0]["texto"])
            self.txt_alt_b.setText(alts[1]["texto"])
            self.txt_alt_c.setText(alts[2]["texto"])
            self.txt_alt_d.setText(alts[3]["texto"])
            
            certa_pos = next((idx for idx, a in enumerate(alts) if a["correta"] is True), 0)
            self.cb_alternativa_correta.setCurrentIndex(certa_pos)

    def excluir_pergunta_editor_fluxo(self):
        if not self.indices_perguntas_edicao or self.id_quiz_sendo_modificado is None: return
        
        perg_a_remover = self.indices_perguntas_edicao[self.indice_pergunta_atual_edicao]
        
        perguntas = carregar_json_local("data/perguntas.json")
        perguntas = [p for p in perguntas if p["id"] != perg_a_remover["id"]]
        salvar_json_local("data/perguntas.json", perguntas)

        alternativas = carregar_json_local("data/alternativas.json")
        alternativas = [a for a in alternativas if a["pergunta_id"] != perg_a_remover["id"]]
        salvar_json_local("data/alternativas.json", alternativas)

        self.indices_perguntas_edicao.pop(self.indice_pergunta_atual_edicao)
        
        if not self.indices_perguntas_edicao:
            QMessageBox.information(self, "Aviso", "O quiz ficou vazio!")
            self.resetar_formulario_quiz()
            self.mudar_tela(0)
            self.atualizar_quizzes()
            return

        if self.indice_pergunta_atual_edicao >= len(self.indices_perguntas_edicao):
            self.indice_pergunta_atual_edicao = max(0, len(self.indices_perguntas_edicao) - 1)

        QMessageBox.information(self, "Removido", "Pergunta excluída!")
        self.carregar_pergunta_lote_no_formulario()

    def excluir_quiz_selecionado(self):
        item = self.lista_quizzes_visuais.currentItem()
        if not item: return
        quiz_id = item.text().split(" - ID: ")[1].strip()
        
        quizzes = [q for q in carregar_json_local("data/quizzes.json") if q["id"] != quiz_id]
        salvar_json_local("data/quizzes.json", quizzes)
        self.atualizar_quizzes()

    def configurar_pag_quizzes(self):
        layout = QVBoxLayout(self.pag_quizzes)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(8)

        lbl = QLabel("Criar Novo Quiz")
        lbl.setObjectName("lblMainHeader")
        layout.addWidget(lbl)

        self.txt_novo_titulo = QLineEdit()
        self.txt_novo_titulo.setPlaceholderText("Título do Quiz Contêiner (Ex: Astronomia)")
        layout.addWidget(self.txt_novo_titulo)

        self.cb_dificuldade = QComboBox()
        self.cb_dificuldade.addItems(["easy", "medium", "hard"])
        layout.addWidget(self.cb_dificuldade)

        self.lbl_pergunta_contagem = QLabel("<b>Configurar Pergunta 1 (Obrigatória):</b>")
        self.lbl_pergunta_contagem.setStyleSheet("color: #a78bfa; margin-top: 10px;")
        layout.addWidget(self.lbl_pergunta_contagem)

        self.txt_enunciado = QLineEdit()
        self.txt_enunciado.setPlaceholderText("Enunciado da Questão")
        layout.addWidget(self.txt_enunciado)

        self.txt_alt_a = QLineEdit()
        self.txt_alt_a.setPlaceholderText("Alternativa A")
        self.txt_alt_b = QLineEdit()
        self.txt_alt_b.setPlaceholderText("Alternativa B")
        self.txt_alt_c = QLineEdit()
        self.txt_alt_c.setPlaceholderText("Alternativa C")
        self.txt_alt_d = QLineEdit()
        self.txt_alt_d.setPlaceholderText("Alternativa D")

        layout.addWidget(self.txt_alt_a)
        layout.addWidget(self.txt_alt_b)
        layout.addWidget(self.txt_alt_c)
        layout.addWidget(self.txt_alt_d)

        self.cb_alternativa_correta = QComboBox()
        self.cb_alternativa_correta.addItems(["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D"])
        layout.addWidget(self.cb_alternativa_correta)

        layout_botoes_fluxo = QHBoxLayout()
        self.btn_add_outra = QPushButton("➕ Adicionar Outra Pergunta")
        self.btn_add_outra.setObjectName("btnSecondary")
        self.btn_add_outra.clicked.connect(self.armazenar_pergunta_em_memoria)
        
        self.btn_finalizar_lote = QPushButton("💾 Salvar e Finalizar Quiz")
        self.btn_finalizar_lote.setObjectName("btnPrimary")
        self.btn_finalizar_lote.clicked.connect(self.salvar_quiz_e_lote_completo)
        
        layout_botoes_fluxo.addWidget(self.btn_add_outra)
        layout_botoes_fluxo.addWidget(self.btn_finalizar_lote)
        layout.addLayout(layout_botoes_fluxo)

        self.btn_remover_pergunta_editor = QPushButton("❌ Remover Esta Pergunta do Quiz")
        self.btn_remover_pergunta_editor.setObjectName("btnDanger")
        self.btn_remover_pergunta_editor.clicked.connect(self.excluir_pergunta_editor_fluxo)
        self.btn_remover_pergunta_editor.hide()
        layout.addWidget(self.btn_remover_pergunta_editor)

    def armazenar_pergunta_em_memoria(self):
        enunciado = self.txt_enunciado.text().strip()
        alt_a = self.txt_alt_a.text().strip()
        alt_b = self.txt_alt_b.text().strip()
        alt_c = self.txt_alt_c.text().strip()
        alt_d = self.txt_alt_d.text().strip()

        if not enunciado or not all([alt_a, alt_b, alt_c, alt_d]): return

        pergunta = {
            "pergunta_id": str(uuid.uuid4()), "enunciado": enunciado,
            "alternativas": [
                {"texto": alt_a, "marcada": "Alternativa A"},
                {"texto": alt_b, "marcada": "Alternativa B"},
                {"texto": alt_c, "marcada": "Alternativa C"},
                {"texto": alt_d, "marcada": "Alternativa D"}
            ],
            "correta": self.cb_alternativa_correta.currentText()
        }
        self.perguntas_temporarias_lote.append(pergunta)

        self.txt_enunciado.clear()
        self.txt_alt_a.clear()
        self.txt_alt_b.clear()
        self.txt_alt_c.clear()
        self.txt_alt_d.clear()
        self.cb_alternativa_correta.setCurrentIndex(0)
        
        self.lbl_pergunta_contagem.setText(f"<b>Configurar Pergunta {len(self.perguntas_temporarias_lote)+1}:</b>")

    def salvar_quiz_e_lote_completo(self):
        if self.id_quiz_sendo_modificado is not None:
            perg = self.indices_perguntas_edicao[self.indice_pergunta_atual_edicao]
            
            perguntas_banco = carregar_json_local("data/perguntas.json")
            for p in perguntas_banco:
                if p["id"] == perg["id"]: p["enunciado"] = self.txt_enunciado.text().strip()
            salvar_json_local("data/perguntas.json", perguntas_banco)

            alternativas_banco = carregar_json_local("data/alternativas.json")
            alts_locais = [a for a in alternativas_banco if a["pergunta_id"] == perg["id"]]
            novos_textos = [self.txt_alt_a.text().strip(), self.txt_alt_b.text().strip(), self.txt_alt_c.text().strip(), self.txt_alt_d.text().strip()]
            marcas = ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D"]
            qual_certa = self.cb_alternativa_correta.currentText()

            for i, alt_obj in enumerate(alts_locais):
                if i < len(novos_textos):
                    alt_obj["texto"] = novos_textos[i]
                    alt_obj["correta"] = (marcas[i] == qual_certa)
            salvar_json_local("data/alternativas.json", alternativas_banco)

            self.indice_pergunta_atual_edicao += 1
            self.carregar_pergunta_lote_no_formulario()
            return

        titulo = self.txt_novo_titulo.text().strip()
        if not titulo: return

        enunciado = self.txt_enunciado.text().strip()
        if enunciado: self.armazenar_pergunta_em_memoria()

        if not self.perguntas_temporarias_lote: return

        quiz_id = str(uuid.uuid4())
        quizzes = carregar_json_local("data/quizzes.json")
        quizzes.append({"id": quiz_id, "titulo": titulo, "tema_id": "30e567ad-e151-4c16-922f-0405ae9ad685", "criado_por": ID_USUARIO_LOGADO, "dificuldade": self.cb_dificuldade.currentText(), "publico": True})
        salvar_json_local("data/quizzes.json", quizzes)

        perguntas_banco = carregar_json_local("data/perguntas.json")
        alternativas_banco = carregar_json_local("data/alternativas.json")

        for p_temp in self.perguntas_temporarias_lote:
            perguntas_banco.append({"id": p_temp["pergunta_id"], "quiz_id": quiz_id, "enunciado": p_temp["enunciado"], "tipo": "multipla_escolha", "dificuldade": "easy", "data_creation": datetime.now().isoformat()})
            for alt in p_temp["alternativas"]:
                alternativas_banco.append({"id": str(uuid.uuid4()), "pergunta_id": p_temp["pergunta_id"], "texto": alt["texto"], "correta": (alt["marcada"] == p_temp["correta"]), "data_creation": datetime.now().isoformat()})

        salvar_json_local("data/perguntas.json", perguntas_banco)
        salvar_json_local("data/alternativas.json", alternativas_banco)

        QMessageBox.information(self, "Sucesso", f"Quiz '{titulo}' criado com sucesso!")
        self.resetar_formulario_quiz()
        self.atualizar_quizzes()

    # 🛠️ AREA MULTIPLAYER REFORMULADA DO SEU COLEGA
    def configurar_pag_salas(self):
        layout = QVBoxLayout(self.pag_salas)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(10)

        titulo = QLabel("Salas Multiplayer")
        titulo.setObjectName("lblMainHeader")
        layout.addWidget(titulo)

        self.lista_salas = QListWidget()
        layout.addWidget(self.lista_salas)

        self.txt_codigo_sala = QLineEdit()
        self.txt_codigo_sala.setPlaceholderText("Código de Entrada da Sala (5 Dígitos)")
        layout.addWidget(self.txt_codigo_sala)

        layout_btns = QHBoxLayout()
        btn_criar = QPushButton("➕ Criar Sala")
        btn_criar.setObjectName("btnPrimary")
        btn_criar.clicked.connect(self.criar_sala)

        btn_entrar = QPushButton("🚪 Entrar na Sala / Atualizar")
        btn_entrar.setObjectName("btnSecondary")
        btn_entrar.clicked.connect(self.entrar_sala)

        layout_btns.addWidget(btn_criar)
        layout_btns.addWidget(btn_entrar)
        layout.addLayout(layout_btns)

        # Arena do Lobby Ativo de Competição
        layout.addWidget(QLabel("<b>👥 Líderes e Competidores Conectados no Lobby:</b>"))
        self.lista_jogadores_sala = QListWidget()
        layout.addWidget(self.lista_jogadores_sala)

        # Botão de Start Síncrono da Competição
        self.btn_start_competicao_sala = QPushButton("🚀 Iniciar Competição Síncrona")
        self.btn_start_competicao_sala.setObjectName("btnPrimary")
        self.btn_start_competicao_sala.clicked.connect(self.disparar_partida_multiplayer_sala)
        self.btn_start_competicao_sala.hide()
        layout.addWidget(self.btn_start_competicao_sala)

    def atualizar_salas(self):
        self.lista_salas.clear()
        for sala in carregar_json_local("data/salas.json"):
            qtd = len(sala.get("players", []))
            self.lista_salas.addItem(f"🎮 Sala {sala['codigo']} │ Host ID: {sala['host_id'][:8]}... │ Competidores: {qtd}")

    def criar_sala(self):
        item = self.lista_quizzes_visuais.currentItem()
        if not item:
            QMessageBox.warning(self, "Aviso", "Selecione um quiz na aba 'Dashboard' antes de abrir a sala para competição!")
            return

        quiz_id = item.text().split(" - ID: ")[1].strip()
        salas = carregar_json_local("data/salas.json")
        codigo = gerar_codigo_sala()[:5] # Padroniza para 5 dígitos idêntico ao seu app web

        nova_sala = {
            "id": str(uuid.uuid4()), "codigo": codigo, "quiz_id": quiz_id,
            "host_id": ID_USUARIO_LOGADO, "status": "aguardando",
            "players": [{"id": ID_USUARIO_LOGADO, "nome": "Host Líder", "pontuacao": 0}]
        }
        salas.append(nova_sala)
        salvar_json_local("data/salas.json", salas)
        
        self.txt_codigo_sala.setText(codigo)
        self.entrar_sala()
        self.atualizar_salas()

    def entrar_sala(self):
        codigo = self.txt_codigo_sala.text().strip().upper()
        if not codigo: return

        salas = carregar_json_local("data/salas.json")
        sala = next((s for s in salas if s["codigo"] == codigo), None)

        if not sala:
            QMessageBox.critical(self, "Erro", "Sala de jogos não encontrada ou expirada.")
            return

        self.sala_codigo_conectada_lobby = codigo
        ja_existe = next((p for p in sala["players"] if p["id"] == ID_USUARIO_LOGADO), None)
        
        if not ja_existe:
            sala["players"].append({"id": ID_USUARIO_LOGADO, "nome": f"Competidor_{str(uuid.uuid4())[:4]}", "pontuacao": 0})
            salvar_json_local("data/salas.json", salas)

        self.lista_jogadores_sala.clear()
        ranking = sorted(sala["players"], key=lambda x: x["pontuacao"], reverse=True)
        for pos, player in enumerate(ranking):
            medalha = "🥇" if pos == 0 else "🥈" if pos == 1 else "🥉" if pos == 2 else f" {pos+1}º "
            self.lista_jogadores_sala.addItem(f"{medalha} {player['nome']} │ Placar: {player['pontuacao']} pts")

        # Exibe o botão de Start apenas se o usuário logado for o Host criador da sala
        if sala["host_id"] == ID_USUARIO_LOGADO:
            self.btn_start_competicao_sala.show()
        else:
            self.btn_start_competicao_sala.hide()

    def disparar_partida_multiplayer_sala(self):
        """🚀 ACIONADOR MULTIPLAYER: Inicia a partida do pacote de perguntas puxando o contexto competitivo"""
        if not self.sala_codigo_conectada_lobby: return
        
        salas = carregar_json_local("data/salas.json")
        sala = next((s for s in salas if s["codigo"] == self.sala_codigo_conectada_lobby), None)
        
        if sala:
            quiz_id = sala["quiz_id"]
            perguntas = [p for p in carregar_json_local("data/perguntas.json") if p["quiz_id"] == quiz_id]
            if perguntas:
                # Dispara passando o código da sala para atualizar o ranking competitivo dela
                self.callback_iniciar_partida(quiz_id, perguntas, carregar_json_local("data/alternativas.json"), self.sala_codigo_conectada_lobby)

    def configurar_pag_ranking(self):
        layout = QVBoxLayout(self.pag_ranking)
        layout.setContentsMargins(35, 35, 35, 35)
        lbl = QLabel("Ranking Global")
        lbl.setObjectName("lblMainHeader")
        layout.addWidget(lbl)
        self.lista_ranking_visual = QListWidget()
        layout.addWidget(self.lista_ranking_visual)
        self.atualizar_ranking()

    def atualizar_ranking(self):
        self.lista_ranking_visual.clear()
        ranking = sorted(carregar_json_local("data/users.json"), key=lambda u: u.get("xp_total", 0), reverse=True)
        for pos, u in enumerate(ranking):
            medalha = "🥇" if pos == 0 else "🥈" if pos == 1 else "🥉" if pos == 2 else f"  {pos+1}  "
            self.lista_ranking_visual.addItem(f"{medalha}  {u.get('nome').ljust(25)} │   {u.get('xp_total', 0)} XP")

    def configurar_pag_historico(self):
        layout = QVBoxLayout(self.pag_historico)
        layout.setContentsMargins(35, 35, 35, 35)
        lbl = QLabel("Minhas Partidas")
        lbl.setObjectName("lblMainHeader")
        layout.addWidget(lbl)
        self.lista_historico_visual = QListWidget()
        layout.addWidget(self.lista_historico_visual)
        self.atualizar_historico()

    def atualizar_historico(self):
        self.lista_historico_visual.clear()
        quizzes = carregar_json_local("data/quizzes.json")
        mapa_quizzes = {q["id"]: q["titulo"] for q in quizzes}

        minhas = [t for t in carregar_json_local("data/tentativas.json") if t.get("usuario_id") == ID_USUARIO_LOGADO]
        minhas = sorted(minhas, key=lambda x: x.get("data_inicio", ""), reverse=True)

        for m in minhas:
            nome_q = mapa_quizzes.get(m.get("quiz_id"), "Quiz Desconhecido")
            self.lista_historico_visual.addItem(f"🎮 {nome_q} │ +{m.get('pontuacao', 0)} XP")


class AppPrincipal(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(QUIZIFY_STYLE)
        self.tela_auth = TelaAutenticacao(self.liberar_dashboard_jogo)
        self.addWidget(self.tela_auth)
        self.setCurrentWidget(self.tela_auth)
        self.setWindowTitle("QuizArena Engine")
        self.resize(880, 600)

    def liberar_dashboard_jogo(self):
        if not hasattr(self, "tela_dashboard"):
            self.tela_dashboard = TelaDashboardJogo(self.retornar_ao_login, self.abrir_partida_ativa)
            self.addWidget(self.tela_dashboard)
        self.setCurrentWidget(self.tela_dashboard)

    def abrir_partida_ativa(self, quiz_id, perguntas, alternativas, sala_codigo_ativo=None):
        self.tela_partida = TelaPartidaQuiz(quiz_id, perguntas, alternativas, self.retornar_ao_dashboard, sala_codigo_ativo)
        self.addWidget(self.tela_partida)
        self.setCurrentWidget(self.tela_partida)

    def retornar_ao_dashboard(self):
        self.tela_dashboard.atualizar_historico()
        self.tela_dashboard.atualizar_ranking()
        self.tela_dashboard.atualizar_quizzes()
        self.tela_dashboard.atualizar_salas()
        self.setCurrentWidget(self.tela_dashboard)

    def retornar_ao_login(self):
        global TOKEN_USUARIO, ID_USUARIO_LOGADO
        TOKEN_USUARIO = None
        ID_USUARIO_LOGADO = None
        self.setCurrentWidget(self.tela_auth)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    main_window = AppPrincipal()
    main_window.show()
    sys.exit(app.exec())