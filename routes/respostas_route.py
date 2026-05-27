from flask import Blueprint, request, jsonify
from controllers.respostas_controller import RespostasController
from utils.auth_middleware import token_obrigatorio

respostas_bp = Blueprint("respostas", __name__)

@respostas_bp.route("/respostas", methods=["POST"])
@token_obrigatorio
def responder(usuario_token):
    dados = request.json
    resposta, status = RespostasController.salvar_resposta(dados)
    return jsonify(resposta), status