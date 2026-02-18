Relatório Técnico: Compilador para a Linguagem Tascal

Disciplina: 11927 - Introdução à Compilação
Equipe: [Seu Nome ou Nomes da Equipe]
Data: 23/10/2025

1. Ferramenta Utilizada

Para a implementação do compilador da linguagem Tascal, foi utilizada a linguagem de programação Python juntamente com a biblioteca PLY (Python Lex-Yacc).

PLY: Esta biblioteca foi escolhida por fornecer uma implementação conveniente e direta dos analisadores léxico (Lex) e sintático (Yacc) em Python, facilitando a definição de tokens, regras gramaticais e ações semânticas. A versão utilizada é a mais recente disponível via pip.

2. Organização Básica do Código

O código-fonte do compilador foi estruturado em quatro arquivos principais para promover modularidade e clareza:

lexer.py:

Responsabilidade: Análise Léxica.

Conteúdo: Define as palavras reservadas, os tokens da linguagem Tascal (incluindo operadores, símbolos especiais, identificadores e números), as expressões regulares para reconhecimento dos tokens e o tratamento básico de erros léxicos (símbolos ilegais). Também inclui uma lógica para identificar e reportar palavras reservadas escritas com grafia incorreta (maiúsculas/minúsculas).

analise_semantica.py:

Responsabilidade: Análise Semântica e Gerenciamento de Estado Semântico.

Conteúdo: Contém a Tabela de Símbolos (implementada como um dicionário Python), a lista para armazenamento de erros semânticos, e todas as funções auxiliares responsáveis pelas checagens semânticas (verificação de declarações, tipos, etc.). Esta separação visa manter o arquivo do parser focado na gramática.

parser.py:

Responsabilidade: Análise Sintática e Recuperação de Erros Sintáticos.

Conteúdo: Define a gramática da linguagem Tascal, baseada na especificação EBNF fornecida (adaptada para o formato do PLY), e a precedência dos operadores. As regras gramaticais invocam as funções de checagem semântica do módulo analise_semantica.py. Inclui também regras específicas para recuperação de erros sintáticos comuns (ex: falta de then, do, ponto final, operador de atribuição incorreto, etc.), permitindo que a análise continue após um erro e fornecendo mensagens mais informativas.

main.py:

Responsabilidade: Orquestração do Processo de Compilação.

Conteúdo: É o ponto de entrada do compilador. Lê o nome do arquivo de código-fonte Tascal a partir dos argumentos da linha de comando, lê o conteúdo do arquivo, inicializa/limpa os estados dos analisadores (listas de erros, tabela de símbolos), invoca o parser, e por fim, exibe os erros encontrados (léxicos, sintáticos e semânticos) ou uma mensagem de sucesso.

3. Ações Semânticas Implementadas

As seguintes verificações e ações semânticas foram implementadas, primariamente no módulo analise_semantica.py e invocadas pelo parser.py:

Gerenciamento da Tabela de Símbolos:

Armazena o identificador do programa.

Registra todas as variáveis declaradas na seção var com seus respectivos tipos (integer ou boolean).

Verificação de Declarações:

Declaração Duplicada: Emite um erro se uma variável for declarada mais de uma vez no escopo global.

Uso Antes da Declaração: Emite um erro se um identificador for utilizado em uma expressão ou comando (read, write, lado direito de :=) sem ter sido previamente declarado.

Verificação de Tipos:

Atribuição (:=): Garante que o tipo da expressão à direita seja compatível com o tipo da variável à esquerda.

Comandos Condicionais (if) e de Repetição (while): Verifica se a expressão de controle resulta em um valor boolean.

Operadores Aritméticos (+, -, *, div): Exige que ambos os operandos sejam do tipo integer. O resultado é integer.

Operadores Lógicos (and, or, not): Exige que o(s) operando(s) seja(m) do tipo boolean. O resultado é boolean.

Operadores Relacionais:

=, <>: Permitem comparação entre operandos do mesmo tipo (integer com integer ou boolean com boolean). O resultado é boolean.

<, <=, >, >=: Exigem que ambos os operandos sejam do tipo integer. O resultado é boolean.

Comando read: Verifica se todos os argumentos são identificadores de variáveis já declaradas.

Comando write: Permite qualquer expressão válida (integer ou boolean). A validação do tipo da expressão ocorre durante a análise da própria expressão.

4. Etapas Não Cumpridas

Com base na especificação do trabalho e nos casos de teste fornecidos (P1 a P10 e PErr01 a PErr18), todas as etapas solicitadas foram cumpridas. O compilador:

Realiza a análise léxica, sintática e semântica.

Utiliza a ferramenta PLY.

Aceita corretamente todos os programas válidos fornecidos.

Rejeita corretamente todos os programas inválidos fornecidos, emitindo mensagens de erro que indicam a linha e a natureza do problema (léxico, sintático ou semântico).

Implementa recuperação de erros sintáticos para identificar múltiplos erros em uma única compilação e fornecer mensagens mais precisas.

É executado via linha de comando, recebendo o nome do arquivo como argumento.

Não há justificativas a apresentar, pois todos os requisitos foram atendidos.