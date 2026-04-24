from service.chat_facade import ChatFacade
from infraestructure.gerenciador_json import GerenciadorJson

facade = ChatFacade()
usuarios = GerenciadorJson.ler_arquivo(facade.usuarios_path).conteudo
print(f"Antes de apagar mensagem {usuarios}")
usuario_existente = next((u for u in usuarios if u['nome'] == "Apagador"), None)
print(f"Usuário existente: {usuario_existente}")
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
    print(f"Usuário encontrado: {usuario.get_nome()}")
else:
    res_usuario = facade.criar_novo_usuario("Apagador")
    if not res_usuario.sucesso:
        print("Erro ao criar usuário:", res_usuario.erro)
        exit(1)
    usuario = res_usuario.conteudo

# Busca sala pelo nome, se não existir, cria
salas = GerenciadorJson.ler_arquivo(facade.salas_path).conteudo
print(f"Salas existentes: {salas}")
sala_existente = next((s for s in salas if s['nome'] == "SalaApagar"), None)
print(f"Sala existente: {sala_existente}")
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

# Envia mensagem
# res_msg = facade.enviar_mensagem("Mensagem para apagar", sala.get_id_sala(), usuario.get_id_usuario())
# print(f"Mensagem enviada: {res_msg.sucesso}")
# if not res_msg.sucesso:
#     print("Erro ao enviar mensagem:", res_msg.erro)
#     exit(1)
# msg = res_msg.conteudo
# print("Mensagem enviada com id:", msg.get_id_mensagem())

# Tenta apagar a mensagem com o próprio usuário (deve funcionar)
res_apagar = facade.apagar_mensagem(5, usuario.get_id_usuario())
print("Apagar própria mensagem:", res_apagar.sucesso, res_apagar.erro)
print(f"Mensagem apagada com sucesso: {res_apagar.sucesso}")
print("Mensagens depois de apagar:", GerenciadorJson.ler_arquivo(facade.mensagens_path).conteudo)

# # Cria outro usuário
# res_outro_usuario = facade.criar_novo_usuario("Intruso")
# if not res_outro_usuario.sucesso:
#     print("Erro ao criar usuário intruso:", res_outro_usuario.erro)
#     exit(1)
# outro_usuario = res_outro_usuario.conteudo

# Envia nova mensagem com o usuário original
# res_msg2 = facade.enviar_mensagem("Mensagem protegida", sala.get_id_sala(), usuario.get_id_usuario())
# msg2 = res_msg2.conteudo

# Tenta apagar a mensagem com outro usuário (não deve funcionar)
# res_apagar2 = facade.apagar_mensagem(msg2.get_id_mensagem(), outro_usuario.get_id_usuario())
# print("Apagar mensagem de outro usuário:", res_apagar2.sucesso, res_apagar2.erro)
