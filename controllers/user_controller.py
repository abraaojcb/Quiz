# controllers/user_controller.py
import random
from models.user_model import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from utils.email_helper import enviar_email_otp
from utils.jwt_helper import gerar_token

class UserController:
    
    @staticmethod
    def cadastrar_usuario(dados):
        nome = dados.get("nome")
        email = dados.get("email")
        senha = dados.get("senha")
        
        if not nome or not email or not senha:
            return {"erro": "Nome, email e senha são obrigatórios!"}, 400
            
        if "@" not in email or "." not in email:
            return {"erro": "Formato de email inválido!"}, 400

        # 🔍 VALIDAÇÃO DO BANCO JSON: Verifica se o e-mail já existe no arquivo
        usuario_existente = UserModel.buscar_por_email(email)
        if usuario_existente:
            # Retorna 400 para alinhar perfeitamente com o tratamento de erro da nossa CLI
            return {"erro": "Este e-mail já está cadastrado no sistema!"}, 400
            
        # Criptografa a senha do usuário por segurança
        senha_hash = generate_password_hash(senha)
        
        # Gera o código numérico de 6 dígitos para o e-mail
        codigo_otp = str(random.randint(100000, 999999))
        
        # Monta a estrutura do usuário usando o molde do modelo
        novo_usuario = UserModel.criar_molde_usuario(
            nome, email, senha_hash, codigo_otp
        )

        # Salva o novo registro na base de dados JSON
        UserModel.salvar_usuario(novo_usuario)
        
        # Dispara o e-mail real com o token de ativação
        enviar_email_otp(email, codigo_otp)
        
        return {
            "mensagem": "Conta criada! Verifique seu e-mail para pegar o código de ativação.",
            "id": novo_usuario["id"]
        }, 201

    @staticmethod
    def verificar_otp(dados):
        email = dados.get("email")
        codigo_digitado = dados.get("codigo")

        if not email or not codigo_digitado:
            return {"erro": "Email e código são obrigatórios!"}, 400

        usuario = UserModel.buscar_por_email(email)
        if not usuario:
            return {"erro": "Usuário não encontrado!"}, 404

        if usuario.get("is_verified"):
            return {"mensagem": "Esta conta já está verificada!"}, 400

        # Valida se o código digitado bate com o que foi gerado no cadastro
        if usuario.get("otp_code") == codigo_digitado:
            # Modifica o status do usuário no arquivo JSON para True
            UserModel.atualizar_usuario(usuario["id"], {
                "is_verified": True,
                "otp_code": None
            })

            return {"mensagem": "Conta ativada com sucesso! Você já pode fazer login."}, 200
        else:
            return {"erro": "Código inválido ou incorreto!"}, 401

    @staticmethod
    def fazer_login(dados):
        email = dados.get("email")
        senha_digitada = dados.get("senha")
        
        if not email or not senha_digitada:
            return {"erro": "Email e senha são obrigatórios!"}, 400
            
        usuario = UserModel.buscar_por_email(email)
        if not usuario:
            return {"erro": "Usuário não encontrado!"}, 404
            
        # Bloqueia o login caso a conta não tenha passado pela Opção 2 da CLI
        if not usuario.get("is_verified"):
            return {
                "erro": "Conta não ativada! Por favor, ative com o código enviado para o seu e-mail."
            }, 403
            
        # Descriptografa e valida a senha
        if check_password_hash(usuario["senha"], senha_digitada):
            token = gerar_token(usuario)
            
            return {
                "mensagem": "Login realizado com sucesso!",
                "token": token,
                "usuario": {
                    "id": usuario["id"],
                    "nome": usuario["nome"]
                }
            }, 200
        else:
            return {"erro": "Senha incorreta!"}, 401