from commands.command import Command


class LoginCommand(Command):
    def __init__(self, servico_chat):
        self.servico_chat = servico_chat

    def validar(self, nome):
        self.validar_texto_obrigatorio(nome, "Nome")

    def executar(self, nome):
        return self.servico_chat.acessar_usuario(nome)
