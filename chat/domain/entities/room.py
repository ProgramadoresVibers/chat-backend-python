class Sala:
    def __init__(self, id_sala, nome):
        self._id_sala = id_sala
        self._nome = nome

    def get_id_sala(self):
        return self._id_sala

    def get_nome(self):
        return self._nome