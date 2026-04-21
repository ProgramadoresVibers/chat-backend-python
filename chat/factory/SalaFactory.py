from domain.entities.sala import Sala
from domain.shared.resultado import Resultado

class SalaFactory:
    @staticmethod
    def criar_sala(nome):
        try:
            return Sala(nome)
        except Exception as e:
            return Resultado.falha(f"ocorreu um erro que eu não sei: {e}")