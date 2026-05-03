from .RoomFactory import RoomFactory
from .UserFactory import UserFactory
from .MessageFactory import MessageFactory
from chat.domain.shared.result import Resultado

class ChatFactory:
    @staticmethod
    def get_factory(factory_type):
        if factory_type == "RoomFactory":
            return Resultado.ok(RoomFactory())
        elif factory_type == "UserFactory":
            return Resultado.ok(UserFactory())
        elif factory_type == "MessageFactory":
            return Resultado.ok(MessageFactory())
        else:
            return Resultado.falha("Tipo de factory desconhecido")