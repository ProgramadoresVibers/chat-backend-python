class Usuario:
    def __init__(self, id_usuario, nome):
        self._id_usuario = id_usuario
        self._nome = nome

    def get_id_usuario(self):
        return self._id_usuario

    def get_nome(self):
        return self._nome