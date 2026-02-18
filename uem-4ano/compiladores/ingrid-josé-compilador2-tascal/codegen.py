from __future__ import annotations
from typing import List
import ast_tascal as ast
from defs_tascal import Visitador

NIVEL_LEXICO = 0


class GeradorCodigo(Visitador):

    def __init__(self):
        self.codigo: List[str] = []
        self.contador_rotulos = 0

        self.mapa_ops = {
            '+': 'SOMA',
            '-': 'SUBT',
            '*': 'MULT',
            'div': 'DIVI',
            'and': 'CONJ',
            'or': 'DISJ',
            'not': 'NEGA',
            '=': 'CMIG',
            '<>': 'CMDG',
            '<': 'CMME',
            '>': 'CMMA',
            '<=': 'CMEG',
            '>=': 'CMAG'
        }

    def obter_codigo(self) -> str:
        return "\n".join(self.codigo)


    def _emite(self, instrucao: str):
        self.codigo.append(f"    {instrucao}")

    def _novo_rotulo(self) -> str:
        lbl = f"R{self.contador_rotulos:02d}"
        self.contador_rotulos += 1
        return lbl

    def _emite_rotulo(self, rotulo: str):
        self.codigo.append(f"{rotulo}: NADA")


    def visita_Programa(self, no: ast.Programa):
        self._emite("INPP")

        if no.total_vars > 0:
            self._emite(f"AMEM {no.total_vars}")

        self.visita(no.comando_composto)

        if no.total_vars > 0:
            self._emite(f"DMEM {no.total_vars}")

        self._emite("PARA")
        self.codigo.append("FIM")

    def visita_ComandoComposto(self, no: ast.ComandoComposto):
        for cmd in no.lista_cmds:
            self.visita(cmd)

    def visita_Atribuicao(self, no: ast.Atribuicao):
        self.visita(no.expressao)
        simbolo = no.id.simbolo
        self._emite(f"ARMZ {NIVEL_LEXICO},{simbolo.deslocamento}")

    def visita_Leitura(self, no: ast.Leitura):
        for id_node in no.ids:
            self._emite("LEIT")
            simbolo = id_node.simbolo
            self._emite(f"ARMZ {NIVEL_LEXICO},{simbolo.deslocamento}")

    def visita_Escrita(self, no: ast.Escrita):
        for expr in no.expressoes:
            self.visita(expr)
            self._emite("IMPR")

    def visita_Condicional(self, no: ast.Condicional):
        lbl_else = self._novo_rotulo()
        lbl_fim = self._novo_rotulo()

        self.visita(no.expressao)

        self._emite(f"DSVF {lbl_else}")

        self.visita(no.cmd_then)

        self._emite(f"DSVS {lbl_fim}")

        self._emite_rotulo(lbl_else)
        if no.cmd_else:
            self.visita(no.cmd_else)

        self._emite_rotulo(lbl_fim)

    def visita_Repeticao(self, no: ast.Repeticao):
        lbl_inicio = self._novo_rotulo()
        lbl_fim = self._novo_rotulo()

        self._emite_rotulo(lbl_inicio)

        self.visita(no.expressao)
        self._emite(f"DSVF {lbl_fim}")

        self.visita(no.cmd)

        self._emite(f"DSVS {lbl_inicio}")

        self._emite_rotulo(lbl_fim)


    def visita_ExpressaoBinaria(self, no: ast.ExpressaoBinaria):
        self.visita(no.esq)
        self.visita(no.dir)

        instr = self.mapa_ops.get(no.op)
        if instr:
            self._emite(instr)
        else:
            raise ValueError(f"Operador desconhecido na geração: {no.op}")

    def visita_ExpressaoUnaria(self, no: ast.ExpressaoUnaria):
        self.visita(no.expressao)

        if no.op == '-':
            self._emite("INVR")
        elif no.op == 'not':
            self._emite("NEGA")

    def visita_CalcId(self, no: ast.CalcId):
        simbolo = no.simbolo
        self._emite(f"CRVL {NIVEL_LEXICO},{simbolo.deslocamento}")

    def visita_ConstanteInt(self, no: ast.ConstanteInt):
        self._emite(f"CRCT {no.valor}")

    def visita_ConstanteBool(self, no: ast.ConstanteBool):
        val = 1 if no.valor else 0
        self._emite(f"CRCT {val}")
