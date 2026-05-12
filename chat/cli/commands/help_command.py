from chat.cli.commands.command import Command


class HelpCommand(Command):
    def validar(self):
        pass

    def executar(self):
        return "\n".join(
            [
                "/help - Lista todos os comandos disponiveis.",
                "/criar_usuario <nome> - Cria um novo usuario.",
                "/login <nome> - Entra com um usuario existente.",
                "/criar_sala <nome> - Cria uma nova sala.",
                "/listar_salas - Lista as salas disponiveis.",
                "/entrar_sala <nome> - Entra em uma sala.",
                "/listar_mensagens - Lista as mensagens da sala atual.",
                "/enviar <texto> - Envia uma mensagem para a sala atual.",
                "/apagar - Apaga sua ultima mensagem visivel na sala atual.",
                "/sair - Encerra a CLI.",
            ]
        )
