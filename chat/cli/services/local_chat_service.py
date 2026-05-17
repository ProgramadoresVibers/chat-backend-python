from services.chat_service import ChatService
import  sys
import os
sys.path.append(r'C:\Users\Estêvan S.S\Documents\prjote-alex\chat-backend-python')
from chat.domain.entities.message import Mensagem
from chat.domain.entities.room import Sala
from chat.domain.entities.user import Usuario
from chat.domain.proxies.chat_proxy import ChatProxy
from chat.domain.services.chat_facade import ChatFacade


class LocalChatService(ChatService):
    def __init__(self, chat=None):
        self.chat = chat or ChatProxy(ChatFacade())

    def _resposta(self, resultado):
        if not resultado.sucesso:
            return {"sucesso": False, "erro": resultado.erro}

        return {"sucesso": True, "conteudo": self._serializar(resultado.conteudo)}

    def _serializar(self, conteudo):
        if isinstance(conteudo, Usuario):
            return {
                "id_usuario": conteudo.get_id_usuario(),
                "nome": conteudo.get_nome(),
            }

        if isinstance(conteudo, Sala):
            return {
                "id_sala": conteudo.get_id_sala(),
                "nome": conteudo.get_nome(),
            }

        if isinstance(conteudo, Mensagem):
            return {
                "id_mensagem": conteudo.get_id_mensagem(),
                "texto": conteudo.get_texto(),
                "id_sala": conteudo.get_sala().get_id_sala(),
                "id_usuario": conteudo.get_usuario().get_id_usuario(),
                "visivel": conteudo.get_visivel(),
            }

        return conteudo

    def acessar_usuario(self, nome: str) -> dict:
        return self._resposta(self.chat.acessar_usuario(nome))

    def criar_usuario(self, nome: str) -> dict:
        return self._resposta(self.chat.criar_novo_usuario(nome))

    def entrar_sala(self, nome: str) -> dict:
        return self._resposta(self.chat.acessar_sala(nome))

    def criar_sala(self, nome: str) -> dict:
        return self._resposta(self.chat.criar_nova_sala(nome))

    def listar_salas(self) -> dict:
        return self._resposta(self.chat.listar_salas())

    def enviar_mensagem(self, texto: str, id_sala: int, id_usuario: int) -> dict:
        return self._resposta(self.chat.enviar_mensagem(texto, id_sala, id_usuario))

    def listar_mensagens(self, id_sala: int) -> dict:
        return self._resposta(self.chat.listar_mensagens(id_sala))

    def apagar_mensagem(self, id_sala: int, id_mensagem: int, id_usuario: int) -> dict:
        return self._resposta(self.chat.apagar_mensagem(id_mensagem, id_sala, id_usuario))
