from chat.domain.interfaces.repositories.chat_operations import ChatOperacoesInterface
from chat.domain.entities.user import Usuario
from chat.domain.entities.room import Sala
from chat.domain.shared.result import Resultado
from chat.infraestructure.persistence.json_manager import GerenciadorJson
from chat.domain.factory.ChatFactory import ChatFactory
from pathlib import Path


class ChatFacade(ChatOperacoesInterface):
    def __init__(self):
        # .parent sobe um nível por vez
        raiz_projeto = Path(__file__).resolve().parent.parent.parent

        data_dir = raiz_projeto / 'infraestructure' / 'data'

        # Cria a pasta (parents=True: cria as pastas intermediárias se não existirem)
        data_dir.mkdir(parents=True, exist_ok=True)

        self.usuarios_path = data_dir / 'usuarios.json'
        self.salas_path = data_dir / 'salas.json'
        self.mensagens_path = data_dir / 'mensagens.json'

    def _obter_objeto(self, tipo_factory: str, *args):
        resultado_factory = ChatFactory.get_factory(tipo_factory)
        if not resultado_factory.sucesso:
            return resultado_factory

        factory = resultado_factory.conteudo

        return factory.create(*args)

    def _obter_usuario(self, id_usuario: int, nome: str):
        return self._obter_objeto("UserFactory", id_usuario, nome)

    def _obter_sala(self, id_sala: int, nome: str):
        return self._obter_objeto("RoomFactory", id_sala, nome)

    def _obter_mensagem(self, id_mensagem: int, texto: str, sala: Sala, usuario: Usuario):
        return self._obter_objeto("MessageFactory", id_mensagem, texto, sala, usuario)

    def acessar_usuario(self, nome: str):
        resultado_leitura = GerenciadorJson.ler_arquivo(self.usuarios_path, nome=nome)

        if not resultado_leitura.sucesso:
            return resultado_leitura

        if not resultado_leitura.conteudo:
            return Resultado.falha('Não existe usuário com esse nome')

        usuario = resultado_leitura.conteudo[0]

        return self._obter_usuario(usuario['id_usuario'], usuario['nome'])

    def acessar_sala(self, nome: str):
        resultado_leitura = GerenciadorJson.ler_arquivo(self.salas_path, nome=nome)

        if not resultado_leitura.sucesso:
            return resultado_leitura

        if not resultado_leitura.conteudo:
            return Resultado.falha('Não existe sala com esse nome')

        sala = resultado_leitura.conteudo[0]

        return self._obter_sala(sala['id_sala'], sala['nome'])

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

        return self._obter_usuario(usuario['id_usuario'], usuario['nome'])

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

        return self._obter_sala(sala['id_sala'], sala['nome'])

    def listar_salas(self):
        return GerenciadorJson.ler_arquivo(self.salas_path)

    def enviar_mensagem(self, texto: str, id_sala: int, id_usuario: int):
        resultado_leitura_sala = GerenciadorJson.ler_arquivo(self.salas_path, id_sala=id_sala)
        if not resultado_leitura_sala.sucesso:
            return resultado_leitura_sala

        if not resultado_leitura_sala.conteudo:
            return Resultado.falha('Sala não existe')

        sala_dicionario = resultado_leitura_sala.conteudo[0]

        resultado_sala = self._obter_sala(sala_dicionario['id_sala'], sala_dicionario['nome'])
        if not resultado_sala.sucesso:
            return resultado_sala

        sala_objeto = resultado_sala.conteudo

        resultado_leitura_usuario = GerenciadorJson.ler_arquivo(self.usuarios_path, id_usuario=id_usuario)
        if not resultado_leitura_usuario.sucesso:
            return resultado_leitura_usuario

        if not resultado_leitura_usuario.conteudo:
            return Resultado.falha('Usuário não existe')

        usuario_dicionario = resultado_leitura_usuario.conteudo[0]

        resultado_usuario = self._obter_usuario(usuario_dicionario['id_usuario'], usuario_dicionario['nome'])
        if not resultado_usuario.sucesso:
            return resultado_usuario

        usuario_objeto = resultado_usuario.conteudo

        resultado_leitura_mensagem = GerenciadorJson.ler_arquivo(self.mensagens_path)
        if not resultado_leitura_mensagem.sucesso:
            return resultado_leitura_mensagem

        mensagens = resultado_leitura_mensagem.conteudo

        novo_id = 1 if not mensagens else max(m['id_mensagem'] for m in mensagens) + 1

        resultado_mensagem = self._obter_mensagem(novo_id, texto, sala_objeto, usuario_objeto)
        if not resultado_mensagem.sucesso:
            return resultado_mensagem

        mensagem_objeto = resultado_mensagem.conteudo

        res = GerenciadorJson.adicionar_item(self.mensagens_path, {
            'id_mensagem': novo_id, 'texto': mensagem_objeto.get_texto(),
            'id_usuario': id_usuario, 'id_sala': id_sala, 'visivel': mensagem_objeto.get_visivel()
        })

        if not res.sucesso:
            return res

        return Resultado.ok(mensagem_objeto)

    def listar_mensagens(self, id_sala: int) -> Resultado:
        return GerenciadorJson.ler_arquivo(self.mensagens_path, id_sala=id_sala)

    def apagar_mensagem(self, id_mensagem: int, id_sala: int, id_usuario: int):
        return GerenciadorJson.atualizar_item(self.mensagens_path,
                                              {"id_mensagem": id_mensagem,
                                               "id_sala": id_sala,
                                               "id_usuario": id_usuario},
                                              {"visivel": False})