from domain.entities.mensagem import Mensagem

class MensagemFactory:
    @staticmethod
    def criar_mensagem(texto, id_sala, id_usuario):
        try:
            return Mensagem(texto, id_sala, id_usuario)
        except Exception as e:
            raise("ocorreu um erro que eu não sei: " + e)
