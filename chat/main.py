from service.chat_facade import ChatFacade

facade = ChatFacade()

# Cria usuário e sala
res_usuario = facade.criar_novo_usuario("Maria")
if not res_usuario.sucesso:
    print("Erro ao criar usuário:", res_usuario.erro)
    exit(1)
usuario = res_usuario.conteudo

res_sala = facade.criar_nova_sala("Geral")
if not res_sala.sucesso:
    print("Erro ao criar sala:", res_sala.erro)
    exit(1)
sala = res_sala.conteudo

# Envia mensagem
res_msg = facade.enviar_mensagem("Olá, mundo!", sala.get_id_sala(), usuario.get_id_usuario())
print("Mensagem enviada:", res_msg.sucesso)

# Lista mensagens
res_list = facade.listar_mensagens(sala.get_id_sala())
for msg in res_list.conteudo:
    print(msg._formatar_mensagem())