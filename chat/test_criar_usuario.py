from service.chat_facade import ChatFacade
from infraestructure.gerenciador_json import GerenciadorJson

facade = ChatFacade()

res_outro_usuario = facade.criar_novo_usuario("Carlos")
json = GerenciadorJson.ler_arquivo("chat/data/usuarios.json")

print(json.conteudo)