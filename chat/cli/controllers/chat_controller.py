from session import ChatSession


class ChatController:
    def __init__(self, invoker):
        self.invoker = invoker
        self.sessao = ChatSession()

    def _id_usuario_logado(self):
        if not self.sessao.esta_logado():
            raise ValueError("Faca login antes de executar esta acao.")

        return self.sessao.usuario["id_usuario"]

    def _id_sala_atual(self):
        if not self.sessao.esta_em_sala():
            raise ValueError("Entre em uma sala antes de executar esta acao.")

        return self.sessao.sala_atual["id_sala"]

    def _conteudo_ou_erro(self, resposta, mensagem_padrao):
        if not isinstance(resposta, dict):
            raise ValueError(mensagem_padrao)

        mensagem = resposta.get("mensagem") or resposta.get("erro") or mensagem_padrao

        if resposta.get("sucesso") is False:
            raise ValueError(mensagem)

        if resposta.get("conteudo") is not None:
            return resposta["conteudo"]

        raise ValueError(mensagem)

    def help(self):
        return self.invoker.executar("help")

    def login(self, nome):
        usuario = self.invoker.executar("login", nome)
        self.sessao.usuario = self._conteudo_ou_erro(
            usuario,
            "Nao foi possivel fazer login.",
        )
        return usuario

    def criar_usuario(self, nome):
        return self.invoker.executar("criar_usuario", nome)

    def criar_sala(self, nome):
        return self.invoker.executar("criar_sala", nome)

    def listar_salas(self):
        return self.invoker.executar("listar_salas")

    def entrar_sala(self, nome):
        sala = self.invoker.executar("entrar_sala", nome)
        self.sessao.sala_atual = self._conteudo_ou_erro(
            sala,
            "Nao foi possivel entrar na sala.",
        )
        return sala

    def listar_mensagens(self):
        return self.invoker.executar("listar_mensagens", self._id_sala_atual())

    def _id_usuario_da_mensagem(self, mensagem):
        if not isinstance(mensagem, dict):
            return None

        usuario = mensagem.get("usuario")
        if isinstance(usuario, dict):
            return usuario.get("id_usuario")

        return mensagem.get("id_usuario") or mensagem.get("usuario_id")

    def _id_mensagem(self, mensagem):
        if not isinstance(mensagem, dict):
            return None

        return mensagem.get("id_mensagem") or mensagem.get("id")

    def _mensagem_visivel(self, mensagem):
        if not isinstance(mensagem, dict):
            return False

        return mensagem.get("visivel") is not False

    def _ultima_mensagem_do_usuario(self):
        resposta = self.listar_mensagens()
        mensagens = self._conteudo_ou_erro(
            resposta,
            "Nao foi possivel listar as mensagens.",
        )

        if not isinstance(mensagens, list):
            raise ValueError("Resposta inesperada da API.")

        id_usuario = self._id_usuario_logado()
        for mensagem in reversed(mensagens):
            if (
                self._mensagem_visivel(mensagem)
                and self._id_usuario_da_mensagem(mensagem) == id_usuario
            ):
                id_mensagem = self._id_mensagem(mensagem)
                if id_mensagem is None:
                    raise ValueError("Nao foi possivel identificar a ultima mensagem.")

                return id_mensagem

        raise ValueError("Voce ainda nao enviou mensagens nesta sala.")

    def enviar_mensagem(self, texto):
        return self.invoker.executar(
            "enviar_mensagem",
            texto,
            self._id_sala_atual(),
            self._id_usuario_logado(),
        )

    def apagar_mensagem(self):
        id_mensagem = self._ultima_mensagem_do_usuario()
        return self.invoker.executar(
            "apagar_mensagem",
            self._id_sala_atual(),
            id_mensagem,
            self._id_usuario_logado(),
        )
