from lexer import tokens
import ply.yacc as yacc

tabela_simbolos = {}
erros_semanticos = []
erros_sintaticos = []
ultima_linha_end = 0


# --- Funções Auxiliares para Semântica ---
def erro_semantico(linha, mensagem):
    erros_semanticos.append(f"ERRO SEMÂNTICO na linha {linha}: {mensagem}")


def adicionar_variavel(nome, tipo, linha):
    if nome in tabela_simbolos:
        erro_semantico(linha, f"Variável '{nome}' já declarada.")
    else:
        tabela_simbolos[nome] = {'tipo': tipo, 'categoria': 'variavel'}


def verificar_declaracao(nome, linha):
    if nome not in tabela_simbolos:
        erro_semantico(linha, f"Variável '{nome}' não declarada.")
        return None
    return tabela_simbolos[nome]['tipo']


# --- Definição da Precedência de Operadores ---
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'OP_RELACIONAL'),
    ('left', 'OP_SOMA', 'OP_SUBTRACAO'),
    ('left', 'OP_MULTIPLICA', 'DIV'),
    ('right', 'UMINUS'),
)


# --- Definição da Gramática e Ações Semânticas ---
def p_programa(p):
    '''programa : PROGRAM ID PONTO_VIRGULA bloco ponto_final_ou_erro'''
    if p[2] in tabela_simbolos:
        erro_semantico(
            p.lineno(2),
            f"Identificador de programa '{p[2]}' já utilizado como variável.")
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
    global ultima_linha_end
    ultima_linha_end = p.lineno(3)


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
    if tipo_variavel and p[3] is not None and tipo_variavel != p[3]:
        erro_semantico(
            p.lineno(1),
            f"Tipo da expressão ('{p[3]}') incompatível com o tipo da variável '{p[1]}' ('{tipo_variavel}')."
        )


def p_condicional(p):
    '''condicional : IF expressao THEN comando
                   | IF expressao THEN comando ELSE comando'''
    if p[2] != 'boolean':
        erro_semantico(
            p.lineno(1),
            "A expressão do comando 'if' deve ser do tipo 'boolean'.")


def p_repeticao(p):
    '''repeticao : WHILE expressao DO comando'''
    if p[2] != 'boolean':
        erro_semantico(
            p.lineno(1),
            "A expressão do comando 'while' deve ser do tipo 'boolean'.")


def p_repeticao_erro(p):
    '''repeticao : WHILE expressao error'''

    if erros_sintaticos:
        erros_sintaticos.pop()

    linha = p.lineno(1)
    mensagem = f"ERRO SINTÁTICO na linha {linha}: Palavra-chave 'do' esperada após a expressão do 'while'."
    erros_sintaticos.append(mensagem)


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
    tipo1, op_token, op_valor, tipo2 = p[1], p.slice[2], p[2], p[3]
    if op_token.type in ['AND', 'OR']:
        if tipo1 != 'boolean' or tipo2 != 'boolean':
            erro_semantico(
                p.lineno(2),
                f"Operador lógico '{op_valor}' exige operandos do tipo 'boolean'."
            )
        p[0] = 'boolean'
    elif op_token.type == 'OP_RELACIONAL':
        if op_valor in ['=', '<>']:
            if tipo1 != tipo2:
                erro_semantico(
                    p.lineno(2),
                    f"Operador '{op_valor}' exige operandos do mesmo tipo (recebeu '{tipo1}' e '{tipo2}')."
                )
        else:
            if tipo1 != 'integer' or tipo2 != 'integer':
                erro_semantico(
                    p.lineno(2),
                    f"Operador relacional '{op_valor}' exige operandos do tipo 'integer'."
                )
        p[0] = 'boolean'


def p_expressao_matematica(p):
    '''expressao : expressao OP_SOMA expressao
                 | expressao OP_SUBTRACAO expressao
                 | expressao OP_MULTIPLICA expressao
                 | expressao DIV expressao'''
    tipo1, op_token, op_valor, tipo2 = p[1], p.slice[2], p[2], p[3]
    if op_token.type in ['OP_SOMA', 'OP_SUBTRACAO', 'OP_MULTIPLICA', 'DIV']:
        if tipo1 != 'integer' or tipo2 != 'integer':
            erro_semantico(
                p.lineno(2),
                f"Operador aritmético '{op_valor}' exige operandos do tipo 'integer'."
            )
        p[0] = 'integer'
    elif op_token.type in ['AND', 'OR']:
        if tipo1 != 'boolean' or tipo2 != 'boolean':
            erro_semantico(
                p.lineno(2),
                f"Operador lógico '{op_valor}' exige operandos do tipo 'boolean'."
            )


def p_expressao_unaria(p):
    '''expressao : NOT expressao'''
    if p[2] != 'boolean':
        erro_semantico(p.lineno(1),
                       "Operador 'not' exige um operando do tipo 'boolean'.")
    p[0] = 'boolean'


def p_expressao_uminus(p):
    '''expressao : OP_SUBTRACAO expressao %prec UMINUS'''
    if p[2] != 'integer':
        erro_semantico(
            p.lineno(1),
            "Operador de negação '-' exige um operando do tipo 'integer'.")
    p[0] = 'integer'


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


def p_programa_erro(p):
    '''programa : PROGRAM error PONTO_VIRGULA bloco PONTO_FINAL'''
    parser.errok()


def p_ponto_final_ou_erro(p):
    '''ponto_final_ou_erro : PONTO_FINAL'''
    pass


def p_ponto_final_ou_erro_recuperacao(p):
    '''ponto_final_ou_erro : error'''
    global ultima_linha_end
    linha = ultima_linha_end

    if erros_sintaticos:
        last_error = erros_sintaticos[-1]
        if "Token inesperado" in last_error:
            erros_sintaticos.pop()

    mensagem = f"ERRO SINTÁTICO próximo à linha {linha}: Esperava um '.' (ponto final) após o 'end' para finalizar o programa."

    if mensagem not in erros_sintaticos:
        erros_sintaticos.append(mensagem)


def p_lista_declaracoes_erro(p):
    '''lista_declaracoes : lista_declaracoes error PONTO_VIRGULA'''
    parser.errok()


def p_expressao_logica_relacional_erro(p):
    '''expressao : expressao AND error
                 | expressao OR error
                 | expressao OP_RELACIONAL error'''

    op_valor = p[2]
    linha = p.lineno(2)

    if erros_sintaticos and "Token inesperado" in erros_sintaticos[-1]:
        erros_sintaticos.pop()

    mensagem = f"ERRO SINTÁTICO na linha {linha}: Operando faltando após o operador '{op_valor}'."

    if mensagem not in erros_sintaticos:
        erros_sintaticos.append(mensagem)


def p_expressao_matematica_erro(p):
    '''expressao : expressao OP_SOMA error
                 | expressao OP_SUBTRACAO error
                 | expressao OP_MULTIPLICA error
                 | expressao DIV error'''

    op_valor = p[2]
    linha = p.lineno(2)

    if erros_sintaticos and "Token inesperado" in erros_sintaticos[-1]:
        erros_sintaticos.pop()

    mensagem = f"ERRO SINTÁTICO na linha {linha}: Operando faltando após o operador aritmético '{op_valor}'."

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
    global ultima_linha_end
    if t:
        # Caso padrão para um token (ex: 'end,')
        # A regra p_ponto_final_ou_erro_recuperacao vai tratar isso
        mensagem = f"Token inesperado '{t.value}' na linha {t.lineno}"
        erros_sintaticos.append(f"ERRO SINTÁTICO: {mensagem}")
    else:
        # Caso de Fim de Arquivo (EOF)
        if ultima_linha_end > 0:
            # Se sabemos a linha do 'end', damos o erro customizado
            mensagem = f"ERRO SINTÁTICO próximo à linha {ultima_linha_end}: Esperava um '.' (ponto final) após o 'end' para finalizar o programa."
            if mensagem not in erros_sintaticos:
                erros_sintaticos.append(mensagem)
        else:
            # EOF em qualquer outro lugar do código
            if not erros_sintaticos or "Fim de arquivo" not in erros_sintaticos[
                    -1]:
                erros_sintaticos.append(
                    "ERRO SINTÁTICO: Fim de arquivo inesperado.")


parser = yacc.yacc()
