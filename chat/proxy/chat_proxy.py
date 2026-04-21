from domain.interfaces.chat_operacoes import ChatOperacoesInterface
from domain.shared.resultado import Resultado


class ChatProxy(ChatOperacoesInterface):
    def __init__(self, chat_facade: ChatOperacoesInterface):
        self._chat_facade = chat_facade

    def criar_novo_usuario(self, nome: str):
        print("[LOG] Criando novo Usuario...")
        resultado = self._chat_facade.criar_novo_usuario(nome)
        return Resultado.ok(resultado)

    def criar_nova_sala(self, nome: str):
        print("[LOG] Criando nova Sala...")
        resultado = self._chat_facade.criar_nova_sala(nome)
        return Resultado.ok(resultado)

    def listar_salas(self):
        return Resultado.ok(self._chat_facade.listar_salas())

    def enviar_mensagem(self, texto: str, id_sala: int, id_usuario: int):
        if not texto.strip():
            raise Resultado.falha("Mensagem não pode ser vazia")

        print("[LOG] Enviando nova mensagem...")
        self._chat_facade.enviar_mensagem(texto, id_sala, id_usuario)

    def listar_mensagens(self):
        return self._chat_facade.listar_mensagens()

    def apagar_mensagem(self, id_mensagem: int, id_usuario: int):
        print("[LOG] Apagando mensagem...")
        self._chat_facade.apagar_mensagem(id_mensagem, id_usuario)