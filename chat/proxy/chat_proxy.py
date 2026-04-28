from domain.interfaces.chat_operacoes import ChatOperacoesInterface
from domain.shared.resultado import Resultado
from infraestructure.gerenciador_json import GerenciadorJson


class ChatProxy(ChatOperacoesInterface):
    def __init__(self, chat_facade: ChatOperacoesInterface):
        self._chat_facade = chat_facade
        self.mensagens_path = 'chat/data/mensagens.json'

    def acessar_usuario(self, nome: str):
        if not nome or not nome.strip():
            return Resultado.falha("Nome do usuário não pode ser vazio")
        if len(nome.strip()) < 3:
            return Resultado.falha("Nome do usuário deve ter pelo menos 3 caracteres")

        return self._chat_facade.acessar_usuario(nome)

    # Criar um novo usuario.
    def criar_novo_usuario(self, nome: str):
        if not nome or not nome.strip():
            return Resultado.falha("Nome do usuário não pode ser vazio")
        if len(nome.strip()) < 3:
            return Resultado.falha("Nome do usuário deve ter pelo menos 3 caracteres")
        # Chama o ChatFacade para criar e persistir o usuário
        return self._chat_facade.criar_novo_usuario(nome)

    # Criar uma nova sala
    def criar_nova_sala(self, nome: str):
        if not nome or not nome.strip():
            return Resultado.falha("Nome da sala não pode ser vazio")
        if len(nome.strip()) < 3:
            return Resultado.falha("Nome da sala deve ter pelo menos 3 caracteres")
        return self._chat_facade.criar_nova_sala(nome)

    # Listar salas
    def listar_salas(self):
        return self._chat_facade.listar_salas()

    # Enviar mensagem
    def enviar_mensagem(self, texto: str, id_sala: int, id_usuario: int) -> Resultado:
        if not texto or not texto.strip():
            return Resultado.falha("Mensagem não pode ser vazia")
        if not isinstance(id_sala, int) or id_sala <= 0:
            return Resultado.falha("ID da sala inválido")
        if not isinstance(id_usuario, int) or id_usuario <= 0:
            return Resultado.falha("ID do usuário inválido")
        return self._chat_facade.enviar_mensagem(texto, id_sala, id_usuario)

    # Listar mensagens
    def listar_mensagens(self, id_sala: int) -> Resultado:
        if not isinstance(id_sala, int) or id_sala <= 0:
            return Resultado.falha("ID da sala inválido")
        return self._chat_facade.listar_mensagens(id_sala)

    # Apagar mensagem
    def apagar_mensagem(self, id_mensagem: int, id_sala: int, id_usuario: int):
        if not isinstance(id_mensagem, int) or id_mensagem <= 0:
            return Resultado.falha("ID da mensagem inválido")
        if not isinstance(id_sala, int) or id_sala <= 0:
            return Resultado.falha("ID da sala inválido")
        if not isinstance(id_usuario, int) or id_usuario <= 0:
            return Resultado.falha("ID do usuário inválido")
        resultado_leitura = GerenciadorJson.ler_arquivo(self.mensagens_path, id_mensagem=id_mensagem)

        if not resultado_leitura.sucesso:
            return resultado_leitura

        if not resultado_leitura.conteudo:
            return Resultado.falha("Mensagem não encontrada")

        mensagem = resultado_leitura.conteudo[0]

        if mensagem['id_usuario'] != id_usuario:
            return Resultado.falha("Usuário não tem permissão para apagar esta mensagem")
        if mensagem['id_sala'] != id_sala:
            return Resultado.falha("Não foi possível encontrar essa mensagem nesta sala")

        return self._chat_facade.apagar_mensagem(id_mensagem, id_sala, id_usuario)