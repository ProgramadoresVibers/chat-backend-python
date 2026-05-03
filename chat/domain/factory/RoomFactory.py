from chat.domain.entities.room import Room
from chat.domain.shared.result import Resultado

class RoomFactory:
    def create(self, room_id, name):
        try:
            return Resultado.ok(Room(room_id, name))
        except Exception as e:
            return Resultado.falha(f"Unexpected error when instantiating room: {str(e)}")
