from flask import Blueprint, request, jsonify
from controllers.quiz_controller import QuizController
from utils.auth_middleware import token_obrigatorio

quiz_bp = Blueprint("quizzes", __name__)

# CREATE
@quiz_bp.route("/quizzes", methods=["POST"])
@token_obrigatorio
def criar_quiz(usuario_token):
    dados = request.json
    resposta, status = QuizController.criar_quiz(dados, usuario_token)
    return jsonify(resposta), status


# READ ALL
@quiz_bp.route("/quizzes", methods=["GET"])
@token_obrigatorio
def listar_quizzes(usuario_token):
    resposta, status = QuizController.listar_quizzes()
    return jsonify(resposta), status


# READ ONE
@quiz_bp.route("/quizzes/<id>", methods=["GET"])
@token_obrigatorio
def buscar_quiz(id, usuario_token):
    resposta, status = QuizController.buscar_quiz_por_id(id)
    return jsonify(resposta), status


# UPDATE
@quiz_bp.route("/quizzes/<id>", methods=["PUT"])
@token_obrigatorio
def atualizar_quiz(id, usuario_token):
    dados = request.json
    resposta, status = QuizController.atualizar_quiz(id, dados)
    return jsonify(resposta), status


# DELETE
@quiz_bp.route("/quizzes/<id>", methods=["DELETE"])
@token_obrigatorio
def deletar_quiz(id, usuario_token):
    resposta, status = QuizController.deletar_quiz(id)
    return jsonify(resposta), status