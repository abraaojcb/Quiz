from flask import Blueprint, request, jsonify
from controllers.tema_controller import TemaController
from utils.auth_middleware import token_obrigatorio

tema_bp = Blueprint("temas", __name__)

@tema_bp.route("/temas", methods=["POST"])
@token_obrigatorio
def criar_tema(usuario_token):
    dados = request.json
    resposta, status = TemaController.criar_tema(dados)
    return jsonify(resposta), status

@tema_bp.route("/temas", methods=["GET"])
@token_obrigatorio
def listar_temas(usuario_token):
    resposta, status = TemaController.listar_temas()
    return jsonify(resposta), status

@tema_bp.route("/temas/<id>", methods=["GET"])
@token_obrigatorio
def buscar_tema(usuario_token, id):
    resposta, status = TemaController.buscar_tema_por_id(id)
    return jsonify(resposta), status

@tema_bp.route("/temas/<id>", methods=["PUT"])
@token_obrigatorio
def atualizar_tema(usuario_token, id):
    dados = request.json
    resposta, status = TemaController.atualizar_tema(id, dados)
    return jsonify(resposta), status

@tema_bp.route("/temas/<id>", methods=["DELETE"])
@token_obrigatorio
def deletar_tema(usuario_token, id):
    resposta, status = TemaController.deletar_tema(id)
    return jsonify(resposta), status