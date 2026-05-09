from flask import Flask, request
from chat.domain.services.chat_facade import ChatFacade
from chat.domain.proxies.chat_proxy import ChatProxy

app = Flask(__name__)

chat = ChatProxy(ChatFacade())

@app.route("/login", methods=['POST'])
def login():
    dados_usuario = request.json

    resultado = chat.acessar_usuario(dados_usuario.get("nome"))

    if not resultado.sucesso:
        return {"sucesso": False, "erro": resultado.erro}

    usuario = resultado.conteudo

    return {
        "sucesso": True,
        "conteudo":
            {
                "id_usuario": usuario.get_id_usuario(),
                "nome": usuario.get_nome()
            }
    }

@app.route("/entrar_sala", methods=['POST'])
def entrar_na_sala():
    dados_sala = request.json

    resultado = chat.acessar_sala(dados_sala.get("nome"))

    if not resultado.sucesso:
        return {"sucesso": False, "erro": resultado.erro}

    sala = resultado.conteudo

    return {
        "sucesso": True,
        "conteudo":
            {
                "id_sala": sala.get_id_sala(),
                "nome": sala.get_nome()
            }
    }

@app.route("/criar_usuario", methods=["POST"])
def criar_usuario():
    dados_usuario = request.json

    resultado = chat.criar_novo_usuario(dados_usuario.get("nome"))

    if not resultado.sucesso:
        return {"sucesso": False, "erro": resultado.erro}

    usuario = resultado.conteudo

    return {
        "sucesso": True,
        "conteudo":
            {
                "id_usuario": usuario.get_id_usuario(),
                "nome": usuario.get_nome()
            }
    }

@app.route("/criar_sala", methods=["POST"])
def criar_sala():
    dados_sala = request.json

    resultado = chat.criar_nova_sala(dados_sala.get("nome"))

    if not resultado.sucesso:
        return {"sucesso": False, "erro": resultado.erro}

    sala = resultado.conteudo

    return {
        "sucesso": True,
        "conteudo":
            {
                "id_sala": sala.get_id_sala(),
                "nome": sala.get_nome()
            }
    }

@app.route("/salas", methods=["GET"])
def listar_salas():
    resultado = chat.listar_salas()

    if not resultado.sucesso:
        return {"sucesso": False, "erro": resultado.erro}

    salas = resultado.conteudo

    return {
        "sucesso": True,
        "conteudo": salas
    }

@app.route("/enviar_mensagem", methods=["POST"])
def enviar_mensagem():
    dados_mensagem = request.json

    resultado = chat.enviar_mensagem(dados_mensagem.get("texto"),
                                    dados_mensagem.get("id_sala"),
                                    dados_mensagem.get("id_usuario"))

    if not resultado.sucesso:
        return {"sucesso": False, "erro": resultado.erro}

    mensagem = resultado.conteudo

    return {
        "sucesso": True,
        "conteudo":
            {
                "id_mensagem": mensagem.get_id_mensagem(),
                "texto": mensagem.get_texto(),
                "id_sala": mensagem.get_sala().get_id_sala(),
                "id_usuario": mensagem.get_usuario().get_id_usuario(),
                "visivel": mensagem.get_visivel()
            }
    }

@app.route("/salas/<int:id_sala>/mensagens", methods=["GET"])
def listar_mensagens(id_sala):
    resultado = chat.listar_mensagens(id_sala)

    if not resultado.sucesso:
        return {"sucesso": False, "erro": resultado.erro}

    mensagens = resultado.conteudo

    return {
        "sucesso": True,
        "conteudo": mensagens
    }

@app.route("/salas/<int:id_sala>/mensagens/<int:id_mensagem>/usuarios/<int:id_usuario>", methods=["DELETE"])
def apagar_mensagem(id_sala, id_mensagem, id_usuario):
    resultado = chat.apagar_mensagem(id_mensagem, id_sala, id_usuario)

    if not resultado.sucesso:
        return {"sucesso": False, "erro": resultado.erro}

    return {
        "sucesso": True,
        "conteudo": None
    }