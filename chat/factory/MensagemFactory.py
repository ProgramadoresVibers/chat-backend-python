from domain.entities.mensagem import Mensagem
from domain.shared.resultado import Resultado

class MensagemFactory:
    def criar(self, id_mensagem, texto, sala, usuario):
        try:
            mensagem = Mensagem(id_mensagem, texto, sala, usuario)
            return Resultado.ok(mensagem)
        except Exception as e:
            return Resultado.falha(f"Erro inesperado ao tentar instanciar mensagem: {str(e)}")
