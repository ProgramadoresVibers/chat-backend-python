from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    def validar_texto_obrigatorio(self, valor, nome_campo):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{nome_campo} e obrigatorio.")

        return valor.strip()

    def validar_inteiro_positivo(self, valor, nome_campo):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError(f"{nome_campo} deve ser um numero inteiro positivo.")

        return valor

    @abstractmethod
    def validar(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def executar(self, *args, **kwargs) -> Any:
        pass
