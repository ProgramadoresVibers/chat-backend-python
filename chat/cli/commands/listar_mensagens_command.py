from commands.command import Command


class ListarMensagensCommand(Command):
    def __init__(self, servico_chat):
        self.servico_chat = servico_chat

    def validar(self, id_sala):
        self.validar_inteiro_positivo(id_sala, "Id da sala")

    def executar(self, id_sala):
        return self.servico_chat.listar_mensagens(id_sala)
