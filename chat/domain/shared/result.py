from typing import Generic, TypeVar, Optional

T = TypeVar("T")
class Resultado(Generic[T]):
    def __init__(self, sucesso: bool, conteudo: Optional[T] = None, erro: str = None):
        self.sucesso = sucesso
        self.conteudo = conteudo
        self.erro = erro

    @staticmethod
    def ok(conteudo: T = None):
        return Resultado(True, conteudo)

    @staticmethod
    def falha(erro: str):
        return Resultado(False, None, erro)