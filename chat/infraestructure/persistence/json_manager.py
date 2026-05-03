from chat.domain.shared.result import Resultado
import json

class GerenciadorJson:
    @staticmethod
    def ler_arquivo(caminho_arquivo, **filtros):
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)

                if filtros:
                    dados_filtrados = []

                    for item in dados:
                        if all(item.get(chave) == valor for chave, valor in filtros.items()):
                            dados_filtrados.append(item)
                    return Resultado.ok(dados_filtrados)
                return Resultado.ok(dados)

        # Permite a manipulação ou criação do arquivo, se ele não existir ou estiver vazio ou corrompido
        # quando o método de adicionar ou remover for usado.
        except (FileNotFoundError, json.JSONDecodeError):
            return Resultado.ok([])
        except Exception as ex:
            return Resultado.falha(f"Erro inesperado ao tentar ler o arquivo: {str(ex)}")

    @staticmethod
    def _escrever_arquivo(caminho_arquivo, conteudo):
        try:
            with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                        # ensure_ascii como False serve para escrever as letras acentuadas
                        # no arquivo sem converter elas em código ASCII (ou seja, mais legível
                        # ao ler o manualmente arquivo). Além disso, o indent=4 faz com que cada
                        # dado (chave/valor) fique em uma linha separada, além de adicionar 4
                        # espaços de recuo para cada nível de profundidade
                        json.dump(conteudo, arquivo, ensure_ascii=False, indent=4)
            return Resultado.ok(conteudo)

        # Esse erro só ocorre durante a escrita quando o diretório no caminho não existe, caso contrário,
        # o arquivo é criado corretamente
        except FileNotFoundError:
            return Resultado.falha(f"O diretório do caminho {caminho_arquivo} não foi encontrado ao tentar escrever")
        except Exception as ex:
            return Resultado.falha(f"Erro inesperado ao tentar escrever no arquivo: {str(ex)}")

    @staticmethod
    def adicionar_item(caminho_arquivo, item):
        resultado_leitura = GerenciadorJson.ler_arquivo(caminho_arquivo)

        if not resultado_leitura.sucesso:
            return resultado_leitura

        dados = resultado_leitura.conteudo
        dados.append(item)

        resultado_escrita = GerenciadorJson._escrever_arquivo(caminho_arquivo, dados)

        if resultado_escrita.sucesso:
            return Resultado.ok(item)
        return resultado_escrita

    @staticmethod
    def remover_item(caminho_arquivo, **filtros):
        resultado_leitura = GerenciadorJson.ler_arquivo(caminho_arquivo)

        if not resultado_leitura.sucesso:
            return resultado_leitura

        dados_restantes = []

        for item in resultado_leitura.conteudo:
            if not all(item.get(chave) == valor for chave, valor in filtros.items()):
                dados_restantes.append(item)

        resultado_escrita = GerenciadorJson._escrever_arquivo(caminho_arquivo, dados_restantes)

        if resultado_escrita.sucesso:
            return Resultado.ok()
        return resultado_escrita