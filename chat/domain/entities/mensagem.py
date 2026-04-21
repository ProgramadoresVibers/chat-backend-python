class Mensagem:
    def __init__(self, id_mensagem: int, texto: str, id_usuario: int, id_sala: int):
        self._id_mensagem = id_mensagem
        self._texto = texto
        self._sala = id_sala
        self._usuario = id_usuario

    def get_id_mensagem(self) -> int:
        return self._id_mensagem

    def get_texto(self):
        return self._texto

    def get_sala(self):
        return self._sala

    def get_usuario(self):
        return self._usuario

    def _formatar_mensagem(self):
        return f"{self.get_usuario()}:\n{self.get_texto()}"