class CommandInvoker:
    def __init__(self):
        self.comandos = {}

    def registrar(self, nome: str, comando):
        self.comandos[nome] = comando

    def executar(self, nome: str, *args, **kwargs):
        if nome not in self.comandos:
            raise ValueError("Comando nao encontrado.")

        comando = self.comandos[nome]
        comando.validar(*args, **kwargs)
        return comando.executar(*args, **kwargs)
