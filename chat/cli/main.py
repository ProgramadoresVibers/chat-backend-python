import json

from chat.cli.commands.command_invoker import CommandInvoker
from chat.cli.controllers.chat_controller import ChatController
from chat.cli.factory.command_factory import CommandFactory
from chat.cli.services.local_chat_service import LocalChatService


def validar_argumento(argumento, uso):
    if not argumento:
        raise ValueError(f"Uso: {uso}")

    return argumento


def obter_conteudo(resposta):
    if isinstance(resposta, str):
        try:
            resposta = json.loads(resposta)
        except json.JSONDecodeError:
            raise ValueError("Resposta inesperada da API.")

    if not isinstance(resposta, dict):
        raise ValueError("Resposta inesperada da API.")

    if resposta.get("sucesso") is False:
        mensagem = resposta.get("mensagem") or resposta.get("erro")
        raise ValueError(mensagem or "Nao foi possivel executar o comando.")

    if "conteudo" not in resposta:
        raise ValueError("Resposta inesperada da API.")

    conteudo = resposta["conteudo"]
    if isinstance(conteudo, str):
        try:
            return json.loads(conteudo)
        except json.JSONDecodeError:
            return conteudo

    return conteudo


def obter_nome(conteudo, mensagem_erro):
    if isinstance(conteudo, dict) and conteudo.get("nome"):
        return conteudo["nome"]

    raise ValueError(mensagem_erro)


def formatar_login(resposta):
    nome = obter_nome(obter_conteudo(resposta), "Nao foi possivel identificar o usuario.")
    return f"Logado como: {nome}"


def formatar_usuario_criado(resposta):
    nome = obter_nome(obter_conteudo(resposta), "Usuario criado.")
    return f"Usuario criado: {nome}"


def formatar_sala_criada(resposta):
    nome = obter_nome(obter_conteudo(resposta), "Sala criada.")
    return f"Sala criada: {nome}"


def formatar_entrada_sala(resposta):
    nome = obter_nome(obter_conteudo(resposta), "Entrou na sala.")
    return f"Entrou na sala: {nome}"


def formatar_lista_salas(resposta):
    conteudo = obter_conteudo(resposta)

    if not conteudo:
        return "Nenhuma sala encontrada."

    if not isinstance(conteudo, list):
        raise ValueError("Resposta inesperada da API.")

    nomes = []
    for sala in conteudo:
        if isinstance(sala, dict) and sala.get("nome"):
            nomes.append(sala["nome"])
        elif isinstance(sala, str) and sala.strip():
            nomes.append(sala.strip())

    if not nomes:
        return "Nenhuma sala encontrada."

    return "\n".join(nomes)


def obter_nome_autor(mensagem):
    usuario = mensagem.get("usuario")
    if isinstance(usuario, dict) and usuario.get("nome"):
        return usuario["nome"]

    return mensagem.get("nome_usuario") or mensagem.get("usuario_nome") or mensagem.get("nome")


def formatar_mensagem(mensagem):
    if isinstance(mensagem, str):
        return mensagem

    if not isinstance(mensagem, dict):
        return None

    if mensagem.get("visivel") is False:
        return "mensagem apagada"

    texto = mensagem.get("texto") or mensagem.get("mensagem")
    if not texto:
        return None

    autor = obter_nome_autor(mensagem)
    if autor:
        return f"{autor}: {texto}"

    return texto


def formatar_lista_mensagens(resposta):
    conteudo = obter_conteudo(resposta)

    if not conteudo:
        return "Nenhuma mensagem encontrada."

    if not isinstance(conteudo, list):
        mensagem = formatar_mensagem(conteudo)
        if mensagem:
            return mensagem
        raise ValueError("Resposta inesperada da API.")

    mensagens = []
    for item in conteudo:
        mensagem = formatar_mensagem(item)
        if mensagem:
            mensagens.append(mensagem)

    if not mensagens:
        return "Nenhuma mensagem encontrada."

    return "\n".join(mensagens)


def formatar_mensagem_enviada(resposta):
    conteudo = obter_conteudo(resposta)
    mensagem = formatar_mensagem(conteudo)

    if mensagem:
        return mensagem

    return "Mensagem enviada."


def criar_controller(servico=None):
    servico = servico or LocalChatService()
    comandos = CommandFactory.criar_comandos(servico)

    invoker = CommandInvoker()
    for nome, comando in comandos.items():
        invoker.registrar(nome, comando)

    return ChatController(invoker)


def rodar_cli(controller):
    while True:
        entrada = input("> ").strip()

        if not entrada:
            continue

        comando, _, argumento = entrada.partition(" ")
        argumento = argumento.strip()

        try:
            if comando == "/help":
                if argumento:
                    raise ValueError("Uso: /help")

                print(controller.help())

            elif comando == "/login":
                nome = validar_argumento(argumento, "/login <nome>")
                print(formatar_login(controller.login(nome)))

            elif comando == "/criar_usuario":
                nome = validar_argumento(argumento, "/criar_usuario <nome>")
                print(formatar_usuario_criado(controller.criar_usuario(nome)))

            elif comando == "/criar_sala":
                nome_sala = validar_argumento(argumento, "/criar_sala <nome>")
                print(formatar_sala_criada(controller.criar_sala(nome_sala)))

            elif comando == "/listar_salas":
                print(formatar_lista_salas(controller.listar_salas()))

            elif comando == "/entrar_sala":
                nome_sala = validar_argumento(argumento, "/entrar_sala <nome>")
                print(formatar_entrada_sala(controller.entrar_sala(nome_sala)))

            elif comando == "/listar_mensagens":
                print(formatar_lista_mensagens(controller.listar_mensagens()))

            elif comando == "/enviar":
                texto = validar_argumento(argumento, "/enviar <texto>")
                print(formatar_mensagem_enviada(controller.enviar_mensagem(texto)))

            elif comando == "/apagar":
                if argumento:
                    raise ValueError("Uso: /apagar")

                controller.apagar_mensagem()
                print("Mensagem apagada.")

            elif comando == "/sair":
                print("Saindo...")
                break

            else:
                print("Comando invalido")
        except ValueError as erro:
            print(erro)
        except KeyError:
            print("Resposta inesperada da API.")


def main():
    controller = criar_controller()
    rodar_cli(controller)

if __name__ == "__main__":
    main()