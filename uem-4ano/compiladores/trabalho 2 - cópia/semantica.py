from __future__ import annotations
from typing import List, Dict
import ast_tascal as ast
from defs_tascal import Visitador, Simbolo, TIPO_INT, TIPO_BOOL, Categoria

class VerificadorSemantico(Visitador):
    def __init__(self):
        self.tabela: Dict[str, Simbolo] = {}
        self.erros: List[str] = []
        self.deslocamento_atual = 0  # Contador para o endereço de memória MEPA

    def erro(self, no, msg):
        # Tenta pegar a linha do nó, se existir (o PLY às vezes não passa linha para nós internos, 
        # mas vamos assumir que o parser repassou ou o nó tem essa info de alguma forma. 
        # Caso contrário, indicamos erro geral).
        linha = getattr(no, 'linha', '?') 
        self.erros.append(f"ERRO SEMÂNTICO: {msg}")

    # --- Programa e Declarações ---

    def visita_Programa(self, no: ast.Programa):
        # 1. Visita declarações para popular tabela de símbolos
        for decl in no.declaracoes:
            self.visita(decl)

        # 2. Guarda o total de variáveis no nó do Programa (essencial para o AMEM do gerador de código)
        no.total_vars = self.deslocamento_atual

        # 3. Visita o corpo do programa
        self.visita(no.comando_composto)

    def visita_Declaracao(self, no: ast.Declaracao):
        # Define o tipo base (integer ou boolean)
        tipo_declarado = TIPO_INT if no.tipo_nome == 'integer' else TIPO_BOOL

        for id_node in no.ids:
            nome = id_node.nome

            # Checa duplicidade
            if nome in self.tabela:
                self.erro(no, f"Variável '{nome}' já declarada.")
            else:
                # Cria símbolo com o endereço de memória atual
                simbolo = Simbolo(
                    nome=nome, 
                    tipo=tipo_declarado, 
                    deslocamento=self.deslocamento_atual
                )
                self.tabela[nome] = simbolo

                # Linka o nó da AST ao símbolo (Anotação)
                id_node.simbolo = simbolo

                # Incrementa endereço para a próxima variável
                self.deslocamento_atual += 1

    # --- Comandos ---

    def visita_ComandoComposto(self, no: ast.ComandoComposto):
        for cmd in no.lista_cmds:
            self.visita(cmd)

    def visita_Atribuicao(self, no: ast.Atribuicao):
        # Visita ID (Lado Esquerdo)
        self.visita(no.id)
        # Visita Expressão (Lado Direito)
        self.visita(no.expressao)

        tipo_var = no.id.tipo
        tipo_expr = no.expressao.tipo

        if tipo_var and tipo_expr:
            if tipo_var != tipo_expr:
                self.erro(no, f"Atribuição inválida: variável '{no.id.nome}' é '{tipo_var}', expressão é '{tipo_expr}'.")

    def visita_Condicional(self, no: ast.Condicional):
        self.visita(no.expressao)
        if no.expressao.tipo != TIPO_BOOL:
            self.erro(no, "A condição do 'if' deve ser do tipo 'boolean'.")

        self.visita(no.cmd_then)
        if no.cmd_else:
            self.visita(no.cmd_else)

    def visita_Repeticao(self, no: ast.Repeticao):
        self.visita(no.expressao)
        if no.expressao.tipo != TIPO_BOOL:
            self.erro(no, "A condição do 'while' deve ser do tipo 'boolean'.")

        self.visita(no.cmd)

    def visita_Leitura(self, no: ast.Leitura):
        for id_node in no.ids:
            self.visita(id_node)
            # O Tascal permite ler inteiros e booleanos? Geralmente sim.
            if id_node.tipo is None:
                # Se tipo é None, é porque variável não foi declarada (erro já capturado no visita_CalcId)
                pass

    def visita_Escrita(self, no: ast.Escrita):
        for expr in no.expressoes:
            self.visita(expr)

    # --- Expressões ---

    def visita_ExpressaoBinaria(self, no: ast.ExpressaoBinaria):
        self.visita(no.esq)
        self.visita(no.dir)

        tipo_esq = no.esq.tipo
        tipo_dir = no.dir.tipo

        # Se algum dos lados já deu erro (None), aborta verificação deste nó
        if tipo_esq is None or tipo_dir is None:
            no.tipo = None
            return

        op = no.op

        # Lógica Aritmética (+, -, *, div)
        if op in ['+', '-', '*', 'div']:
            if tipo_esq != TIPO_INT or tipo_dir != TIPO_INT:
                self.erro(no, f"Operador aritmético '{op}' exige operandos 'integer'.")
                no.tipo = None
            else:
                no.tipo = TIPO_INT

        # Lógica Booleana (and, or)
        elif op in ['and', 'or']:
            if tipo_esq != TIPO_BOOL or tipo_dir != TIPO_BOOL:
                self.erro(no, f"Operador lógico '{op}' exige operandos 'boolean'.")
                no.tipo = None
            else:
                no.tipo = TIPO_BOOL

        # Lógica Relacional (=, <>, <, >, <=, >=)
        elif op in ['=', '<>', '<', '>', '<=', '>=']:
            # Igualdade/Desigualdade funciona para ambos (desde que iguais entre si)
            if op in ['=', '<>']:
                if tipo_esq != tipo_dir:
                    self.erro(no, f"Operador '{op}' exige operandos do mesmo tipo.")
                    no.tipo = None
                else:
                    no.tipo = TIPO_BOOL
            # Ordem (<, >, etc) só para inteiros
            else:
                if tipo_esq != TIPO_INT or tipo_dir != TIPO_INT:
                    self.erro(no, f"Operador relacional '{op}' exige operandos 'integer'.")
                    no.tipo = None
                else:
                    no.tipo = TIPO_BOOL

    def visita_ExpressaoUnaria(self, no: ast.ExpressaoUnaria):
        self.visita(no.expressao)
        tipo = no.expressao.tipo

        if tipo is None:
            no.tipo = None
            return

        if no.op == 'not':
            if tipo != TIPO_BOOL:
                self.erro(no, "Operador 'not' exige operando 'boolean'.")
                no.tipo = None
            else:
                no.tipo = TIPO_BOOL
        elif no.op == '-':
            if tipo != TIPO_INT:
                self.erro(no, "Operador unário '-' exige operando 'integer'.")
                no.tipo = None
            else:
                no.tipo = TIPO_INT

    def visita_CalcId(self, no: ast.CalcId):
        nome = no.nome
        if nome in self.tabela:
            simbolo = self.tabela[nome]
            no.simbolo = simbolo # Anotação crucial para o CodeGen!
            no.tipo = simbolo.tipo
        else:
            self.erro(no, f"Variável '{nome}' não declarada.")
            no.tipo = None

    def visita_ConstanteInt(self, no: ast.ConstanteInt):
        no.tipo = TIPO_INT

    def visita_ConstanteBool(self, no: ast.ConstanteBool):
        no.tipo = TIPO_BOOL