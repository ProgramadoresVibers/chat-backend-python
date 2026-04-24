from service.chat_facade import ChatFacade
from infraestructure.gerenciador_json import GerenciadorJson

facade = ChatFacade()

# Busca usuário pelo nome, se não existir, cria
usuarios = GerenciadorJson.ler_arquivo(facade.usuarios_path).conteudo
usuario_existente = next((u for u in usuarios if u['nome'] == "Apagador"), None)
if usuario_existente:
    class DummyUsuario:
        def __init__(self, id_usuario, nome):
            self._id_usuario = id_usuario
            self._nome = nome
        def get_id_usuario(self):
            return self._id_usuario
        def get_nome(self):
            return self._nome
    usuario = DummyUsuario(usuario_existente['id_usuario'], usuario_existente['nome'])
else:
    res_usuario = facade.criar_novo_usuario("Apagador")
    if not res_usuario.sucesso:
        print("Erro ao criar usuário:", res_usuario.erro)
        exit(1)
    usuario = res_usuario.conteudo

# Busca sala pelo nome, se não existir, cria
salas = GerenciadorJson.ler_arquivo(facade.salas_path).conteudo
sala_existente = next((s for s in salas if s['nome'] == "SalaApagar"), None)
if sala_existente:
    class DummySala:
        def __init__(self, id_sala, nome):
            self._id_sala = id_sala
            self._nome = nome
        def get_id_sala(self):
            return self._id_sala
        def get_nome(self):
            return self._nome
    sala = DummySala(sala_existente['id_sala'], sala_existente['nome'])
else:
    res_sala = facade.criar_nova_sala("SalaApagar")
    if not res_sala.sucesso:
        print("Erro ao criar sala:", res_sala.erro)
        exit(1)
    sala = res_sala.conteudo
