from chat.cli.commands.command import Command


class CriarUsuarioCommand(Command):
    def __init__(self, servico_chat):
        self.servico_chat = servico_chat

    def validar(self, nome):
        self.validar_texto_obrigatorio(nome, "Nome")

    def executar(self, nome):
        return self.servico_chat.criar_usuario(nome)
