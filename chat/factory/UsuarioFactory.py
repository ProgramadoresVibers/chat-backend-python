from domain.entities.usuario import Usuario
from domain.shared.resultado import Resultado

class UsuarioFactory:
    def criar(self, id_usuario, nome):
        try:
            return Resultado.ok(Usuario(id_usuario, nome))
        except Exception as e:
            return Resultado.falha(f"Erro inesperado ao tentar instanciar usuário: {str(e)}")