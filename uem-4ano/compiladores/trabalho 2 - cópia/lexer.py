import ply.lex as lex

erros_lexicos = []

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

tokens = list(palavras_reservadas.values()) + [
    'ATRIBUICAO',       
    'DOIS_PONTOS',      
    'PONTO_VIRGULA',    
    'VIRGULA',          
    'PARENTESE_ESQ',    
    'PARENTESE_DIR',    
    'PONTO_FINAL',      
    'OP_RELACIONAL',    
    'OP_SOMA',          
    'OP_SUBTRACAO',     
    'OP_MULTIPLICA',    
    'ID',              
    'NUMERO',           
]

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
t_OP_RELACIONAL = r'<>|<=|>=|<|>|='

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    val_lower = t.value.lower()

    if val_lower in palavras_reservadas:
        if t.value != val_lower:
            linha = t.lexer.lineno
            mensagem = f"ERRO LÉXICO na linha {linha}: Token '{t.value}' escrito incorretamente. O correto é '{val_lower}'."
            erros_lexicos.append(mensagem)
            t.type = palavras_reservadas[val_lower]
        else:
            t.type = palavras_reservadas[val_lower]
    else:
        t.type = 'ID'

    return t

def t_FLOAT_ERROR(t):
    r'\d+\.\d+'
    linha = t.lexer.lineno
    mensagem = f"ERRO LÉXICO na linha {linha}: Número '{t.value}' inválido. É aceito apenas números inteiros."
    erros_lexicos.append(mensagem)
    t.lexer.skip(len(t.value))

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value) 
    return t
    

def t_error(t):
    mensagem = f"ERRO LÉXICO: Símbolo ilegal '{t.value[0]}' na linha {t.lexer.lineno}"
    erros_lexicos.append(mensagem) 
    t.lexer.skip(1)

lexer = lex.lex()