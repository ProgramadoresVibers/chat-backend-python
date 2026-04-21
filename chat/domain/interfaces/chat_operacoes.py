from abc import ABC, abstractmethod

from domain.entities.usuario import Usuario
from domain.entities.sala import Sala
from domain.entities.mensagem import Mensagem


class ChatOperacoesInterface(ABC):

    @abstractmethod
    def criar_novo_usuario(self, nome: str) -> Usuario:
        pass

    @abstractmethod
    def criar_nova_sala(self, nome: str) -> Sala:
        pass

    @abstractmethod
    def listar_salas(self) -> list[Sala]:
        pass

    @abstractmethod
    def enviar_mensagem(self, texto: str, id_sala: int, id_usuario: int) -> None:
        pass

    @abstractmethod
    def listar_mensagens(self) -> list[Mensagem]:
        pass

    @abstractmethod
    def apagar_mensagem(self, id_mensagem: int, id_usuario: int) -> None:
        pass