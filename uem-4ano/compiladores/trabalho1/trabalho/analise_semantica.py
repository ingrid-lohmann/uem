# --- Estado Semântico ---
tabela_simbolos = {}
erros_semanticos = []

# --- Funções Auxiliares de Base ---
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


# --- Funções de Checagem Semântica ---
def checar_id_programa(nome, linha):
    if nome in tabela_simbolos:
        erro_semantico(
            linha,
            f"Identificador de programa '{nome}' já utilizado como variável.")


def checar_atribuicao(tipo_variavel, tipo_expressao, nome_variavel, linha):
    if tipo_variavel and tipo_expressao is not None and tipo_variavel != tipo_expressao:
        erro_semantico(
            linha,
            f"Tipo da expressão ('{tipo_expressao}') incompatível com o tipo da variável '{nome_variavel}' ('{tipo_variavel}')."
        )


def checar_condicao_booleana(tipo_expressao, linha, comando):
    if tipo_expressao != 'boolean':
        erro_semantico(
            linha,
            f"A expressão do comando '{comando}' deve ser do tipo 'boolean'.")


def checar_operacao_logica_relacional(tipo1, op_token, op_valor, tipo2, linha):
    if op_token.type in ['AND', 'OR']:
        if tipo1 != 'boolean' or tipo2 != 'boolean':
            erro_semantico(
                linha,
                f"Operador lógico '{op_valor}' exige operandos do tipo 'boolean'."
            )
        return 'boolean'
    elif op_token.type == 'OP_RELACIONAL':
        if op_valor in ['=', '<>']:
            if tipo1 != tipo2:
                erro_semantico(
                    linha,
                    f"Operador '{op_valor}' exige operandos do mesmo tipo (recebeu '{tipo1}' e '{tipo2}')."
                )
        else:  
            if tipo1 != 'integer' or tipo2 != 'integer':
                erro_semantico(
                    linha,
                    f"Operador relacional '{op_valor}' exige operandos do tipo 'integer'."
                )
        return 'boolean'


def checar_operacao_matematica(tipo1, op_token, op_valor, tipo2, linha):
    if tipo1 != 'integer' or tipo2 != 'integer':
        erro_semantico(
            linha,
            f"Operador aritmético '{op_valor}' exige operandos do tipo 'integer'."
        )
    return 'integer'


def checar_not(tipo, linha):
    if tipo != 'boolean':
        erro_semantico(linha,
                       "Operador 'not' exige um operando do tipo 'boolean'.")
    return 'boolean'


def checar_uminus(tipo, linha):
    if tipo != 'integer':
        erro_semantico(
            linha,
            "Operador de negação '-' exige um operando do tipo 'integer'.")
    return 'integer'
