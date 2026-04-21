from domain.entities.mensagem import Mensagem
from domain.shared.resultado import Resultado

class MensagemFactory:
    @staticmethod
    def criar_mensagem(texto, id_sala, id_usuario):
        try:
            mensagem = Mensagem(texto, id_sala, id_usuario)
            return Resultado.ok(mensagem)
        except Exception as e:
            return Resultado.falha(f"ocorreu um erro que eu não sei: {e}")
