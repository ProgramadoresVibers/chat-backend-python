from service.chat_facade import ChatFacade
from proxy.chat_proxy import ChatProxy



def teste_basico():
    facade = ChatFacade()
    chat = ChatProxy(facade)

    usuario = chat.criar_novo_usuario("Iarley").conteudo
    sala = chat.criar_nova_sala("Geral").conteudo

    chat.enviar_mensagem("Salve!", sala.get_id_sala(), usuario.get_id_usuario())

    mensagens = chat.listar_mensagens()

    print("\n=== TESTE BÁSICO ===")
    for msg in mensagens:
        print(msg._formatar_mensagem())


def teste_multiplos_usuarios():
    facade = ChatFacade()
    chat = ChatProxy(facade)

    u1 = chat.criar_novo_usuario("Iarley").conteudo
    u2 = chat.criar_novo_usuario("João").conteudo

    sala = chat.criar_nova_sala("Dev").conteudo

    chat.enviar_mensagem("Fala devs!", sala.get_id_sala(), u1.get_id_usuario())
    chat.enviar_mensagem("Salve!", sala.get_id_sala(), u2.get_id_usuario())

    print("\n=== TESTE MÚLTIPLOS USUÁRIOS ===")
    for msg in chat.listar_mensagens():
        print(msg._formatar_mensagem())


def teste_erro_mensagem_vazia():
    facade = ChatFacade()
    chat = ChatProxy(facade)

    u = chat.criar_novo_usuario("Teste").conteudo
    sala = chat.criar_nova_sala("Erro").conteudo

    print("\n=== TESTE ERRO ===")
    try:
        chat.enviar_mensagem("   ", sala.get_id_sala(), u.get_id_usuario())
    except Exception as e:
        print("Erro capturado:", e)


if __name__ == "__main__":
    teste_basico()
    teste_multiplos_usuarios()
    teste_erro_mensagem_vazia()