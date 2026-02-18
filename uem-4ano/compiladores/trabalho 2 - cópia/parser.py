import ply.yacc as yacc
from lexer import tokens, lexer
import ast_tascal as ast

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'OP_RELACIONAL'),
    ('left', 'OP_SOMA', 'OP_SUBTRACAO'),
    ('left', 'OP_MULTIPLICA', 'DIV'),
    ('right', 'UMINUS'),
)

def p_programa(p):
    '''programa : PROGRAM ID PONTO_VIRGULA bloco PONTO_FINAL'''
    declaracoes = p[4]['declaracoes']
    cmd_composto = p[4]['comando_composto']

    p[0] = ast.Programa(
        id=p[2],
        declaracoes=declaracoes,
        comando_composto=cmd_composto
    )

def p_bloco(p):
    '''bloco : secao_declaracao_variaveis comando_composto
             | comando_composto'''
    if len(p) == 3:
        p[0] = {
            'declaracoes': p[1],
            'comando_composto': p[2]
        }
    else:
        p[0] = {
            'declaracoes': [],
            'comando_composto': p[1]
        }

# --- Declarações ---

def p_secao_declaracao_variaveis(p):
    '''secao_declaracao_variaveis : VAR lista_declaracoes'''
    p[0] = p[2] 

def p_lista_declaracoes(p):
    '''lista_declaracoes : lista_declaracoes declaracao_variaveis PONTO_VIRGULA
                         | declaracao_variaveis PONTO_VIRGULA'''
    if len(p) == 4:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_declaracao_variaveis(p):
    '''declaracao_variaveis : lista_identificadores DOIS_PONTOS tipo'''
    p[0] = ast.Declaracao(ids=p[1], tipo_nome=p[3])

def p_lista_identificadores(p):
    '''lista_identificadores : lista_identificadores VIRGULA ID
                             | ID'''
    if len(p) == 4:
        p[0] = p[1] + [ast.CalcId(nome=p[3])]
    else:
        p[0] = [ast.CalcId(nome=p[1])]

def p_tipo(p):
    '''tipo : INTEGER
            | BOOLEAN'''
    p[0] = p[1]

# --- Comandos ---

def p_comando_composto(p):
    '''comando_composto : BEGIN lista_comandos END'''
    p[0] = ast.ComandoComposto(lista_cmds=p[2])

def p_lista_comandos(p):
    '''lista_comandos : lista_comandos PONTO_VIRGULA comando
                      | comando
                      | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]

def p_comando(p):
    '''comando : atribuicao
               | condicional
               | repeticao
               | leitura
               | escrita
               | comando_composto'''
    p[0] = p[1]

def p_atribuicao(p):
    '''atribuicao : ID ATRIBUICAO expressao'''
    p[0] = ast.Atribuicao(
        id=ast.CalcId(nome=p[1]), 
        expressao=p[3]
    )

def p_condicional(p):
    '''condicional : IF expressao THEN comando
                   | IF expressao THEN comando ELSE comando'''
    if len(p) == 7:
        p[0] = ast.Condicional(expressao=p[2], cmd_then=p[4], cmd_else=p[6])
    else:
        p[0] = ast.Condicional(expressao=p[2], cmd_then=p[4], cmd_else=None)

def p_repeticao(p):
    '''repeticao : WHILE expressao DO comando'''
    p[0] = ast.Repeticao(expressao=p[2], cmd=p[4])

def p_leitura(p):
    '''leitura : READ PARENTESE_ESQ lista_identificadores PARENTESE_DIR'''
    p[0] = ast.Leitura(ids=p[3])

def p_escrita(p):
    '''escrita : WRITE PARENTESE_ESQ lista_expressoes PARENTESE_DIR'''
    p[0] = ast.Escrita(expressoes=p[3])

def p_lista_expressoes(p):
    '''lista_expressoes : lista_expressoes VIRGULA expressao
                        | expressao'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# --- Expressões ---

def p_expressao_binaria(p):
    '''expressao : expressao AND expressao
                 | expressao OR expressao
                 | expressao OP_RELACIONAL expressao
                 | expressao OP_SOMA expressao
                 | expressao OP_SUBTRACAO expressao
                 | expressao OP_MULTIPLICA expressao
                 | expressao DIV expressao'''
    p[0] = ast.ExpressaoBinaria(esq=p[1], op=p[2], dir=p[3])

def p_expressao_unaria(p):
    '''expressao : NOT expressao'''
    p[0] = ast.ExpressaoUnaria(op=p[1], expressao=p[2])

def p_expressao_uminus(p):
    '''expressao : OP_SUBTRACAO expressao %prec UMINUS'''
    p[0] = ast.ExpressaoUnaria(op='-', expressao=p[2])

def p_expressao_agrupamento(p):
    '''expressao : PARENTESE_ESQ expressao PARENTESE_DIR'''
    p[0] = p[2]

def p_expressao_base(p):
    '''expressao : ID
                 | NUMERO
                 | TRUE
                 | FALSE'''
    token_type = p.slice[1].type
    if token_type == 'ID':
        p[0] = ast.CalcId(nome=p[1])
    elif token_type == 'NUMERO':
        p[0] = ast.ConstanteInt(valor=p[1])
    elif token_type == 'TRUE':
        p[0] = ast.ConstanteBool(valor=True)
    elif token_type == 'FALSE':
        p[0] = ast.ConstanteBool(valor=False)

def p_empty(p):
    'empty :'
    pass

def p_error(t):
    if t:
        print(f"Erro sintático: Token inesperado '{t.value}' na linha {t.lineno}")
    else:
        print("Erro sintático: Fim de arquivo inesperado.")

parser = yacc.yacc()