from flask import Blueprint, request, jsonify
from controllers.pergunta_controller import QuestionController
from utils.auth_middleware import token_obrigatorio

question_bp = Blueprint("questions", __name__)

# CREATE
@question_bp.route("/questions", methods=["POST"])
@token_obrigatorio
def criar_pergunta(usuario_token):
    dados = request.json
    resposta, status = QuestionController.criar_pergunta(dados)
    return jsonify(resposta), status

# READ ALL
@question_bp.route("/questions", methods=["GET"])
@token_obrigatorio
def listar_perguntas(usuario_token):
    resposta, status = QuestionController.listar_perguntas()
    return jsonify(resposta), status

# READ ONE
@question_bp.route("/questions/<id>", methods=["GET"])
@token_obrigatorio
def buscar_pergunta(id, usuario_token):
    resposta, status = QuestionController.buscar_pergunta_por_id(id)
    return jsonify(resposta), status

# UPDATE
@question_bp.route("/questions/<id>", methods=["PUT"])
@token_obrigatorio
def atualizar_pergunta(id, usuario_token):
    dados = request.json
    resposta, status = QuestionController.atualizar_pergunta(id, dados)
    return jsonify(resposta), status

# DELETE
@question_bp.route("/questions/<id>", methods=["DELETE"])
@token_obrigatorio
def deletar_pergunta(id, usuario_token):
    resposta, status = QuestionController.deletar_pergunta(id)
    return jsonify(resposta), status