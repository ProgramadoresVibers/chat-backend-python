from service.chat_facade import ChatFacade
from domain.shared.resultado import Resultado

facade = ChatFacade()

res_outro_usuario = facade.criar_novo_usuario("Carlos")
if not res_outro_usuario.sucesso:
    Resultado.falha("Erro ao criar usuário:", res_outro_usuario.erro)
    exit(1)
Resultado.ok("Usuário criado com sucesso:", res_outro_usuario.conteudo)
