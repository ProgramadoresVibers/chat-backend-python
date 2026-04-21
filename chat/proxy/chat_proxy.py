from domain.interfaces.chat_operacoes import ChatOperacoesInterface
from domain.shared.resultado import Resultado


class ChatProxy(ChatOperacoesInterface):
    def __init__(self, chat_facade: ChatOperacoesInterface):
        self._chat_facade = chat_facade
        
    # Criar um novo usuario.
    def criar_novo_usuario(self, nome: str) -> Resultado:
        if not nome.strip():
            return Resultado.falha("Nome do usuario não pode ser vazio")

        print("[LOG] Criando novo usuário...")
        return self._chat_facade.criar_novo_usuario(nome)

    def criar_nova_sala(self, nome: str) -> Resultado:
        if not nome.strip():
            return Resultado.falha("Nome da sala não pode ser vazio")

        print("[LOG] Criando nova sala...")
        return self._chat_facade.criar_nova_sala(nome)

    def listar_salas(self) -> Resultado:
        return self._chat_facade.listar_salas()

    def enviar_mensagem(self, texto: str, id_sala: int, id_usuario: int) -> Resultado:
        if not texto.strip():
            return Resultado.falha("Mensagem não pode ser vazia")

        return self._chat_facade.enviar_mensagem(texto, id_sala, id_usuario)

    def listar_mensagens(self, id_sala: int) -> Resultado:
        return self._chat_facade.listar_mensagens(id_sala)

    def apagar_mensagem(self, id_mensagem: int, id_usuario: int) -> Resultado:
        return self._chat_facade.apagar_mensagem(id_mensagem, id_usuario)