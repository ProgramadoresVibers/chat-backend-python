from abc import ABC, abstractmethod


class ChatService(ABC):
    @abstractmethod
    def acessar_usuario(self, nome: str) -> dict:
        pass

    @abstractmethod
    def criar_usuario(self, nome: str) -> dict:
        pass

    @abstractmethod
    def entrar_sala(self, nome: str) -> dict:
        pass

    @abstractmethod
    def criar_sala(self, nome: str) -> dict:
        pass

    @abstractmethod
    def listar_salas(self) -> dict:
        pass

    @abstractmethod
    def enviar_mensagem(self, texto: str, id_sala: int, id_usuario: int) -> dict:
        pass

    @abstractmethod
    def listar_mensagens(self, id_sala: int) -> dict:
        pass

    @abstractmethod
    def apagar_mensagem(self, id_sala: int, id_mensagem: int, id_usuario: int) -> dict:
        pass
