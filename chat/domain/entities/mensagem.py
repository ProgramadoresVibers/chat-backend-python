class Mensagem:
    def __init__(self, id_mensagem, texto, sala, usuario):
        self._id_mensagem = id_mensagem
        self._texto = self._formatar_mensagem(texto, usuario.get_nome())
        self._sala = sala
        self._usuario = usuario

    def get_id_mensagem(self):
        return self._id_mensagem

    def get_texto(self):
        return self._texto

    def get_sala(self):
        return self._sala

    def get_usuario(self):
        return self._usuario

    def _formatar_mensagem(self, texto, nome_usuario):
        return nome_usuario + ":\n" + texto