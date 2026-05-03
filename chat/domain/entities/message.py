from .room import Room
from .user import User
class Message:
    def __init__(self, message_id, text, room, user):
        self._message_id = message_id
        self._text = self._format_message(text, user)
        self._room = room
        self._user = user

    def get_id(self):
        return self._message_id

    def get_text(self) -> str:
        return self._text

    def get_room(self) -> Room:
        return self._room

    def get_user(self) -> User:
        return self._user

    def _format_message(self, text, user) -> str:
        return f"{user.get_name()}:\n{text}"