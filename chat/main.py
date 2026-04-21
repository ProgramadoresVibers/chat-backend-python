from service.chat_facade import ChatFacade
from proxy.chat_proxy import ChatProxy

facade = ChatFacade()
chat = ChatProxy(facade)

usuario = chat.criar_novo_usuario("Iarley").conteudo
sala = chat.criar_nova_sala("Geral").conteudo

chat.enviar_mensagem("Salve!", sala.get_id_sala(), usuario.get_id_usuario())

for msg in chat.listar_mensagens():
    print(msg._formatar_mensagem())