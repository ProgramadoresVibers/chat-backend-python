import SalaFactory
import UsuarioFactory
import MensagemFactory

class ChatFactory:
    @staticmethod
    def get_factory(tipo): '''o que ser esse tipo?????????????????'''
        try:
            if (tipo == "SalaFactory"):
                return SalaFactory()
            elif (tipo == "UsuarioFactory"):
                return UsuarioFactory()
            elif (tipo == "MensagemFactory"):
                return MensagemFactory()
        except Exception as e:
            raise("ocorreu um erro que eu não sei: " + e)