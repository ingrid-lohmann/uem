/*
1) ANÁLISE DO PROBLEMA
  O problema consiste em receber três medidas do usuário, analisa-las e concluir se elas formam ou não um triângulo. Caso formem, é espetrado que o programa retorne a sua classificação.

2) DEFINIÇÃO DO TIPO DOS DADOS
  Os dados utilizados nesse programa são:
    Três do tipo float para as medidas do triângulo (float a, b, c);
    Um do tipo char para receber a classifcação (char *triangleType);
    Um do tipo int (int thereIsTriangle) que irá servir como uma variável booleana, sendo que foi adotado 0 como false e 1 como true.

3) CONSTRUÇÃO DO PROGRAMA
  O programa foi construido para, primeiro, receber os três valores dos lados (a, b, c) do possível triângulo. Após receber os valores, uma estrutura IF analisa a relação das medidas recebidas. A primeira análise é a de se uma das medidas é menor que a soma das outras duas, isso é verificado para os três casos e foi usado um operador lógico AND para retornar se a análise é verdadeira ou não.
Caso seja, uma segunda estrutura IF será iniciada para analisar os seguintes casos:
  se todas as medidas são iguais: neste caso, a variável "triangleType" recebe o valor de "equilatero" e thereIsTriangle recebe o valor 1.
  se apenas duas das medidas são iguais: neste caso, a variável "triangleType" recebe o valor de "isosceles" e thereIsTriangle recebe o valor 1.
  se nenhuma das medidas são iguais: neste caso, a variável "triangleType" recebe o valor de "escaleno" e thereIsTriangle recebe o valor 1.
Caso aquela primeira verificação do IF (a de que um lado é menor que a soma dos outros dois) então é retornado uma string vazia para a variável triangleType e o thereIsTriangle recebe o valor de 0.

Após todas as verificações um segundo bloco IF é iniciado agora analisando o valor da variável thereIsTriangle. Caso o valor seja 1, a classificação do tipo o triângulo é retornada ao usuário, caso contrátrio a mensagem de que as medidas fornecidas não formam um triângulo é mostrada.

4) TESTES
  Casos de testes:
    Triângulo Equilátero: todas as medidas devem ser iguais e maiores que 0.
      Exemplos: 
        1 - a = 1, b = 1, c = 1;
        2 - a = 3, b = 3, c = 3;
      
    Triângulo isósceles: duas das três medidas forncecidas devem ser iguais e maiores que 0.
Exemplos: 
        1 - a = 2, b = 2, c = 1;
        2 - a = 2, b = 2, c = 3;

    Triângulo escaleno: todas as medidas devem ser diferentes e maiores que 0.
Exemplos: 
        1 - a = 2, b = 2, c = 1;
        2 - a = 2, b = 2, c = 3;

Obs: em todos os casos acima o valor da variável thereIsTriangle é 1;

    Não formam um triângulo: as medidas não podem atender a propriedade de que um das medidas deve ser menor que a soma das outras duas.
Exemplos: 
        1 - a = 1, b = 2, c = 3;
        2 - a = 0, b = 1, c = 1;

Obs: no caso acima o valor da variável thereIsTriangle é 0;

5) REVISÃO
  Em resumo, o usuário deve fornecer três medidas, o programa irá analisar se elas atendem a propriedade de existência de um triângulo, caso atendem é retornado o tipo de triângulo que essas medidas formam, caso contrário uma mansagem informando que elas não atendem a propriedade é retornada.
*/

#include <stdio.h>

int main(void) {
  printf("*** PROGRAMA PARA VERIFICAR A EXISTÊNCIA (OU NÃO) DE UM TRIÂNGULO E CLASSIFICÁ-LO *** \n\n");

  float a, b, c;
  int thereIsTriangle;
  char *triangleType = "";
  
  printf("Digite a medida A: ");
  scanf("%f", &a);

  printf("Digite a medida B: ");
  scanf("%f", &b);

  printf("Digite a medida C: ");
  scanf("%f", &c);
  
  if ((a < b + c) && (b < a + c) && (c < a + b)) {
    if (a == b && b == c) {
      triangleType = "equilátero.";
      thereIsTriangle = 1;
    } else if ((a == b) || (b == c) || (c == a)) {
      triangleType = "isósceles.";
      thereIsTriangle = 1;
    } else {
      triangleType = "escaleno.";
      thereIsTriangle = 1;
    }
  } else {
    triangleType = " ";
    thereIsTriangle = 0;
  }

  if (thereIsTriangle == 1) {
    printf("\nO triângulo é do tipo %s\n", triangleType);
  } else {
    printf("\n\aOps! Parece que essas medidas não formam um triangulo!");
  }

  return 0;
}

