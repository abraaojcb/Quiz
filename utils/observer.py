# utils/observer.py
from abc import ABC, abstractmethod

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def notify(self, sala_id, dados_atualizacao):
        for observer in self._observers:
            observer.update(sala_id, dados_atualizacao)

# Transformamos a classe em ABSTRATA (Uma regra estrita)
class SalaObserver(ABC):
    
    @abstractmethod
    def update(self, sala_id: str, dados_atualizacao: dict) -> None:
        """Qualquer classe que herdar daqui é OBRIGADA a ter esse método"""
        pass

# Motor global
motor_de_notificacoes = Subject()