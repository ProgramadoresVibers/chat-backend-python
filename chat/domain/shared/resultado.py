class Resultado:
    def __init__(self, sucesso, conteudo=None, erro=None):
        self.sucesso = sucesso
        self.conteudo = conteudo
        self.erro = erro

    @staticmethod
    def ok(conteudo):
        return Resultado(sucesso=True, conteudo=conteudo)

    @staticmethod
    def falha(erro):
        return Resultado(sucesso=False, erro=erro)