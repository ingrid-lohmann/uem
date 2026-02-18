import ply.lex as lex

palavras_reservadas = {
    'input': 'INPUT',
    'output': 'OUTPUT',
    'iniciar': 'INICIAR',
    'finalizar': 'FINALIZAR',
    'calculadin': 'CALCULADIN',
}

tokens = list(palavras_reservadas.values()) + [
    'MAIS', 'MENOS', 'VEZES', 'DIVIDE', 'NUMERO', 'ID', 'PONTO_VIRGULA',
    'LPAREN', 'RPAREN', 'DOIS_PONTOS', 'IGUAL', 'PONTO'
]

t_MAIS = r'\+'
t_MENOS = r'-'
t_VEZES = r'\*'
t_DIVIDE = r'/'
t_PONTO_VIRGULA = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DOIS_PONTOS = r':'
t_IGUAL = r'='
t_PONTO = r'\.(?!\d)'

t_ignore = ' \t'

# --- ORDEM DE PRECEDÊNCIA DAS FUNÇÕES ---


# 1. Regra para Identificadores e Palavras Reservadas
def t_ID(t):
    r'[a-z][a-z0-9]*'
    t.type = palavras_reservadas.get(t.value, 'ID')
    return t


# 2. Regras de erro para números (MAIOR PRIORIDADE)
# Devem vir antes da regra de número válido para serem capturadas primeiro.


# Captura números que terminam com '.', como '10.', mas NÃO o '1.' de '1.5'
def t_MALFORMED_NUMBER_SUFFIX(t):
    r'\d+\.(?!\d)'  # O (?!\d) é um "negative lookahead" que garante que não há um dígito depois do '.'
    print(
        f"ERRO LÉXICO: Número malformado '{t.value}' na linha {t.lexer.lineno}. Se for decimal, deve ter ao menos um dígito após o ponto."
    )
    t.lexer.skip(len(t.value))


# Captura números que começam com '.', como '.5'
def t_MALFORMED_NUMBER_PREFIX(t):
    r'\.\d+'
    print(
        f"ERRO LÉXICO: Número malformado '{t.value}' na linha {t.lexer.lineno}. Números não podem começar com '.'."
    )
    t.lexer.skip(len(t.value))


# 3. Regra para NÚMEROS VÁLIDOS (MENOR PRIORIDADE)
def t_NUMERO(t):
    r'\d+\.\d+|\d+'
    t.value = float(t.value)
    return t


# 4. Regras restantes
def t_COMMENT(t):
    r'//.*'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# 5. Regra de erro genérica
def t_error(t):
    print(
        f"ERRO LÉXICO: Símbolo ilegal '{t.value[0]}' na linha {t.lexer.lineno}"
    )
    t.lexer.skip(1)


# Constrói o analisador léxico
lexer = lex.lex()
