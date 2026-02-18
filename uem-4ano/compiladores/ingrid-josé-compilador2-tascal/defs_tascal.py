from __future__ import annotations
from dataclasses import dataclass
import ast_tascal as ast

class Tipo:
    pass

@dataclass(frozen=True)
class TipoInt(Tipo):
    def __str__(self) -> str: return "integer"

@dataclass(frozen=True)
class TipoBool(Tipo):
    def __str__(self) -> str: return "boolean"

TIPO_INT = TipoInt()
TIPO_BOOL = TipoBool()

class Categoria:
    VAR = 'var'
    PROGRAMA = 'programa'

@dataclass
class Simbolo:
    nome: str
    categoria: str = Categoria.VAR
    tipo: Tipo | None = None
    deslocamento: int = 0 

class Visitador:
    def visita(self, no: ast.No):
        if no is None:
            return None

        nome_metodo = f'visita_{type(no).__name__}'
        visitador = getattr(self, nome_metodo, self.visita_padrao)
        return visitador(no)

    def visita_padrao(self, no: ast.No):
        raise NotImplementedError(f"O método '{type(no).__name__}' não foi implementado no visitador.")