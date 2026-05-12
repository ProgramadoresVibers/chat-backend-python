from chat.cli.main import criar_controller
from chat.cli.services.local_chat_service import LocalChatService
from chat.domain.proxies.chat_proxy import ChatProxy
from chat.domain.services.chat_facade import ChatFacade


def criar_servico_temporario(tmp_path):
    facade = ChatFacade()
    proxy = ChatProxy(facade)

    facade.usuarios_path = tmp_path / "usuarios.json"
    facade.salas_path = tmp_path / "salas.json"
    facade.mensagens_path = tmp_path / "mensagens.json"
    proxy.salas_path = facade.salas_path
    proxy.mensagens_path = facade.mensagens_path

    return LocalChatService(proxy)


def test_servico_local_cria_e_acessa_usuario_e_sala(tmp_path):
    servico = criar_servico_temporario(tmp_path)

    usuario = servico.criar_usuario("Alice")
    sala = servico.criar_sala("Geral")

    assert usuario == {
        "sucesso": True,
        "conteudo": {"id_usuario": 1, "nome": "Alice"},
    }
    assert servico.acessar_usuario("Alice") == usuario
    assert sala == {
        "sucesso": True,
        "conteudo": {"id_sala": 1, "nome": "Geral"},
    }
    assert servico.entrar_sala("Geral") == sala


def test_servico_local_envia_lista_e_apaga_mensagem(tmp_path):
    servico = criar_servico_temporario(tmp_path)
    servico.criar_usuario("Alice")
    servico.criar_sala("Geral")

    envio = servico.enviar_mensagem("Ola", 1, 1)
    assert envio["sucesso"] is True
    assert envio["conteudo"] == {
        "id_mensagem": 1,
        "texto": "Alice:\nOla",
        "id_sala": 1,
        "id_usuario": 1,
        "visivel": True,
    }

    mensagens = servico.listar_mensagens(1)
    assert mensagens == {
        "sucesso": True,
        "conteudo": [
            {
                "id_mensagem": 1,
                "texto": "Alice:\nOla",
                "id_usuario": 1,
                "id_sala": 1,
                "visivel": True,
            }
        ],
    }

    apagada = servico.apagar_mensagem(1, 1, 1)
    assert apagada["sucesso"] is True
    assert apagada["conteudo"]["visivel"] is False


def test_servico_local_retorna_erro_do_proxy(tmp_path):
    servico = criar_servico_temporario(tmp_path)

    resposta = servico.criar_usuario("Al")

    assert resposta["sucesso"] is False
    assert "pelo menos 3 caracteres" in resposta["erro"]


def test_controller_cli_executa_fluxo_com_servico_local(tmp_path):
    servico = criar_servico_temporario(tmp_path)
    controller = criar_controller(servico)

    assert controller.criar_usuario("Alice")["sucesso"] is True
    assert controller.criar_sala("Geral")["sucesso"] is True
    assert controller.login("Alice")["conteudo"]["id_usuario"] == 1
    assert controller.entrar_sala("Geral")["conteudo"]["id_sala"] == 1

    envio = controller.enviar_mensagem("Ola")
    assert envio["conteudo"]["id_mensagem"] == 1

    mensagens = controller.listar_mensagens()
    assert mensagens["conteudo"][0]["texto"] == "Alice:\nOla"

    apagada = controller.apagar_mensagem()
    assert apagada["conteudo"]["visivel"] is False


def test_controller_help_lista_comandos(tmp_path):
    servico = criar_servico_temporario(tmp_path)
    controller = criar_controller(servico)

    ajuda = controller.help()

    assert "/help" in ajuda
    assert "/login <nome>" in ajuda
    assert "/enviar <texto>" in ajuda
    assert "/sair" in ajuda
