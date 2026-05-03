class Room:
    def __init__(self, room_id, name):
        self._room_id = room_id
        self._name = name

    def get_id(self):
        return self._room_id

    def get_name(self):
        return self._name