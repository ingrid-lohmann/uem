/*
1) ANÁLISE DO PROBLEMA
  O problema consiste em receber quatro idades do usuário, calcular a média entre elas, analisa-las e retornar a maior idade e a médica calculada previamente.

2) DEFINIÇÃO DO TIPO DOS DADOS
  Os dados utilizados nesse programa são:
    Quatro do tipo int para receber as idades (int firstAgeValue, secondAgeValue, thirdAgeValue, fourthAgeValue);
    Um do tipo int para receber a maior idade (int olderAge);
    Um do tipo float para receber o valor do cálculo da média (float average).

3) CONSTRUÇÃO DO PROGRAMA
  O programa primeiro recebe do usuário o valor das quatro idades e armazena cada um em uma respectiva variável. Em seguida a média aritmética simples das idades é calculada.
Logo após o cálculo da média um bloco de if é iniciado, onde as comparações de cada idade é feita com as demais. Caso a verificação seja verdadeira o valor da idade que está sendo comprada será armazenada na variável olderAge.
Por fim os valores da maior idada e da média são retornados ao usuário.

4) TESTES
  Casos de testes:
    Maior idade é a primeira:
      Exemplo: 
        1- firstAgeValue = 50, secondAgeValue = 40, thirdAgeValue = 11, fourthAgeValue = 4;
        Maior idade: 50 e média: 26.00.
      
    Maior idade é a segunda:
      Exemplo: 
        1- firstAgeValue = 22, secondAgeValue = 78, thirdAgeValue = 17, fourthAgeValue = 41;
        Maior idade: 78 e média: 39.00.

    Maior idade é a terceira:
      Exemplo: 
        1- firstAgeValue = 11, secondAgeValue = 28, thirdAgeValue = 99, fourthAgeValue = 33;
        Maior idade: 99 e média: 42.00.
    
    Maior idade é a quarta:
      Exemplo: 
        1- firstAgeValue = 10, secondAgeValue = 88, thirdAgeValue = 30, fourthAgeValue = 89;
        Maior idade: 89 e média: 54.00.

5) REVISÃO
  Em resumo, o usuário deve fornecer quatro idades, o programa irá calcular a média aritmética simples entre elas, retornado esse valor e o valor da maior idade fornecida.
*/


#include <stdio.h>

int main(void) {
  printf("*** PROGRAMA PARA CALCULAR A MÉDIA DE IDADES E TAMBÉM PARA RETORNAR A MAIOR IDADE *** \n\n");

  int firstAgeValue, secondAgeValue, thirdAgeValue, fourthAgeValue, olderAge;
  float average;

  printf("Digite o valor da primeira idade: ");
  scanf("%i", &firstAgeValue);
  
  printf("Digite o valor da segunda idade: ");
  scanf("%i", &secondAgeValue);

  printf("Digite o valor da terceira idade: ");
  scanf("%i", &thirdAgeValue);

  printf("Digite o valor da quarta idade: ");
  scanf("%i", &fourthAgeValue);

 average = (firstAgeValue + secondAgeValue + thirdAgeValue + fourthAgeValue)/4;

  if ((firstAgeValue > secondAgeValue) && (firstAgeValue > thirdAgeValue) && (firstAgeValue > fourthAgeValue)) {
    olderAge = firstAgeValue;
  } else if ((secondAgeValue > firstAgeValue) && (secondAgeValue > thirdAgeValue) && (secondAgeValue > fourthAgeValue)) {
    olderAge = secondAgeValue;
  } else if ((thirdAgeValue > secondAgeValue) && (thirdAgeValue > fourthAgeValue) && (thirdAgeValue > firstAgeValue)) {
    olderAge = thirdAgeValue;
  } else {
    olderAge = fourthAgeValue;
  }

  printf("\nA média das idades é de: %.2f\n", average);
  printf("\nA maior idade é a: %i\n", olderAge);
  return 0;
}

