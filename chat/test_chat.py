from service.chat_facade import ChatFacade
from proxy.chat_proxy import ChatProxy


def teste_fluxo_completo():
    facade = ChatFacade()
    chat = ChatProxy(facade)

    usuario = chat.criar_novo_usuario("Iarley").conteudo
    sala = chat.criar_nova_sala("Geral").conteudo

    chat.enviar_mensagem("Salve!", sala.get_id_sala(), usuario.get_id_usuario())

    mensagens = chat.listar_mensagens(sala.get_id_sala()).conteudo

    print("\n=== TESTE FLUXO COMPLETO ===")
    for msg in mensagens:
        print(msg._formatar_mensagem())


def teste_erro_usuario_invalido():
    facade = ChatFacade()
    chat = ChatProxy(facade)

    sala = chat.criar_nova_sala("Erro").conteudo
    usuario = chat.criar_novo_usuario("Iarley").conteudo

    resultado = chat.enviar_mensagem("Oi", sala.get_id_sala(), 999)

    print("\n=== TESTE ERRO USUÁRIO ===")
    if not resultado.sucesso:
        print("Erro capturado:", resultado.erro)


if __name__ == "__main__":
    teste_fluxo_completo()
    teste_erro_usuario_invalido()