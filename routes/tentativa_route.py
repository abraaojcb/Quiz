from flask import Blueprint, request, jsonify
from controllers.tentativa_controller import TentativaController
from utils.auth_middleware import token_obrigatorio

tentativa_bp = Blueprint("tentativa", __name__)

@tentativa_bp.route("/tentativas", methods=["POST"])
@token_obrigatorio
def iniciar(usuario_token):
    dados = request.json
    resposta, status = TentativaController.iniciar_tentativa(dados, usuario_token)
    return jsonify(resposta), status

@tentativa_bp.route("/tentativas/minhas", methods=["GET"])
@token_obrigatorio
def listar(usuario_token):
    resposta, status = TentativaController.listar_minhas_tentativas(usuario_token)
    return jsonify(resposta), status

@tentativa_bp.route("/tentativas/<id>/finalizar", methods=["PUT"])
@token_obrigatorio
def finalizar(usuario_token, id): # <--- Mudei a ordem aqui!
    # Agora o usuario_token recebe os dados do middleware e o id recebe o valor da URL
    resposta, status = TentativaController.finalizar_tentativa(id, usuario_token)
    return jsonify(resposta), status