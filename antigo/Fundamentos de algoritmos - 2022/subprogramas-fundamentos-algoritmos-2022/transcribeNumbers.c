// // ALUNA: INGRID LOHMANN
// // RA: 117698

// /*
// 1) ANÁLISE DO PROBLEMA
//   O problema consiste em criar um subprograma que lê o número (de 1 a 10) digitado pelo usuário e retornar o valor escrito por extenso.

// 2) DEFINIÇÃO DO TIPO DOS DADOS
//   Os dados utilizados nesse programa são:
//     Um do tipo int (int value) que receberá o valor digitado pelo usuário.
//     Um do tipo int (int value) que é usado como parâmetro na função transcribeNumbers.

// 3) CONSTRUÇÃO DO PROGRAMA
//   O programa primeiro recebe do usuário o número, em seguida um bloco de SWITCH será iniciado comparando o valor recebido com os possíveis casos. Caso o número esteja entre um dos casos disponíveis, o número por extenso será retornado, caso contrário a situação será a de DEFAULT, retornando que não foi possível transcrever o valor.

// 4) TESTES
//   Casos de testes:
//     Valor transcrito corretamente:
//       number: 5
//       esperado: cinco

//     Valor não transcrito:
//       number: 57
//       esperado: O número 55 não pode ser escrito por extenso no momento!

// 5) REVISÃO
//   Em resumo, o usuário deve fornecer o número, o programa irá comparar o valor fornecido com os casos disponíveis e retornar ou não o valor transcrito.
// */

#include <stdio.h>

void transcribeNumbers (int value) {

  switch (value) {
    case 1 :
     printf ("\nUm");
    break;
    
    case 2 :
      printf ("\nDois");
    break;
    
    case 3 :
      printf ("\nTrês");
    break;
    
    case 4 :
     printf ("\nQuatro");
    break;
    
    case 5 :
      printf ("\nCinco");
    break;
    
    case 6 :
     printf ("\nSeis");
    break;
    
    case 7 :
     printf ("\nSete");
    break;

    case 8 :
     printf ("\nOito");
    break;

    case 9 :
    printf ("\nNove");
    break;

    case 10 :
     printf ("\nDez");
    break;
    
    default :
     printf ("\nO número %i não pode ser escrito por extenso no momento!\n", value);
  }
  
}

int main (void )
{
   printf("*** PROGRAMA PARA ESCREVER O NÚMERO POR EXTENSO *** \n");

  int number;
  
  printf ("\nDigite um número de 1 a 10: ");
  scanf("%d", &number);
  
  transcribeNumbers(number);
  
  return 0;
}