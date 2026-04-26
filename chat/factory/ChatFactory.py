from .SalaFactory import SalaFactory
from .UsuarioFactory import UsuarioFactory
from .MensagemFactory import MensagemFactory
from domain.shared.resultado import Resultado

class ChatFactory:
    @staticmethod
    def get_factory(tipo):  #tipo = string que representa o tipo de factory que eu quero criar
        if tipo == "SalaFactory":
            return Resultado.ok(SalaFactory())
        elif tipo == "UsuarioFactory":
            return Resultado.ok(UsuarioFactory())
        elif tipo == "MensagemFactory":
            return Resultado.ok(MensagemFactory())
        else:
            return Resultado.falha("Tipo de factory desconhecido")