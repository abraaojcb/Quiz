from flask import Blueprint, jsonify
from controllers.ranking_controller import RankingController
from utils.auth_middleware import token_obrigatorio 

ranking_bp = Blueprint("ranking", __name__)

@ranking_bp.route("/ranking/global", methods=["GET"])
def ranking_global():
    resposta, status = RankingController.obter_ranking_global()
    return jsonify(resposta), status

@ranking_bp.route("/ranking/sala/<id_sala>", methods=["GET"])
@token_obrigatorio # Agora o Python vai saber o que é isso
def ranking_da_sala(usuario_token, id_sala):
    resposta, status = RankingController.obter_ranking_sala(id_sala)
    return jsonify(resposta), status