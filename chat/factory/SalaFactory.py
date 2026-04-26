from domain.entities.sala import Sala
from domain.shared.resultado import Resultado

class SalaFactory:
    def criar(self, id_sala, nome):
        try:
            return Resultado.ok(Sala(id_sala, nome))
        except Exception as e:
            return Resultado.falha(f"Erro inesperado ao tentar instanciar sala: {str(e)}")