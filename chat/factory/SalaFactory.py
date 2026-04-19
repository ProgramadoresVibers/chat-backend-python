from domain.entities.sala import Sala

class SalaFactory:
    @staticmethod
    def criar_sala(nome):
        try:
            return Sala(nome)
        except Exception as e:
            raise("ocorreu um erro que eu não sei: " + e)