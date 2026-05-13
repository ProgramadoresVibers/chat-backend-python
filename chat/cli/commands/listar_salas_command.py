from commands.command import Command


class ListarSalasCommand(Command):
    def __init__(self, servico_chat):
        self.servico_chat = servico_chat

    def validar(self):
        pass

    def executar(self):
        return self.servico_chat.listar_salas()
