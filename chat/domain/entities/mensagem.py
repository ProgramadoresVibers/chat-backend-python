from sala import Sala
from usuario import Usuario
class Mensagem:
    def __init__(self, id_mensagem, texto, sala, usuario):
        self._id_mensagem = id_mensagem
        self._texto = texto
        self._sala = sala
        self._usuario = usuario

    def get_id_mensagem(self):
        return self._id_mensagem

    def get_texto(self) -> str:
        return self._texto

    def get_sala(self) -> Sala:
        return self._sala

    def get_usuario(self) -> Usuario:
        return self._usuario

    def _formatar_mensagem(self) -> str:
        return f"{self.get_usuario()}:\n{self.get_texto()}"