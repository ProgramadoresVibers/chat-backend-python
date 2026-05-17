from chat.domain.entities.user import Usuario
from chat.domain.shared.result import Resultado

class UserFactory:
    def create(self, user_id, name):
        try:
            return Resultado.ok(Usuario(user_id, name))
        except Exception as e:
            return Resultado.falha(f"Unexpected error when instantiating user: {str(e)}")
