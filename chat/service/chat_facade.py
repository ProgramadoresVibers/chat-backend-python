from domain.interfaces.chat_operacoes import ChatOperacoesInterface
from domain.entities.usuario import Usuario
from domain.entities.sala import Sala
from domain.entities.mensagem import Mensagem
from domain.shared.resultado import Resultado
from infraestructure.gerenciador_json import GerenciadorJson
import os

class ChatFacade(ChatOperacoesInterface):
    def __init__(self):
        self.usuarios_path = 'chat/data/usuarios.json'
        self.salas_path = 'chat/data/salas.json'
        self.mensagens_path = 'chat/data/mensagens.json'
        os.makedirs('chat/data', exist_ok=True)

    def criar_novo_usuario(self, nome: str) -> Resultado:
        usuarios = GerenciadorJson.ler_arquivo(self.usuarios_path).conteudo
        # Verifica se já existe usuário com o mesmo nome
        if any(u['nome'].lower() == nome.lower() for u in usuarios):
            return Resultado.falha('Já existe um usuário com esse nome')
        novo_id = 1 if not usuarios else max(u['id_usuario'] for u in usuarios) + 1
        usuario = {'id_usuario': novo_id, 'nome': nome}
        res = GerenciadorJson.adicionar_item(self.usuarios_path, usuario)
        if res.sucesso:
            return Resultado.ok(Usuario(usuario['id_usuario'], usuario['nome']))
        return res

    def criar_nova_sala(self, nome: str) -> Resultado:
        salas = GerenciadorJson.ler_arquivo(self.salas_path).conteudo
        # Verifica se já existe sala com o mesmo nome
        if any(s['nome'].lower() == nome.lower() for s in salas):
            return Resultado.falha('Já existe uma sala com esse nome')
        novo_id = 1 if not salas else max(s['id_sala'] for s in salas) + 1
        sala = {'id_sala': novo_id, 'nome': nome}
        res = GerenciadorJson.adicionar_item(self.salas_path, sala)
        if res.sucesso:
            return Resultado.ok(Sala(sala['id_sala'], sala['nome']))
        return res

    def listar_salas(self) -> Resultado:
        salas = GerenciadorJson.ler_arquivo(self.salas_path).conteudo
        return Resultado.ok([
            Sala(s['id_sala'], s['nome'])
            for s in salas
        ])

    def enviar_mensagem(self, texto: str, id_sala: int, id_usuario: int) -> Resultado:
        salas = GerenciadorJson.ler_arquivo(self.salas_path).conteudo
        usuarios = GerenciadorJson.ler_arquivo(self.usuarios_path).conteudo
        sala_existe = any(s['id_sala'] == id_sala for s in salas)
        usuario_existe = any(u['id_usuario'] == id_usuario for u in usuarios)
        
        if not sala_existe:
            return Resultado.falha('Sala não existe')
        if not usuario_existe:
            return Resultado.falha('Usuário não existe')
        mensagens = GerenciadorJson.ler_arquivo(self.mensagens_path).conteudo
        novo_id = 1 if not mensagens else max(m['id_mensagem'] for m in mensagens) + 1
        mensagem = {'id_mensagem': novo_id, 'texto': texto, 'id_usuario': id_usuario, 'id_sala': id_sala}
        res = GerenciadorJson.adicionar_item(self.mensagens_path, mensagem)
        if res.sucesso:
            return Resultado.ok(Mensagem(mensagem['id_mensagem'], mensagem['texto'], mensagem['id_usuario'], mensagem['id_sala']))
        return res

    def listar_mensagens(self, id_sala: int) -> Resultado:
        mensagens = GerenciadorJson.ler_arquivo(self.mensagens_path).conteudo
        msgs = []
        for m in mensagens:
            if m['id_sala'] == id_sala:
                msgs.append(Mensagem(m['id_mensagem'], m['texto'], m['id_usuario'], m['id_sala']))
        return Resultado.ok(msgs)

    def apagar_mensagem(self, id_mensagem: int, id_usuario: int) -> Resultado:
        mensagens = GerenciadorJson.ler_arquivo(self.mensagens_path).conteudo
        mensagem = next(
            (m for m in mensagens if m['id_mensagem'] == id_mensagem and m['id_usuario'] == id_usuario),
            None
        )
        if not mensagem:
            return Resultado.falha('Mensagem não encontrada ou usuário não autorizado')
        res = GerenciadorJson.remover_item(self.mensagens_path, id_mensagem=id_mensagem, id_usuario=id_usuario)
        if res.sucesso:
            return Resultado.ok()
        return res