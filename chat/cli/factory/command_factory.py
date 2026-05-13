from commands.apagar_mensagem_command import ApagarMensagemCommand
from commands.criar_sala_command import CriarSalaCommand
from commands.criar_usuario_command import CriarUsuarioCommand
from commands.entrar_sala_command import EntrarSalaCommand
from commands.enviar_mensagem_command import EnviarMensagemCommand
from commands.help_command import HelpCommand
from commands.listar_mensagens_command import ListarMensagensCommand
from commands.listar_salas_command import ListarSalasCommand
from commands.login_command import LoginCommand


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
