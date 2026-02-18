/*
1) ANÁLISE DO PROBLEMA
  O problema consiste em receber quatro idades do usuário, calcular a média entre elas, analisa-las e retornar a maior idade e a médica calculada previamente.

2) DEFINIÇÃO DO TIPO DOS DADOS
  Os dados utilizados nesse programa são:
    Quatro do tipo float para receber a média (float average);
    Um do tipo char para receber o conceito (char *concept);
     Um do tipo int (int thereIsConcept) que irá servir como uma variável booleana, sendo que foi adotado 0 como false e 1 como true.

3) CONSTRUÇÃO DO PROGRAMA
  O programa primeiro recebe do usuário o valor da média, em seguida um bloco de IF será iniciado comparando a média com o conceito.
Sendo eles: 
  Conceito A: média entre 9.0 e 10;
  Conceito B: média entre 7.0 e 8.9;
  Conceito C: média entre 5.0 e 6.9;
  Conceito D: média entre 0 e 4.9;
  Indefinido: média maior que 10;

  Nos casos do conceitos A, B, C e D, o valor da variável thereIsConcept será de 1, caso contrário será de 0.
  Após a classificação (ou não) do conceito da média, um segundo bloco de IF será iniciado, analisando o valor da variável thereIsConcept, caso ele seja de 1, o valor do conceito será retornado ao usuário, porém, caso seja 0, uma mensagem com informando que não foi possível calcular o conceito da média será retornado, junto com uma aviso de que o valor da média deve ser entre 0 e 10.

4) TESTES
  Casos de testes:
    Conceito A:
      Exemplo: 
        1 - average = 9.5;
        concept: A
        thereIsConcept = 1;

        2 - average = 10;
        concept: A
        thereIsConcept = 1;

        3 - average = 9.0;
        concept: A
        thereIsConcept = 1;
      
    Conceito B:
      Exemplo: 
        1 - average = 8.9;
        concept: B
        thereIsConcept = 1;

        2 - average = 8.7;
        concept: B
        thereIsConcept = 1;

        3 - average = 7.6;
        concept: B
        thereIsConcept = 1;

   Conceito C:
      Exemplo: 
        1 - average = 5.6;
        concept: C
        thereIsConcept = 1;

        2 - average = 6.9;
        concept: C
        thereIsConcept = 1;

        3 - average = 6.1;
        concept: C
        thereIsConcept = 1;
    
    Conceito D:
      Exemplo: 
        1 - average = 0;
        concept: D
        thereIsConcept = 1;

        2 - average = 2.7;
        concept: D
        thereIsConcept = 1;

        3 - average = 4.9;
        concept: D
        thereIsConcept = 1;

    Sem Conceito:
      Exemplo: 
        1 - average = 99;
        concept: inexistente
        thereIsConcept = 0;

        2 - average = 32;
        concept: inexistente
        thereIsConcept = 0;

        3 - average = -4;
        concept: inexistente
        thereIsConcept = 0;

5) REVISÃO
  Em resumo, o usuário deve fornecer a média, o programa irá analisar o conceito na qual ela se encaixa. Caso se encaixe em algum dos conceitos (A,B, C e D) a classificação será retornada, caso contrário uma mensagem de alerta será exibida.
*/


#include <stdio.h>

int main(void) {
  printf("*** PROGRAMA PARA VERIFICAR O CONCEITO DE MÉDIAS *** \n");

  float average;
  char *concept = "";
  int thereIsConcept;

  printf("\nDigite a média do aluno para saber o conceito da nota: ");
  scanf("%f", &average);
  
  if (average >= 0 && average <= 4.9) {
    concept = "D";
    thereIsConcept = 1;
  } else if (average >= 5.0 && average <= 6.9) {
    concept = "C";
    thereIsConcept = 1;
  } else if (average >= 7.0 && average <= 8.9) {
    concept = "B";
    thereIsConcept = 1;
  } else if (average >= 9.0 && average <= 10) {
    concept = "A";
    thereIsConcept = 1;
  } else {
    thereIsConcept = 0;
  }

  if (thereIsConcept == 1) {
    printf("\nO conceito da média é igual a %s\n.", concept);
  } else {
    printf("\aNão foi possível calcular o conceito da média! Por favor, digite um valor entre 0 e 10. \n");
  }

  return 0;
}

