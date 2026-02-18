import ply.lex as lex

# --- Especificação Léxica da Linguagem Tascal ---

# 1. Palavras Reservadas 
palavras_reservadas = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'begin': 'BEGIN',
    'end': 'END',
    'integer': 'INTEGER',
    'boolean': 'BOOLEAN',
    'read': 'READ',
    'write': 'WRITE',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'false': 'FALSE',
    'true': 'TRUE',
    'div': 'DIV'
}

# 2. Lista de Tokens
# Inclui as palavras reservadas e os símbolos especiais da linguagem.
tokens = list(palavras_reservadas.values()) + [
    'ATRIBUICAO',       # :=
    'DOIS_PONTOS',      # :
    'PONTO_VIRGULA',    # ;
    'VIRGULA',          # ,
    'PARENTESE_ESQ',    # (
    'PARENTESE_DIR',    # )
    'PONTO_FINAL',      # .

    # Operadores 
    'OP_RELACIONAL',    # =, <>, <, <=, >, >=
    'OP_ADITIVO',       # +, -
    'OP_MULTIPLICATIVO',# * # Tokens para Tipos de Dados 
    'ID',               # Identificadores
    'NUMERO',           # Constantes numéricas inteiras
]

# 3. Expressões Regulares para Símbolos e Operadores
# Para cada símbolo simples, uma expressão regular é definida.
t_ATRIBUICAO = r':='
t_DOIS_PONTOS = r':'
t_PONTO_VIRGULA = r';'
t_VIRGULA = r','
t_PARENTESE_ESQ = r'\('
t_PARENTESE_DIR = r'\)'
t_PONTO_FINAL = r'\.'
t_OP_SOMA = r'\+'
t_OP_SUBTRACAO = r'-'
t_OP_MULTIPLICA = r'\*'
t_OP_DIVIDE = r'div'
t_OP_RELACIONAL = r'<>|<=|>=|<|>|='

# 4. Caracteres a serem ignorados 
# Espaços, tabulações e quebras de linha não possuem significado e devem ser ignorados. 
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# 5. Regras para Tokens Complexos (Identificadores e Números)

# Regra para Identificadores 
# Devem iniciar com uma letra, seguida por letras, dígitos ou sublinhados. 
# A linguagem é case-sensitive.
def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    # Verifica se o identificador é uma palavra reservada
    t.type = palavras_reservadas.get(t.value, 'ID')
    return t

# Regra para Números 
# A linguagem Tascal suporta apenas constantes numéricas na base decimal (inteiros). 
# Números negativos são tratados sintaticamente (ex: '-' é um token, '42' é outro).
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)  # Converte o valor para inteiro
    return t


def t_BOOLEAN(t):
    r'\false\b|\true\b'
    t.value = bool(t.value)
    return t


# 6. Tratamento de Erros (Página 3)
# Símbolos não reconhecidos devem ser reportados como erro léxico. 
# A mensagem deve indicar a linha e a natureza do erro. 
def t_error(t):
    print(f"ERRO LÉXICO: Símbolo ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Constrói o analisador léxico
lexer = lex.lex()

