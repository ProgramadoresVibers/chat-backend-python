class User:
    def __init__(self, user_id, name):
        self._user_id = user_id
        self._name = name

    def get_id(self):
        return self._user_id

    def get_name(self):
        return self._name