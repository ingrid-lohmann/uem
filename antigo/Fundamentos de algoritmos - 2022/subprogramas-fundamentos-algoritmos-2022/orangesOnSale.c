// ALUNA: INGRID LOHMANN
// RA: 117698

/*
1) ANÁLISE DO PROBLEMA
  O problema consiste em criar um subprograma que lê o valor de laranjas digitado pelo usuário e retornar o valor que a se pagar, baseando-se na quantidade fornecida.

2) DEFINIÇÃO DO TIPO DOS DADOS
  Os dados utilizados nesse programa são:
    Um do tipo float (int total) que retorna o valor final para o usuário.
    Um do tipo int (int oranges) que receberá o valor digitado pelo usuário.
    Um do tipo int (int value) que é usado como parâmetro na função purchaseTotal.

3) CONSTRUÇÃO DO PROGRAMA
  O programa primeiro recebe do usuário o número de4 laranjas, em seguida um bloco de IF será iniciado comparando o valor recebido com os dois possíveis casos. Caso o número esteja seja menor que 12, o valor digitado será multiplicado por 0,35 e o resultado armazenado na variável total. Se não o valor será multiplicado por 0,30 e o resultado também será armazenado na variável total.

4) TESTES
  Casos de testes:
    Valor inserido igual a 6:
      oranges: 6
      esperado: O valor total da compra é de R$ 2.10

    Valor inserido igual a 10:
      oranges: 10
      esperado: O valor total da compra é de R$ 3.50

    Valor inserido igual a 20:
      oranges: 20
      esperado: O valor total da compra é de R$ 6.00

    Valor inserido igual a 1000:
      oranges: 1000
      esperado: O valor total da compra é de R$ 300.00

5) REVISÃO
  Em resumo, o usuário deve fornecer o número de laranjas que deseja comprar, e o programa irá retornar o valor baseanda se o número mínimo exigido para que o desconto seja aplicado foi atingido.
*/

// #include <stdio.h>

// void purchaseTotal (int value) {
//   float total;
  
//   if (value < 12) {
//     total = (value * 0.35);
//   } else {
//     total = (value * 0.30);
//   }

//   printf ("O valor total da compra é de R$ %.2f\n", total);
// }

// int main (void) {
//    printf("*** PROGRAMA PARA CALCULAR O VALOR DA COMPRA DE LARANJAS *** \n");

//   int oranges;
  
  
//   printf ("\nDigite o número de laranjas: ");
//   scanf("%d", &oranges);

//   purchaseTotal(oranges);
 
//   return 0;
// }

