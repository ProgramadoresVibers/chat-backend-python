from chat.domain.entities.room import Sala
from chat.domain.shared.result import Resultado

class RoomFactory:
    def create(self, room_id, name):
        try:
            return Resultado.ok(Sala(room_id, name))
        except Exception as e:
            return Resultado.falha(f"Unexpected error when instantiating room: {str(e)}")
