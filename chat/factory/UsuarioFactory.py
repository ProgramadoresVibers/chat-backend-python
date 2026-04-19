from domain.entities.usuario import Usuario

class UsuarioFactory:
    @staticmethod
    def criar_usuario(nome):
        try:
            return Usuario(nome):
        except Exception as e:
            raise("ocorreu um erro que eu não sei: " + e)