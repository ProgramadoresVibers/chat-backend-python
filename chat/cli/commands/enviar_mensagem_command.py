from chat.cli.commands.command import Command


class EnviarMensagemCommand(Command):
    def __init__(self, servico_chat):
        self.servico_chat = servico_chat

    def validar(self, texto, id_sala, id_usuario):
        self.validar_texto_obrigatorio(texto, "Mensagem")
        self.validar_inteiro_positivo(id_sala, "Id da sala")
        self.validar_inteiro_positivo(id_usuario, "Id do usuario")

    def executar(self, texto, id_sala, id_usuario):
        return self.servico_chat.enviar_mensagem(texto, id_sala, id_usuario)
