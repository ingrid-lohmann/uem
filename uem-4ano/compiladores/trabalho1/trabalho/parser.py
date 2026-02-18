from lexer import tokens
import ply.yacc as yacc
from analise_semantica import (
    tabela_simbolos, erros_semanticos, adicionar_variavel,
    verificar_declaracao, checar_id_programa, checar_atribuicao,
    checar_condicao_booleana, checar_operacao_logica_relacional,
    checar_operacao_matematica, checar_not, checar_uminus)

erros_sintaticos = []

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
    '''programa : PROGRAM ID PONTO_VIRGULA bloco fim_do_programa'''
    if p[5] is False:  
        linha_do_end = p[4]  #
        mensagem = f"ERRO SINTÁTICO próximo à linha {linha_do_end}: Esperava um '.' (ponto final) após o 'end' para finalizar o programa."
        if mensagem not in erros_sintaticos:
            erros_sintaticos.append(mensagem)

    checar_id_programa(p[2], p.lineno(2))
    tabela_simbolos[p[2]] = {'tipo': None, 'categoria': 'programa'}


def p_bloco(p):
    '''bloco : secao_declaracao_variaveis comando_composto
             | comando_composto'''
    p[0] = p[len(p) - 1]


def p_secao_declaracao_variaveis(p):
    '''secao_declaracao_variaveis : VAR lista_declaracoes'''


def p_lista_declaracoes(p):
    '''lista_declaracoes : lista_declaracoes declaracao_variaveis PONTO_VIRGULA
                         | declaracao_variaveis PONTO_VIRGULA'''


def p_declaracao_variaveis(p):
    '''declaracao_variaveis : lista_identificadores DOIS_PONTOS tipo'''
    tipo_var = p[3]
    for nome_var in p[1]:
        adicionar_variavel(nome_var['nome'], tipo_var, nome_var['linha'])


def p_lista_identificadores(p):
    '''lista_identificadores : lista_identificadores VIRGULA ID
                             | ID'''
    if len(p) == 2:
        p[0] = [{'nome': p[1], 'linha': p.lineno(1)}]
    else:
        p[0] = p[1] + [{'nome': p[3], 'linha': p.lineno(3)}]


def p_tipo(p):
    '''tipo : INTEGER
            | BOOLEAN'''
    p[0] = p[1]


def p_comando_composto(p):
    '''comando_composto : BEGIN lista_comandos END'''
    p[0] = p.lineno(3)


def p_lista_comandos(p):
    '''lista_comandos : lista_comandos PONTO_VIRGULA comando
                      | comando
                      | empty'''


def p_comando(p):
    '''comando : atribuicao
               | condicional
               | repeticao
               | leitura
               | escrita
               | comando_composto'''


def p_atribuicao(p):
    '''atribuicao : ID ATRIBUICAO expressao'''
    tipo_variavel = verificar_declaracao(p[1], p.lineno(1))
    checar_atribuicao(tipo_variavel, p[3], p[1], p.lineno(1))


def p_condicional(p):
    '''condicional : IF expressao THEN comando
                   | IF expressao THEN comando ELSE comando'''
    checar_condicao_booleana(p[2], p.lineno(1), 'if')


def p_repeticao(p):
    '''repeticao : WHILE expressao DO comando'''
    checar_condicao_booleana(p[2], p.lineno(1), 'while')


def p_leitura(p):
    '''leitura : READ PARENTESE_ESQ lista_identificadores PARENTESE_DIR'''
    for var in p[3]:
        verificar_declaracao(var['nome'], var['linha'])


def p_escrita(p):
    '''escrita : WRITE PARENTESE_ESQ lista_expressoes PARENTESE_DIR'''


def p_lista_expressoes(p):
    '''lista_expressoes : lista_expressoes VIRGULA expressao
                        | expressao'''


# --- Regras de Expressão ---
def p_expressao_binaria(p):
    '''expressao : expressao AND expressao
                 | expressao OR expressao
                 | expressao OP_RELACIONAL expressao'''
    p[0] = checar_operacao_logica_relacional(p[1], p.slice[2], p[2], p[3],
                                             p.lineno(2))


def p_expressao_matematica(p):
    '''expressao : expressao OP_SOMA expressao
                 | expressao OP_SUBTRACAO expressao
                 | expressao OP_MULTIPLICA expressao
                 | expressao DIV expressao'''
    p[0] = checar_operacao_matematica(p[1], p.slice[2], p[2], p[3],
                                      p.lineno(2))


def p_expressao_unaria(p):
    '''expressao : NOT expressao'''
    p[0] = checar_not(p[2], p.lineno(1))


def p_expressao_uminus(p):
    '''expressao : OP_SUBTRACAO expressao %prec UMINUS'''
    p[0] = checar_uminus(p[2], p.lineno(1))


def p_expressao_agrupamento(p):
    '''expressao : PARENTESE_ESQ expressao PARENTESE_DIR'''
    p[0] = p[2]


def p_expressao_base(p):
    '''expressao : ID
                 | NUMERO
                 | TRUE
                 | FALSE'''
    tipo_token = p.slice[1].type
    if tipo_token == 'ID':
        p[0] = verificar_declaracao(p[1], p.lineno(1))
    elif tipo_token == 'NUMERO':
        p[0] = 'integer'
    elif tipo_token in ['TRUE', 'FALSE']:
        p[0] = 'boolean'


def p_empty(p):
    'empty :'
    pass


# --- Regras de Recuperação de Erro ---

def p_fim_do_programa_ok(p):
    '''fim_do_programa : PONTO_FINAL'''
    p[0] = True  # Sucesso


def p_fim_do_programa_erro_token(p):
    '''fim_do_programa : error'''
    if erros_sintaticos:
        erros_sintaticos.pop()
    p[0] = False  # Erro


def p_fim_do_programa_erro_eof(p):
    '''fim_do_programa : empty'''
    if erros_sintaticos:
        if "Fim de arquivo inesperado" in erros_sintaticos[-1]:
            erros_sintaticos.pop()
    p[0] = False  # Erro


def p_programa_erro(p):
    '''programa : PROGRAM error PONTO_VIRGULA bloco PONTO_FINAL'''
    parser.errok()


def p_lista_declaracoes_erro(p):
    '''lista_declaracoes : lista_declaracoes error PONTO_VIRGULA'''
    parser.errok()


def p_expressao_operador_erro(p):
    '''expressao : expressao AND error
                 | expressao OR error
                 | expressao OP_RELACIONAL error
                 | expressao OP_SOMA error
                 | expressao OP_SUBTRACAO error
                 | expressao OP_MULTIPLICA error
                 | expressao DIV error'''

    op_valor = p[2]
    linha = p.lineno(2)

    if erros_sintaticos and "Token inesperado" in erros_sintaticos[-1]:
        erros_sintaticos.pop()

    mensagem = f"ERRO SINTÁTICO na linha {linha}: Operando faltando após o operador '{op_valor}'."

    if mensagem not in erros_sintaticos:
        erros_sintaticos.append(mensagem)


def p_atribuicao_erro(p):
    '''atribuicao : ID ATRIBUICAO expressao error'''
    if erros_sintaticos:
        erros_sintaticos.pop()
    linha = p.lineno(1)
    mensagem = f"ERRO SINTÁTICO na linha {linha}: Está faltando um ponto e vírgula após a atribuição."
    erros_sintaticos.append(mensagem)


def p_lista_comandos_erro(p):
    '''lista_comandos : lista_comandos PONTO_VIRGULA error'''
    parser.errok()


def p_condicional_erro(p):
    '''condicional : IF expressao error'''
    if erros_sintaticos:
        erros_sintaticos.pop()
    linha = p.lineno(1)
    mensagem = f"ERRO SINTÁTICO na linha {linha}: Palavra-chave 'then' esperada após a expressão do 'if'."
    erros_sintaticos.append(mensagem)


def p_repeticao_erro(p):
    '''repeticao : WHILE expressao error'''
    if erros_sintaticos:
        erros_sintaticos.pop()
    linha = p.lineno(1)
    mensagem = f"ERRO SINTÁTICO na linha {linha}: Palavra-chave 'do' esperada após a expressão do 'while'."
    erros_sintaticos.append(mensagem)


def p_leitura_erro(p):
    '''leitura : READ PARENTESE_ESQ error PARENTESE_DIR'''
    if erros_sintaticos:
        erros_sintaticos.pop()
    linha = p.lineno(1)
    mensagem = f"ERRO SINTÁTICO na linha {linha}: O comando 'read' aceita apenas variáveis como argumentos, não literais ou expressões."
    erros_sintaticos.append(mensagem)


def p_lista_expressoes_erro(p):
    '''lista_expressoes : lista_expressoes VIRGULA error'''
    if erros_sintaticos:
        erros_sintaticos.pop()
    linha = p.lineno(2)
    mensagem = f"ERRO SINTÁTICO na linha {linha}: Vírgula extra ou argumento faltando na lista de parâmetros."
    erros_sintaticos.append(mensagem)


# --- Função Principal de Tratamento de Erros ---
def p_error(t):
    if t:
        mensagem = f"Token inesperado '{t.value}' na linha {t.lineno}"
        erros_sintaticos.append(f"ERRO SINTÁTICO: {mensagem}")
    else:
        if not erros_sintaticos or "Fim de arquivo" not in erros_sintaticos[-1]:
            erros_sintaticos.append(
                "ERRO SINTÁTICO: Fim de arquivo inesperado.")


parser = yacc.yacc()
