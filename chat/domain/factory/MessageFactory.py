from chat.domain.entities.message import Message
from chat.domain.shared.result import Resultado

class MessageFactory:
    def create(self, message_id, text, room, user):
        try:
            return Resultado.ok(Message(message_id, text, room, user))
        except Exception as e:
            return Resultado.falha(f"Unexpected error when instantiating message: {str(e)}")
