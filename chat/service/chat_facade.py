from domain.interfaces.chat_operacoes import ChatOperacoesInterface
from domain.entities.usuario import Usuario
from domain.entities.sala import Sala
from domain.entities.mensagem import Mensagem


class ChatFacade(ChatOperacoesInterface):
    def __init__(self):
        self.usuarios = []
        self.salas = []
        self.mensagens = []

        self.id_usuario_seq = 1
        self.id_sala_seq = 1
        self.id_mensagem_seq = 1

    def criar_novo_usuario(self, nome: str) -> Usuario:
        usuario = Usuario(self.id_usuario_seq, nome)
        self.usuarios.append(usuario)
        self.id_usuario_seq += 1
        return usuario

    def criar_nova_sala(self, nome: str) -> Sala:
        sala = Sala(self.id_sala_seq, nome)
        self.salas.append(sala)
        self.id_sala_seq += 1
        return sala

    def listar_salas(self):
        return self.salas

    def enviar_mensagem(self, texto: str, id_sala: int, id_usuario: int):
        mensagem = Mensagem(self.id_mensagem_seq, texto, id_usuario, id_sala)
        self.mensagens.append(mensagem)
        self.id_mensagem_seq += 1

    def listar_mensagens(self):
        return self.mensagens

    def apagar_mensagem(self, id_mensagem: int, id_usuario: int):
        self.mensagens = [
            m for m in self.mensagens
            if not (m.id_mensagem == id_mensagem and m.id_usuario == id_usuario)
        ]