from commands.command import Command


class CriarSalaCommand(Command):
    def __init__(self, servico_chat):
        self.servico_chat = servico_chat

    def validar(self, nome):
        self.validar_texto_obrigatorio(nome, "Nome da sala")

    def executar(self, nome):
        return self.servico_chat.criar_sala(nome)
