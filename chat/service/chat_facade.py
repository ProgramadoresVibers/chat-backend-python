from domain.interfaces.chat_operacoes import ChatOperacoesInterface
from domain.entities.usuario import Usuario
from domain.entities.sala import Sala
from domain.entities.mensagem import Mensagem
from domain.shared.resultado import Resultado


class ChatFacade(ChatOperacoesInterface):
    def __init__(self):
        self.usuarios = []
        self.salas = []
        self.mensagens = []

        self.id_usuario_seq = 1
        self.id_sala_seq = 1
        self.id_mensagem_seq = 1

    def criar_novo_usuario(self, nome: str) -> Resultado[Usuario]:
        usuario = Usuario(self.id_usuario_seq, nome)
        self.usuarios.append(usuario)
        self.id_usuario_seq += 1
        
        return Resultado.ok(usuario)

    def criar_nova_sala(self, nome: str) -> Resultado[Sala]:
        sala = Sala(self.id_sala_seq, nome)
        self.salas.append(sala)
        self.id_sala_seq += 1
        
        return Resultado.ok(sala)

    def listar_salas(self) -> Resultado[list[Sala]]:
        return Resultado.ok(self.salas)

    def enviar_mensagem(self, texto: str, id_sala: int, id_usuario: int) -> Resultado[Mensagem]:
        sala_existe = False
        for sala in self.salas:
            if sala.get_id_sala() == id_sala:
                sala_existe = True
                break

        usuario_existe = False
        for u in self.usuarios:
            if u.get_id_usuario() == id_usuario:
                usuario_existe = True
                break

        if not sala_existe:
            return Resultado.falha("Sala não existe")

        if not usuario_existe:
            return Resultado.falha("Usuário não existe")

        mensagem = Mensagem(self.id_mensagem_seq, texto, id_usuario, id_sala)
        self.mensagens.append(mensagem)
        self.id_mensagem_seq += 1
        
        return Resultado.ok(mensagem)

    def listar_mensagens(self, id_sala: int) -> Resultado[list[Mensagem]]:
        mensagens = []
        for mensagem in self.mensagens:
            if mensagem.get_id_mensagem() == id_sala:
                mensagens.append(mensagem)
                
        return Resultado.ok(mensagens)

    def apagar_mensagem(self, id_mensagem: int, id_usuario: int) -> Resultado[None]:
        novas_mensagens = []
        
        for mensagem in self.mensagens:
            if mensagem.get_id_mensagem() == id_mensagem and mensagem.get_id_usuario() == id_usuario:
                continue
            
            novas_mensagens.append(mensagem)
            
        self.mensagens = novas_mensagens
        
        return Resultado.ok(None)