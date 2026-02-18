// ALUNA: INGRID LOHMANN
// RA: 117698

/*
1) ANÁLISE DO PROBLEMA
  O problema consiste em receber quatro idades do usuário, analisa-las e retornar a maior idade entre as quatro fornecidas.

2) DEFINIÇÃO DO TIPO DOS DADOS
  Os dados utilizados nesse programa são:
    Quatro do tipo int para receber as idades (int firstAgeValue, secondAgeValue, thirdAgeValue, fourthAgeValue);
    Um do tipo int (int firstComparison) para receber o resultado da comparação do primeiro par de idades;
  Um do tipo int (int secondComparison) para receber o resultado da comparação do segundo par de idades;
    Um do tipo int (int olderAge) para receber a maior idade final;

3) CONSTRUÇÃO DO PROGRAMA
  O programa primeiro recebe do usuário o valor das quatro idades e armazena cada um em uma respectiva variável. A função compareAges é executada e recebendo como parâmetros os valores de firstAgeValue e secondAgeValue e o resultado é armazedado na variável firstComparison. De forma similar os pares de idades thirdAgeValue, fourthAgeValue também são comparados e o resultado armazenado em secondComparison. Por fim os valores armazenados em firstComparison e secondComparison são comparados utilizando a função compareAges e o resultado é armazenado e retornado ao usuário através da variável olderAge.

4) TESTES
  Casos de testes:
    Maior idade é a primeira:
      Exemplo: 
        1- firstAgeValue = 50, secondAgeValue = 40, thirdAgeValue = 11, fourthAgeValue = 4;
        esperado: A maior idade é de 50 anos
      
    Maior idade é a segunda:
      Exemplo: 
        1- firstAgeValue = 22, secondAgeValue = 78, thirdAgeValue = 17, fourthAgeValue = 41;
        esperado: A maior idade é de 78 anos

    Maior idade é a terceira:
      Exemplo: 
        1- firstAgeValue = 11, secondAgeValue = 28, thirdAgeValue = 99, fourthAgeValue = 33;
       esperado: A maior idade é de 99 anos
    
    Maior idade é a quarta:
      Exemplo: 
        1- firstAgeValue = 10, secondAgeValue = 88, thirdAgeValue = 30, fourthAgeValue = 89;
        esperado: A maior idade é de 89 anos

5) REVISÃO
  Em resumo, o usuário deve fornecer quatro idades, o programa comparar as idades através da função compareAges e o resultado será retornado ao usuário através da variável olderAge.
*/

#include <stdio.h>

int compareAges (int firstValue, int secondValue) {
  int result;
  
  if (firstValue > secondValue) {
    result = firstValue;
  } else {
    result = secondValue;
  }

  return result;
}


int main(void) {
  printf("*** PROGRAMA PARA CALCULAR A MÉDIA DE IDADES E TAMBÉM PARA RETORNAR A MAIOR IDADE *** \n\n");

  int firstAgeValue, secondAgeValue, thirdAgeValue, fourthAgeValue, firstComparison, secondComparison, olderAge;


  printf("Digite o valor da primeira idade: ");
  scanf("%i", &firstAgeValue);
  
  printf("Digite o valor da segunda idade: ");
  scanf("%i", &secondAgeValue);

  printf("Digite o valor da terceira idade: ");
  scanf("%i", &thirdAgeValue);

  printf("Digite o valor da quarta idade: ");
  scanf("%i", &fourthAgeValue);

  firstComparison = compareAges(firstAgeValue, secondAgeValue);
  secondComparison = compareAges(thirdAgeValue, fourthAgeValue);

  olderAge = compareAges(firstComparison, secondComparison);


  printf("\nA maior idade é de %i anos", olderAge);
  return 0;
}

