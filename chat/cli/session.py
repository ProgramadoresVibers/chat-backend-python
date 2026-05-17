class ChatSession:
    def __init__(self):
        self.usuario = None
        self.sala_atual = None

    def esta_logado(self):
        return self.usuario is not None

    def esta_em_sala(self):
        return self.sala_atual is not None
