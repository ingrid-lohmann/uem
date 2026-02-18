from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Any

Simbolo = Any
Tipo = Any

class No:
    pass

class Cmd(No):
    pass

class Expressao(No):
    tipo: Optional[Tipo] = None

@dataclass
class Programa(No):
    id: str
    declaracoes: List[Declaracao]
    comando_composto: ComandoComposto
    total_vars: int = 0

@dataclass
class Declaracao(No):
    ids: List[CalcId] 
    tipo_nome: str   


@dataclass
class ComandoComposto(Cmd):
    lista_cmds: List[Cmd]

@dataclass
class Atribuicao(Cmd):
    id: CalcId
    expressao: Expressao

@dataclass
class Condicional(Cmd):
    expressao: Expressao
    cmd_then: Cmd
    cmd_else: Optional[Cmd] = None

@dataclass
class Repeticao(Cmd): 
    expressao: Expressao
    cmd: Cmd

@dataclass
class Leitura(Cmd): 
    ids: List[CalcId]

@dataclass
class Escrita(Cmd):
    expressoes: List[Expressao]

@dataclass
class ExpressaoBinaria(Expressao):
    esq: Expressao
    op: str
    dir: Expressao

@dataclass
class ExpressaoUnaria(Expressao):
    op: str
    expressao: Expressao

@dataclass
class CalcId(Expressao):
    nome: str
    simbolo: Optional[Simbolo] = None

@dataclass
class ConstanteInt(Expressao):
    valor: int

@dataclass
class ConstanteBool(Expressao):
    valor: bool