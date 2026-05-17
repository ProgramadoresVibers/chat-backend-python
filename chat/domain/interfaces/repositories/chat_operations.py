from abc import ABC, abstractmethod

from chat.domain.entities.user import Usuario
from chat.domain.entities.room import Sala
from chat.domain.entities.message import Mensagem
from chat.domain.shared.result import Resultado


class ChatOperacoesInterface(ABC):

    @abstractmethod
    def acessar_usuario(self, nome: str) -> Resultado[Usuario]:
        pass

    @abstractmethod
    def acessar_sala(self, nome: str) -> Resultado[Sala]:
        pass

    @abstractmethod
    def criar_novo_usuario(self, nome: str) -> Resultado[Usuario]:
        pass

    @abstractmethod
    def criar_nova_sala(self, nome: str) -> Resultado[Sala]:
        pass

    @abstractmethod
    def listar_salas(self) -> Resultado[list[dict]]:
        pass

    @abstractmethod
    def enviar_mensagem(self, texto: str, id_sala: int, id_usuario: int) -> Resultado[Mensagem]:
        pass

    @abstractmethod
    def listar_mensagens(self, id_sala: int) -> Resultado[list[dict]]:
        pass

    @abstractmethod
    def apagar_mensagem(self, id_mensagem: int, id_sala: int, id_usuario: int) -> Resultado[None]:
        pass