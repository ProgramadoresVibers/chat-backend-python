from chat.cli.commands.apagar_mensagem_command import ApagarMensagemCommand
from chat.cli.commands.criar_sala_command import CriarSalaCommand
from chat.cli.commands.criar_usuario_command import CriarUsuarioCommand
from chat.cli.commands.entrar_sala_command import EntrarSalaCommand
from chat.cli.commands.enviar_mensagem_command import EnviarMensagemCommand
from chat.cli.commands.help_command import HelpCommand
from chat.cli.commands.listar_mensagens_command import ListarMensagensCommand
from chat.cli.commands.listar_salas_command import ListarSalasCommand
from chat.cli.commands.login_command import LoginCommand


class CommandFactory:
    @staticmethod
    def criar_comandos(servico):
        return {
            "help": HelpCommand(),
            "login": LoginCommand(servico),
            "criar_usuario": CriarUsuarioCommand(servico),
            "criar_sala": CriarSalaCommand(servico),
            "listar_salas": ListarSalasCommand(servico),
            "entrar_sala": EntrarSalaCommand(servico),
            "listar_mensagens": ListarMensagensCommand(servico),
            "enviar_mensagem": EnviarMensagemCommand(servico),
            "apagar_mensagem": ApagarMensagemCommand(servico),
        }
