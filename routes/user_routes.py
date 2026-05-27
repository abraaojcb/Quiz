from flask import Blueprint, request, jsonify
from controllers.user_controller import UserController

# Cria um "pacote" de rotas para usuários
user_bp = Blueprint('user_routes', __name__)

# Rota de Cadastro (POST)
@user_bp.route('/cadastro', methods=['POST'])
def cadastro():
    dados = request.json
    resposta, status_code = UserController.cadastrar_usuario(dados)
    return jsonify(resposta), status_code

# Rota de Login (POST)
@user_bp.route('/login', methods=['POST'])
def login():
    dados = request.json
    resposta, status_code = UserController.fazer_login(dados)
    return jsonify(resposta), status_code

# Rota para validar o código OTP (POST)
@user_bp.route('/verificar', methods=['POST'])
def verificar_conta():
    dados = request.json
    resposta, status_code = UserController.verificar_otp(dados)
    return jsonify(resposta), status_code