from flask import Blueprint, request, jsonify
from controllers.alternativa_controller import AnswerOptionController
from utils.auth_middleware import token_obrigatorio

answer_bp = Blueprint("answers", __name__)

@answer_bp.route("/answers", methods=["POST"])
@token_obrigatorio
def criar_alternativa(usuario_token):
    dados = request.json
    resposta, status = AnswerOptionController.criar_alternativa(dados)
    return jsonify(resposta), status


@answer_bp.route("/answers", methods=["GET"])
@token_obrigatorio
def listar_alternativas(usuario_token):
    resposta, status = AnswerOptionController.listar_alternativas()
    return jsonify(resposta), status


@answer_bp.route("/answers/<id>", methods=["GET"])
@token_obrigatorio
def buscar_alternativa(id, usuario_token):
    resposta, status = AnswerOptionController.buscar_alternativa_por_id(id)
    return jsonify(resposta), status


@answer_bp.route("/answers/<id>", methods=["PUT"])
@token_obrigatorio
def atualizar_alternativa(id, usuario_token):
    dados = request.json
    resposta, status = AnswerOptionController.atualizar_alternativa(id, dados)
    return jsonify(resposta), status


@answer_bp.route("/answers/<id>", methods=["DELETE"])
@token_obrigatorio
def deletar_alternativa(id, usuario_token):
    resposta, status = AnswerOptionController.deletar_alternativa(id)
    return jsonify(resposta), status