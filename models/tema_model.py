import datetime
import uuid

class TemaModel:
    @staticmethod
    def criar_molde_tema(nome, descricao=""):
        return {
            "id": str(uuid.uuid4()),
            "nome": nome.strip().lower(),
            "descricao": descricao,
            "data_criacao": datetime.datetime.now().isoformat()
        }