from chat.cli.commands.command import Command


class ApagarMensagemCommand(Command):
    def __init__(self, servico_chat):
        self.servico_chat = servico_chat

    def validar(self, id_sala, id_mensagem, id_usuario):
        self.validar_inteiro_positivo(id_sala, "Id da sala")
        self.validar_inteiro_positivo(id_mensagem, "Id da mensagem")
        self.validar_inteiro_positivo(id_usuario, "Id do usuario")

    def executar(self, id_sala, id_mensagem, id_usuario):
        return self.servico_chat.apagar_mensagem(id_sala, id_mensagem, id_usuario)
