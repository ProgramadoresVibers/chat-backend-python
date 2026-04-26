from domain.interfaces.chat_operacoes import ChatOperacoesInterface
from domain.entities.usuario import Usuario
from domain.entities.sala import Sala
from domain.entities.mensagem import Mensagem
from domain.shared.resultado import Resultado
from infraestructure.gerenciador_json import GerenciadorJson
from factory.ChatFactory import ChatFactory
import os

class ChatFacade(ChatOperacoesInterface):
    def __init__(self):
        self.usuarios_path = 'chat/data/usuarios.json'
        self.salas_path = 'chat/data/salas.json'
        self.mensagens_path = 'chat/data/mensagens.json'
        os.makedirs('chat/data', exist_ok=True)

    def criar_novo_usuario(self, nome: str):
        resultado_leitura = GerenciadorJson.ler_arquivo(self.usuarios_path)
        if not resultado_leitura.sucesso:
            return resultado_leitura
        usuarios = resultado_leitura.conteudo

        # Verifica se já existe usuário com o mesmo nome
        if any(u['nome'].lower() == nome.lower() for u in usuarios):
            return Resultado.falha('Já existe um usuário com esse nome')

        novo_id = 1 if not usuarios else max(u['id_usuario'] for u in usuarios) + 1
        usuario = {'id_usuario': novo_id, 'nome': nome}
        res = GerenciadorJson.adicionar_item(self.usuarios_path, usuario)

        if not res.sucesso:
            return res

        resultado_factory = ChatFactory.get_factory("UsuarioFactory")
        if not resultado_factory.sucesso:
            return resultado_factory

        resultado_usuario_factory = resultado_factory.conteudo
        if not resultado_usuario_factory:
            return resultado_usuario_factory

        usuario_factory = resultado_usuario_factory.conteudo
        resultado_usuario = usuario_factory.criar(usuario['id_usuario'], usuario['nome'])

        if not resultado_usuario.sucesso:
            return resultado_usuario

        return resultado_usuario.conteudo

    def criar_nova_sala(self, nome: str):
        resultado_leitura = GerenciadorJson.ler_arquivo(self.salas_path)
        if not resultado_leitura.sucesso:
            return resultado_leitura
        salas = resultado_leitura.conteudo

        # Verifica se já existe sala com o mesmo nome
        if any(s['nome'].lower() == nome.lower() for s in salas):
            return Resultado.falha('Já existe uma sala com esse nome')

        novo_id = 1 if not salas else max(s['id_sala'] for s in salas) + 1
        sala = {'id_sala': novo_id, 'nome': nome}
        res = GerenciadorJson.adicionar_item(self.salas_path, sala)

        if not res.sucesso:
            return res

        resultado_factory = ChatFactory.get_factory("SalaFactory")
        if not resultado_factory.sucesso:
            return resultado_factory

        resultado_sala_factory = resultado_factory.conteudo
        if not resultado_sala_factory:
            return resultado_sala_factory

        sala_factory = resultado_sala_factory.conteudo
        resultado_sala = sala_factory.criar(sala['id_sala'], sala['nome'])

        if not resultado_sala.sucesso:
            return resultado_sala

        return resultado_sala.conteudo

    def listar_salas(self):
        resultado_leitura = GerenciadorJson.ler_arquivo(self.salas_path)
        if not resultado_leitura.sucesso:
            return resultado_leitura
        salas = resultado_leitura.conteudo

        resultado_factory = ChatFactory.get_factory("SalaFactory")
        if not resultado_factory.sucesso:
            return resultado_factory
        resultado_sala_factory = resultado_factory.conteudo
        if not resultado_sala_factory:
            return resultado_sala_factory
        sala_factory = resultado_sala_factory.conteudo

        salas_obj = []
        for s in salas:
            resultado_sala = sala_factory.criar(s['id_sala'], s['nome'])
            if not resultado_sala.sucesso:
                return resultado_sala
            salas_obj.append(resultado_sala.conteudo)
        return Resultado.ok(salas_obj)

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

        if not res.sucesso:
            return res

        resultado_factory = ChatFactory.get_factory("MensagemFactory")
        if not resultado_factory.sucesso:
            return resultado_factory

        resultado_mensagem_factory = resultado_factory.conteudo
        if not resultado_mensagem_factory:
            return resultado_mensagem_factory

        mensagem_factory = resultado_mensagem_factory.conteudo
        resultado_mensagem = mensagem_factory.criar(mensagem['id_mensagem'], mensagem['texto'], mensagem['id_usuario'], mensagem['id_sala'])

        if not resultado_mensagem.sucesso:
            return resultado_mensagem

        return resultado_mensagem.conteudo

    def listar_mensagens(self, id_sala: int) -> Resultado:
        mensagens = GerenciadorJson.ler_arquivo(self.mensagens_path).conteudo
        resultado_factory = ChatFactory.get_factory("MensagemFactory")
        
        if not resultado_factory.sucesso:
            return resultado_factory
        resultado_mensagem_factory = resultado_factory.conteudo
        
        if not resultado_mensagem_factory:
            return resultado_mensagem_factory
        mensagem_factory = resultado_mensagem_factory.conteudo

        msgs = []
        for m in mensagens:
            if m['id_sala'] == id_sala:
                resultado_mensagem = mensagem_factory.criar(m['id_mensagem'], m['texto'], m['id_usuario'], m['id_sala'])
                if not resultado_mensagem.sucesso:
                    return resultado_mensagem
                msgs.append(resultado_mensagem.conteudo)
        return Resultado.ok(msgs)

    def apagar_mensagem(self, id_mensagem: int, id_usuario: int):
        resultado_mensagem = GerenciadorJson.remover_item(self.mensagens_path, id_mensagem=id_mensagem, id_usuario=id_usuario)
        if not resultado_mensagem.sucesso:
            return resultado_mensagem
        return resultado_mensagem
    