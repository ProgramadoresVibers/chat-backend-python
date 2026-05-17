import sys
import os

PASTA_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PASTA_RAIZ not in sys.path:
    sys.path.insert(0, PASTA_RAIZ)

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QLabel
from tela_login import Ui_MainWindow as Ui_Login
from tela_chat import Ui_MainWindow as Ui_Chat

from chat.cli.main import (
    criar_controller,
    formatar_lista_salas,
    formatar_lista_mensagens,
)


TEMA = """
QMainWindow {
    background-color: #111b21;
}

QWidget {
    background-color: #111b21;
    color: #e9edef;
}

QLabel {
    color: #e9edef;
    font-size: 13px;
    font-weight: bold;
}

QLineEdit {
    background-color: #202c33;
    color: #e9edef;
    border: 1px solid #2a3942;
    border-radius: 10px;
    padding: 9px;
}

QLineEdit:focus {
    border: 2px solid #00a884;
}

QPushButton {
    background-color: #00a884;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 9px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #06cf9c;
}

QPushButton:pressed {
    background-color: #008069;
}

QTextEdit {
    background-color: #0b141a;
    color: #e9edef;
    border: 1px solid #2a3942;
    border-radius: 10px;
    padding: 10px;
}

QListWidget {
    background-color: #111b21;
    color: #e9edef;
    border: 1px solid #2a3942;
    border-radius: 10px;
    padding: 8px;
}

QListWidget::item {
    padding: 8px;
    border-radius: 6px;
}

QListWidget::item:selected {
    background-color: #2a3942;
    color: #00a884;
}

QMenuBar {
    background-color: #111b21;
    color: #e9edef;
}

QStatusBar {
    background-color: #111b21;
    color: #8696a0;
}

QLabel#label_logo {
    font-size: 32px;
    font-weight: bold;
    color: white;
}
"""


class TelaLogin(QMainWindow):

    def __init__(self, controller):
        super().__init__()

        self.ui = Ui_Login()
        self.ui.setupUi(self)

        self.setWindowTitle("ZIPZAP")
        self.setFixedSize(self.size())

        self.controller = controller

        self.setStyleSheet(TEMA)

        for label in self.findChildren(QLabel):
            if label.text().strip().upper() == "ZIP ZAP":
                label.setStyleSheet("""
                    font-size: 32px;
                    font-weight: bold;
                    color: white;
                """)       

        self.ui.btn_login.clicked.connect(self.fazer_login)
        self.ui.btn_criar_usuario.clicked.connect(self.criar_usuario)

    def criar_usuario(self):
        nome = self.ui.input_usuario.text().strip()

        if nome == "":
            QMessageBox.warning(self, "Erro", "Digite o nome do usuário.")
            return

        try:
            self.controller.criar_usuario(nome)

            QMessageBox.information(
                self,
                "Sucesso",
                f"Usuário '{nome}' criado!"
            )

            self.ui.input_usuario.clear()

            if hasattr(self.ui, "input_senha"):
                self.ui.input_senha.clear()

        except ValueError as erro:
            QMessageBox.warning(self, "Erro", str(erro))

    def fazer_login(self):
        nome = self.ui.input_usuario.text().strip()

        if nome == "":
            QMessageBox.warning(
                self,
                "Campo obrigatório",
                "Digite o nome do usuário."
            )
            return

        try:
            self.controller.login(nome)

            self.chat = TelaChat(self.controller, nome)
            self.chat.show()
            self.hide()

        except ValueError:
            QMessageBox.warning(
                self,
                "Usuário não cadastrado",
                "Usuário não encontrado. Cadastre-se primeiro antes de entrar."
            )

            self.ui.input_usuario.clear()
            self.ui.input_usuario.setFocus()


class TelaChat(QMainWindow):

    def __init__(self, controller, usuario_logado):
        super().__init__()

        self.ui = Ui_Chat()
        self.ui.setupUi(self)

        self.setWindowTitle("ZIPZAP")

        # trava o tamanho da janela
        self.setFixedSize(self.size())

        self.controller = controller
        self.usuario_logado = usuario_logado
        self.sala_atual = None

        self.ui.label_usuario_logado.setText(f"Usuário: {self.usuario_logado}")
        self.ui.label_sala_atual.setText("Sala: Nenhuma sala selecionada")

        self.setStyleSheet(TEMA)

        self.ui.btn_criar_sala.clicked.connect(self.criar_sala)
        self.ui.btn_entrar_sala.clicked.connect(self.entrar_sala)
        self.ui.btn_listar_salas.clicked.connect(self.listar_salas)
        self.ui.btn_enviar.clicked.connect(self.enviar_mensagem)
        self.ui.input_mensagem.returnPressed.connect(self.enviar_mensagem)
        self.ui.btn_deletar_mensagem.clicked.connect(self.deletar_mensagem)
        self.ui.btn_deletar_mensagem.setStyleSheet("""
        QPushButton {
            background-color: #ff3b30;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 9px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #ff5c52;
        }

        QPushButton:pressed {
            background-color: #cc2f26;
        }
        """)

    def area_status_inicial(self):
        self.ui.area_mensagens.clear()
        self.ui.area_mensagens.append(
            "Selecione ou crie uma sala para começar."
        )

    def criar_sala(self):
        nome_sala = self.ui.input_sala.text().strip()

        if nome_sala == "":
            QMessageBox.warning(self, "Erro", "Digite o nome da sala.")
            return

        try:
            self.controller.criar_sala(nome_sala)

            QMessageBox.information(
                self,
                "Sucesso",
                f"Sala '{nome_sala}' criada!"
            )

            self.ui.input_sala.clear()
            self.listar_salas()

        except ValueError as erro:
            QMessageBox.warning(self, "Erro", str(erro))

    def listar_salas(self):
        try:
            resposta = self.controller.listar_salas()
            texto_formatado = formatar_lista_salas(resposta)

            self.ui.lista_salas.clear()

            if texto_formatado == "Nenhuma sala encontrada.":
                return

            salas = texto_formatado.split("\n")

            for sala in salas:
                if sala.strip():
                    self.ui.lista_salas.addItem(sala.strip())

        except ValueError as erro:
            QMessageBox.warning(self, "Erro", str(erro))

    def entrar_sala(self):
        item = self.ui.lista_salas.currentItem()

        if item is None:
            QMessageBox.warning(self, "Erro", "Selecione uma sala.")
            return

        nome_sala = item.text()

        try:
            self.controller.entrar_sala(nome_sala)
            self.sala_atual = nome_sala

            for label in self.findChildren(QLabel):
                if label.text().startswith("Sala:"):
                    label.setText(f"Sala: {self.sala_atual}")

            self.ui.area_mensagens.clear()
            self.atualizar_mensagens()

        except ValueError as erro:
            QMessageBox.warning(self, "Erro", str(erro))

    def atualizar_mensagens(self):
        if self.sala_atual is None:
            return

        try:
            resposta = self.controller.listar_mensagens()
            texto_formatado = formatar_lista_mensagens(resposta)

            self.ui.area_mensagens.clear()

            if texto_formatado != "Nenhuma mensagem encontrada.":
                self.ui.area_mensagens.append(texto_formatado)

        except ValueError as erro:
            QMessageBox.warning(self, "Erro", str(erro))

    def enviar_mensagem(self):
        texto = self.ui.input_mensagem.text().strip()

        if self.sala_atual is None:
            QMessageBox.warning(self, "Erro", "Entre em uma sala primeiro.")
            return

        if texto == "":
            return

        try:
            self.controller.enviar_mensagem(texto)

            self.ui.input_mensagem.clear()
            self.atualizar_mensagens()

        except ValueError as erro:
            QMessageBox.warning(self, "Erro", str(erro))

    def deletar_mensagem(self):
        if self.sala_atual is None:
            QMessageBox.warning(self, "Erro", "Entre em uma sala primeiro.")
            return

        try:
            self.controller.apagar_mensagem()

            QMessageBox.information(
                self,
                "Sucesso",
                "Sua última mensagem foi apagada."
            )

            self.atualizar_mensagens()

        except ValueError as erro:
            QMessageBox.warning(self, "Erro", str(erro))


def main():
    app = QApplication(sys.argv)

    controller = criar_controller()

    janela = TelaLogin(controller)
    janela.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()