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
        
    
    def _obter_objeto(self, tipo_factory: str, *args):
        resultado_factory = ChatFactory.get_factory(tipo_factory)
        if not resultado_factory.sucesso:
            return resultado_factory

        factory = resultado_factory.conteudo
        resultado = factory.criar(args)

        if not resultado.sucesso:
            return resultado

        return resultado

    def _obter_usuario(self, id_usuario: int, nome: str):
        return self._obter_objeto("UsuarioFactory", id_usuario, nome)

    def _obter_sala(self, id_sala: int, nome: str):
        return self._obter_objeto("SalaFactory", id_sala, nome)

    def _obter_mensagem(self, id_mensagem: int, texto: str, sala: Sala, usuario: Usuario):
        return self._obter_objeto("MensagemFactory", id_mensagem, texto, sala, usuario)

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

        resultado_usuario_objeto = ChatFacade._obter_usuario(usuario['id_usuario'], usuario['nome'])
        if not resultado_usuario_objeto.sucesso:
            return resultado_usuario_objeto
        
        return resultado_usuario_objeto

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

        resultado_sala_objeto = ChatFacade._obter_sala(sala['id_sala'], sala['nome'])
        if not resultado_sala_objeto.sucesso:
            return resultado_sala_objeto

        return resultado_sala_objeto






    def listar_salas(self):
        resultado_leitura = GerenciadorJson.ler_arquivo(self.salas_path)
        if not resultado_leitura.sucesso:
            return resultado_leitura
        salas = resultado_leitura.conteudo
        
        salas_obj = []
        for s in salas:
            resultado_sala = ChatFacade._obter_sala(s['id_sala'], s['nome'])
            if not resultado_sala.sucesso:
                return resultado_sala
            salas_obj.append(resultado_sala.conteudo)
        return Resultado.ok(salas_obj)





    def enviar_mensagem(self, texto: str, id_sala: int, id_usuario: int):
        resultado_leitura_sala = GerenciadorJson.ler_arquivo(self.salas_path)
        if not resultado_leitura_sala.sucesso:
            return resultado_leitura_sala

        if not resultado_leitura_sala.conteudo:
            return Resultado.falha('Sala não existe')
        
        sala = resultado_leitura_sala.conteudo[0]
        
        resultado_leitura_usuario = GerenciadorJson.ler_arquivo(self.usuarios_path)
        if not resultado_leitura_usuario.sucesso:
            return resultado_leitura_usuario

        if not resultado_leitura_usuario.conteudo:
            return Resultado.falha('Usuário não existe')
        usuario = resultado_leitura_usuario.conteudo[0]



        resultado_usuario = ChatFacade._obter_usuario(id_usuario, None)
        if not resultado_usuario.sucesso:
            return resultado_usuario

        resultado_sala = ChatFacade._obter_sala(id_sala, None)
        if not resultado_sala.sucesso:
            return resultado_sala

        mensagens = GerenciadorJson.ler_arquivo(self.mensagens_path).conteudo
        novo_id = 1 if not mensagens else max(m['id_mensagem'] for m in mensagens) + 1
        mensagem = {'id_mensagem': novo_id, 'texto': texto, 'id_usuario': id_usuario, 'id_sala': id_sala}
        res = GerenciadorJson.adicionar_item(self.mensagens_path, mensagem)

        if not res.sucesso:
            return res

        mensagem_objeto = ChatFacade._obter_mensagem(mensagem['id_mensagem'])
        if not mensagem_objeto.sucesso:
            return mensagem_objeto
        
        return Resultado.ok(mensagem_objeto)

    def listar_mensagens(self, id_sala: int) -> Resultado:
        resultado_leitura = GerenciadorJson.ler_arquivo(self.mensagens_path)
        if not resultado_leitura.sucesso:
            return resultado_leitura
        mensagens = resultado_leitura.conteudo

        mensagem_objetos = []
        for m in mensagens:
            mensagem_objeto = ChatFacade._obter_mensagem(m['id_mensagem'], m['texto'], m['id_sala'], m['id_usuario'])
            if not mensagem_objeto.sucesso:
                return mensagem_objeto
            mensagem_objetos.append(mensagem_objeto.conteudo)

        return Resultado.ok(mensagem_objetos)

    def apagar_mensagem(self, id_mensagem: int, id_usuario: int):
        resultado_mensagem = GerenciadorJson.remover_item(self.mensagens_path, id_mensagem=id_mensagem, id_usuario=id_usuario)
        if not resultado_mensagem.sucesso:
            return resultado_mensagem
        return resultado_mensagem
    