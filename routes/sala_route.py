from flask import Blueprint, request, jsonify
from controllers.sala_controller import SalaController
from utils.auth_middleware import token_obrigatorio

sala_bp = Blueprint("sala", __name__)

@sala_bp.route("/salas", methods=["POST"])
@token_obrigatorio
def criar(usuario_token):
    dados = request.json
    resposta, status = SalaController.criar_sala(dados, usuario_token)
    return jsonify(resposta), status

@sala_bp.route("/salas", methods=["GET"])
@token_obrigatorio
def listar(usuario_token):
    resposta, status = SalaController.listar_salas()
    return jsonify(resposta), status

@sala_bp.route("/salas/entrar", methods=["POST"])
@token_obrigatorio
def entrar(usuario_token):
    dados = request.json
    resposta, status = SalaController.entrar_na_sala(dados, usuario_token)
    return jsonify(resposta), status

@sala_bp.route("/salas/<id>/iniciar", methods=["PUT"])
@token_obrigatorio
def iniciar_jogo(usuario_token, id): # Lembre da ordem que corrigimos antes!
    resposta, status = SalaController.iniciar_partida(id, usuario_token)
    return jsonify(resposta), status

@sala_bp.route("/salas/<id>/finalizar", methods=["PUT"])
@token_obrigatorio
def encerrar_sala(usuario_token, id):
    resposta, status = SalaController.finalizar_sala(id, usuario_token)
    return jsonify(resposta), status