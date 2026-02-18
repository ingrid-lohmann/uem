from lexer import tokens
import ply.yacc as yacc

# Estruturas de dados para análise semântica
tabela_simbolos = {}
erros_semanticos = []
erros_sintaticos = []


# Adiciona uma mensagem de erro semântico formatada à lista de erros.
def erro_semantico(linha, mensagem):
  erros_semanticos.append(f"ERRO SEMÂNTICO na linha {linha}: {mensagem}")


# --- Definição da Gramática com Recuperação de Erro ---


# Define a estrutura principal e uma regra para se recuperar de um cabeçalho malformado.
def p_programa(p):
  '''programa : INICIAR CALCULADIN DOIS_PONTOS lista_comandos FINALIZAR CALCULADIN PONTO'''

def p_programa_erro(p):
  """programa : INICIAR error DOIS_PONTOS lista_comandos FINALIZAR CALCULADIN PONTO"""
  parser.errok()

  
# Define a lista de comandos e uma regra para pular linhas com erros.
def p_lista_comandos(p):
  '''lista_comandos : lista_comandos comando PONTO_VIRGULA
                    | empty'''

def p_lista_comandos_erro(p):
  '''lista_comandos : lista_comandos error PONTO_VIRGULA'''
  parser.errok()


# Define que um comando pode ser uma chamada de função ou uma atribuição.
def p_comando(p):
  '''comando : chamada_funcao
             | atribuicao'''


# Define a sintaxe das funções 'input' e 'output' e realiza a análise semântica.
def p_chamada_funcao(p):
  '''chamada_funcao : INPUT LPAREN ID RPAREN
                    | OUTPUT LPAREN ID RPAREN'''
  tipo_chamada = p[1]
  var_name = p[3]
  linha = p.lineno(3)

  if tipo_chamada == 'input':
    if var_name not in tabela_simbolos:
      tabela_simbolos[var_name] = {'declarada': True, 'linha': linha}
  elif tipo_chamada == 'output':
    if var_name not in tabela_simbolos:
      erro_semantico(linha, f"Variável '{var_name}' não declarada.")


# Define a sintaxe de uma atribuição ('variavel = expressao') e declara a variável.
def p_atribuicao(p):
  '''atribuicao : ID IGUAL expr'''
  var_name = p[1]
  linha = p.lineno(1)
  if var_name not in tabela_simbolos:
    tabela_simbolos[var_name] = {'declarada': True, 'linha': linha}


# Define expressões de menor ordem (soma e subtração).
def p_expr(p):
  '''expr : expr MAIS termo
          | expr MENOS termo'''


# Regra que conecta a expressão a um 'termo'.
def p_expr_termo(p):
  'expr : termo'


# Define expressões de maior ordem (multiplicação e divisão).
def p_termo(p):
  '''termo : termo VEZES fator
           | termo DIVIDE fator'''


# Regra que conecta o termo a um 'fator'.
def p_termo_fator(p):
  'termo : fator'


# Define os elementos básicos de uma expressão (número, variável ou outra expressão entre parênteses).
def p_fator(p):
  '''fator : NUMERO
           | ID
           | LPAREN expr RPAREN'''
  if len(p) == 2 and isinstance(p[1], str):
    if p.slice[1].type == 'ID':
      if p[1] not in tabela_simbolos:
        erro_semantico(p.lineno(1), f"Variável '{p[1]}' não declarada.")


# Define uma produção vazia, usada para indicar partes opcionais da gramática.
def p_empty(p):
  'empty :'
  pass


# Função de tratamento de erros: apenas registra a mensagem.
def p_error(t):
  if t:
    mensagem = f"Token inesperado '{t.value}' na linha {t.lineno}"
    erros_sintaticos.append(f"ERRO SINTÁTICO: {mensagem}")
  else:
    if not erros_sintaticos or "Fim de arquivo" not in erros_sintaticos[-1]:
      erros_sintaticos.append("ERRO SINTÁTICO: Fim de arquivo inesperado.")


parser = yacc.yacc()
